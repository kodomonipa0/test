"""Minimal FastAPI application for audio feature extraction."""
from fastapi import FastAPI, Query
import librosa

from analysis import analyze_corpus, extract_features

app = FastAPI(title="Music analysis app")


@app.get("/analyze")
def analyze_example() -> dict:
    """Analyze an example audio file shipped with librosa.

    Returns
    -------
    dict
        Path of the example audio file and extracted features.
    """
    audio_path = librosa.util.example_audio_file()
    return {
        "audio_path": audio_path,
        "features": extract_features(audio_path),
    }


@app.get("/analyze_corpus")
def analyze_corpus_endpoint(directory: str = Query(..., description="Path to a directory of audio files")) -> dict:
    """Analyze all audio files in a directory.

    Parameters
    ----------
    directory:
        Filesystem path containing audio files.

    Returns
    -------
    dict
        Mapping from file names to feature dictionaries.
    """
    return {
        "directory": directory,
        "results": analyze_corpus(directory),
    }
