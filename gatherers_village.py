from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Agent:
    name: str
    hunger: int = 0
    energy: int = 100

    def baseline(self) -> None:
        self.hunger = min(self.hunger + 1, 100)

    def forage(self) -> None:
        self.energy = max(self.energy - 12, 0)
        self.hunger = min(self.hunger + 5, 100)

    def rest(self) -> None:
        self.energy = min(self.energy + 20, 100)
        self.hunger = min(self.hunger + 2, 100)

    def eat(self) -> None:
        self.hunger = max(self.hunger - 30, 0)
        self.energy = min(self.energy + 5, 100)


def policy(agent: Agent, basket: int, num_agents: int) -> str:
    if agent.hunger >= 70 and basket > 0:
        return "eat"
    if basket <= max(1, num_agents // 2) and agent.energy >= 25:
        return "forage"
    if agent.energy < 30:
        return "rest"
    return "forage"


def simulate(days: int = 10, ticks_per_day: int = 24) -> None:
    N = 6
    basket = 3
    field = 40
    regen = 20
    p_base = 0.2
    synergy = 0.15
    p_cap = 0.9

    agents: List[Agent] = [Agent(f"A{i}") for i in range(N)]

    for day in range(1, days + 1):
        gathered = 0
        eaten = 0
        for _ in range(ticks_per_day):
            for ag in agents:
                ag.baseline()
            actions = [policy(ag, basket, N) for ag in agents]
            foragers = actions.count("forage")
            p = min(p_base + synergy * (foragers - 1), p_cap) if foragers else 0.0
            for ag, act in zip(agents, actions):
                if act == "eat":
                    if basket > 0:
                        basket -= 1
                        ag.eat()
                        eaten += 1
                elif act == "rest":
                    ag.rest()
                else:  # forage
                    ag.forage()
                    if field > 0 and random.random() < p:
                        basket += 1
                        field -= 1
                        gathered += 1
        avg_h = sum(ag.hunger for ag in agents) / N
        avg_e = sum(ag.energy for ag in agents) / N
        starv = sum(1 for ag in agents if ag.hunger >= 95)
        print(
            f"Day {day}: basket={basket}, avg_hunger={avg_h:.1f}, avg_energy={avg_e:.1f}, "
            f"gathered={gathered}, eaten={eaten}, starvation_warnings={starv}"
        )
        field += regen


if __name__ == "__main__":
    random.seed(0)
    simulate()
