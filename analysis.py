"""Audio analysis utilities for feature extraction."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import librosa


def extract_features(path: str, hop_length: int = 512) -> Dict[str, Any]:
    """Load an audio file and compute simple spectral features.

    Parameters
    ----------
    path:
        Path to the audio file.
    hop_length:
        Hop length for the short-time analysis.

    Returns
    -------
    dict
        Dictionary containing the sample rate, hop length and selected
        features converted to plain Python lists for JSON serialisation.
    """
    y, sr = librosa.load(path)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, hop_length=hop_length
    )[0]
    return {
        "sample_rate": int(sr),
        "hop_length": hop_length,
        "rms": rms.tolist(),
        "spectral_centroid": centroid.tolist(),
    }


def analyze_corpus(directory: str) -> Dict[str, Dict[str, Any]]:
    """Analyse all audio files in a directory.

    Parameters
    ----------
    directory:
        Directory containing audio files with extensions like WAV/MP3/FLAC.

    Returns
    -------
    dict
        Mapping from file names to their extracted feature dictionaries.
    """
    files = librosa.util.find_files(directory, ext=["wav", "mp3", "flac"])
    return {Path(f).name: extract_features(f) for f in files}
