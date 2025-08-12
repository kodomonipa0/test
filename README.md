# Music analysis app

This repository contains a minimal FastAPI application that demonstrates
how to extract simple audio features using [librosa](https://librosa.org/).

## Installation

```bash
pip install -r requirements.txt
```

## Running the application

Start the development server:

```bash
uvicorn app:app --reload
```

Endpoints:

- `GET /analyze` – extract features from an example audio file shipped with
  librosa.
- `GET /analyze_corpus?directory=/path/to/data` – extract features for every
  audio file in a directory. Supported extensions: WAV, MP3 and FLAC.
