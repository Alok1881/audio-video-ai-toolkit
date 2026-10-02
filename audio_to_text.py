import argparse
import os

# Work around OpenMP runtime clashes on some Windows setups
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Whisper invokes ffmpeg as a subprocess for MP3/WAV decoding.
# Add the WinGet FFmpeg install location to PATH so it can be found.
ffmpeg_dir = r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
if os.path.isdir(ffmpeg_dir):
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

import whisper


def transcribe_audio(input_file, output_file, model_name="small", language=None):
    model = whisper.load_model(model_name)

    kwargs = {
        "fp16": False,
        "temperature": 0,
        "beam_size": 5,
        "condition_on_previous_text": False,
        "verbose": False,
    }
    if language:
        kwargs["language"] = language

    result = model.transcribe(input_file, **kwargs)
    transcript = result["text"].strip()

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(transcript + "\n")

    print(transcript)
    return transcript


def main():
    parser = argparse.ArgumentParser(description="Transcribe an audio file with Whisper.")
    parser.add_argument("input_file", nargs="?", default="sample-0.mp3", help="Path to the input audio file.")
    parser.add_argument("-o", "--output", default="transcript.txt", help="Path to the output transcript file.")
    parser.add_argument("-m", "--model", default="small", help="Whisper model to use: tiny, base, small, medium, large.")
    parser.add_argument("-l", "--language", default=None, help="Language code (for example: en, fr, es).")
    args = parser.parse_args()

    transcribe_audio(args.input_file, args.output, model_name=args.model, language=args.language)


if __name__ == "__main__":
    main()
