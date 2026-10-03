# AI Audio Transcription

This project uses OpenAI Whisper to transcribe audio files into text. The command-line tool and web UI accept files in any format supported by FFmpeg, including common formats such as MP3, WAV, M4A, FLAC, AAC, and OGG.

## Requirements

- Docker
- A local audio file such as `sample-0.mp3`
- FFmpeg installed and available on `PATH` when running outside Docker. Whisper uses FFmpeg to decode audio; formats/codecs not supported by your FFmpeg build cannot be transcribed.

## Project files

- `audio_to_text.py` - Python script that transcribes audio
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image definition
- `.dockerignore` - files to ignore when building the image

## Run locally without Docker

Use the script from the project folder. Replace the example filename with an audio file in any format supported by FFmpeg:

```powershell
python audio_to_text.py "recording.m4a" -o transcript.txt -m small -l en
```

If your audio file is elsewhere, you can pass the full path:

```powershell
python audio_to_text.py "D:\Whisper_Testing\recording.flac" -o transcript.txt -m small -l en
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

## Run the web UI in Docker

Start the web server:

```powershell
docker run --rm -p 10000:10000 whisper-app
```

Open `http://localhost:10000` in your browser.

To use the command-line script instead, mount the folder and explicitly select the Python entrypoint:

```powershell
docker run --rm -it -v "${PWD}:/app" --entrypoint python whisper-app audio_to_text.py sample-0.mp3 -o transcript.txt -m small -l en
```

Replace the example path with your audio file. The file extension does not need to be `.mp3`; FFmpeg determines the format from the input file.

## Run the web UI locally and expose it with ngrok

If you want to launch the Flask interface locally and share it through a public URL, use these commands from the project folder:

```powershell
python -m pip install -r requirements.txt
python ui_interface.py
```

In a second terminal window, start the tunnel:

```powershell
ngrok http 5000
```

This exposes your local app at an ngrok URL such as:

```text
https://<random-name>.ngrok-free.dev
```

Open that URL in your browser to use the AI transcription tool. If you see the ngrok warning page, click **Visit Site** to continue.

For quick testing from the terminal, you can also send the required request header:

```powershell
curl -H "ngrok-skip-browser-warning: true" https://<random-name>.ngrok-free.dev
```

## GitHub Actions

This project includes a workflow file at `.github/workflows/docker-transcribe.yml`.

To run it in GitHub Actions:

1. Push the repository to GitHub.
2. Open the repository in GitHub.
3. Go to the Actions tab.
4. Select `Whisper Docker Transcription`.
5. Click `Run workflow`.
6. Enter values such as:
   - `audio_file`: `sample-0.mp3`
   - `language`: `en`
   - `model`: `small`

The workflow runs the same script and uploads the generated `transcript.txt` as an artifact.

## Deploy the web UI

GitHub stores this project's code, but it does not run the Flask app. To get a persistent public URL, deploy the repository as a Docker web service on a host such as Render:

1. Push the latest changes to GitHub.
2. In Render, create a new **Web Service** and connect this repository.
3. Choose the Docker runtime and use the repository root as the Docker context. Render will use the root `Dockerfile`.
4. Deploy. Once the service is healthy, Render provides a public HTTPS URL for the upload UI.

The first deployment downloads the Whisper `base` model and may take several minutes. Transcription uses CPU and memory, so choose a host instance with enough resources. Anyone with the public URL can submit audio; avoid uploading sensitive recordings and monitor hosting usage and costs.

## Output

The transcription will be printed to the terminal and saved in `transcript.txt`.

## Notes

- `small` is a good CPU-friendly Whisper model for general use.
- Use `-l en` when the audio is in English.
- If the audio is noisy or includes music, Whisper may misinterpret the sound.
