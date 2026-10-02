# AI Audio Transcription

This project uses OpenAI Whisper to transcribe an audio file into text.

## Requirements

- Docker
- A local audio file such as `sample-0.mp3`

## Project files

- `audio_to_text.py` - Python script that transcribes audio
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image definition
- `.dockerignore` - files to ignore when building the image

## Run locally without Docker

Use the script from the project folder:

```powershell
python audio_to_text.py sample-0.mp3 -o transcript.txt -m small -l en
```

If your audio file is elsewhere, you can pass the full path:

```powershell
python audio_to_text.py "D:\Whisper_Testing\sample-0.mp3" -o transcript.txt -m small -l en
```

You can also run it with the default values, if the file is named `sample-0.mp3`:

```powershell
python audio_to_text.py
```

## Install Docker Desktop (Windows)

Docker is a system-level tool, not a Python package, so it must be installed separately on your machine.

1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Start Docker Desktop and wait for it to finish initializing.
3. Verify it is installed:

```powershell
docker --version
```

## Build Docker image

From the project folder:

```powershell
docker build -t whisper-app .
```

## Run Docker container

Mount the current folder so the audio file and transcript can be accessed:

```powershell
docker run --rm -it -v "${PWD}:/app" whisper-app sample-0.mp3 -o transcript.txt -m small -l en
```

If you want to use a different audio file:

```powershell
docker run --rm -it -v "${PWD}:/app" whisper-app my-audio-file.mp3 -o transcript.txt -m small -l en
```

## GitHub Actions

This project includes a workflow file at `.github/workflows/best-transcribe.yml`.

To run it in GitHub Actions:

1. Push the repository to GitHub.
2. Open the repository in GitHub.
3. Go to the Actions tab.
4. Select `Whisper Best Workflow`.
5. Click `Run workflow`.
6. Enter values such as:
   - `audio_file`: `sample-0.mp3`
   - `language`: `en`
   - `model`: `small`

The workflow runs the same script and uploads the generated `transcript.txt` as an artifact.

## Output

The transcription will be printed to the terminal and saved in `transcript.txt`.

## Notes

- `small` is a good CPU-friendly Whisper model for general use.
- Use `-l en` when the audio is in English.
- If the audio is noisy or includes music, Whisper may misinterpret the sound.
