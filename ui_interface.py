import os
from os.path import splitext

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, render_template_string, request
import whisper
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the Whisper speech recognition model once when the application starts
model = whisper.load_model("base")


@app.route("/")
def index():
        return render_template_string("""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Audio to Text</title>
    <style>
        :root { color-scheme: light; font-family: Georgia, "Times New Roman", serif; }
        * { box-sizing: border-box; }
        body {
            min-height: 100vh;
            margin: 0;
            color: #182b28;
            background-color: #f3f2e9;
            background-image: radial-gradient(#c9d0c2 0.7px, transparent 0.7px);
            background-size: 18px 18px;
        }
        main { width: min(760px, calc(100% - 32px)); margin: 0 auto; padding: 64px 0; }
        .eyebrow, label, select, button, #status, .result-heading { font-family: Arial, sans-serif; }
        .eyebrow { color: #b0442f; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; }
        h1 { margin: 12px 0 8px; font-size: clamp(38px, 8vw, 64px); font-weight: 500; line-height: 1; }
        .intro { margin: 0 0 32px; color: #53625d; font-size: 18px; }
        form, .result { padding: 24px; border: 1px solid #cbd1c7; background: #fbfaf5; }
        label { display: block; margin-bottom: 9px; font-size: 13px; font-weight: 700; }
        input[type="file"], select { width: 100%; min-height: 46px; padding: 10px; border: 1px solid #aebbb2; background: #fff; color: #182b28; }
        .controls { display: grid; grid-template-columns: 1fr 180px; gap: 18px; align-items: end; }
        button { min-height: 46px; padding: 0 18px; border: 0; background: #b0442f; color: #fff; font-size: 14px; font-weight: 700; cursor: pointer; }
        button:hover { background: #873523; }
        button:disabled { opacity: 0.6; cursor: wait; }
        #status { min-height: 22px; margin: 14px 0 0; color: #53625d; font-size: 14px; }
        .result { margin-top: 20px; }
        .result-heading { display: flex; justify-content: space-between; gap: 16px; align-items: center; }
        .result-heading h2 { margin: 0; font-size: 14px; }
        .result-heading button { min-height: 36px; padding: 0 12px; background: #315b50; }
        pre { margin: 18px 0 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 16px/1.6 Georgia, "Times New Roman", serif; }
        [hidden] { display: none !important; }
        @media (max-width: 560px) {
            main { padding: 38px 0; }
            .controls { grid-template-columns: 1fr; }
            form, .result { padding: 18px; }
        }
    </style>
</head>
<body>
    <main>
        <div class="eyebrow">Speech / TRANSCRIPTION</div>
        <h1>Audio to text</h1>
        <p class="intro">Choose an audio recording in any format supported by FFmpeg and get its transcript.</p>
        <form id="transcription-form">
            <div class="controls">
                <div>
                    <label for="audio">Audio file</label>
                    <input id="audio" name="audio" type="file" required>
                </div>
                <div>
                    <label for="language">Language</label>
                    <select id="language" name="language">
                        <option value="">Detect automatically</option>
                        <option value="en">English</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="hi">Hindi</option>
                    </select>
                </div>
            </div>
            <button id="submit" type="submit" style="margin-top: 20px">Transcribe audio</button>
            <p id="status" role="status" aria-live="polite"></p>
        </form>
        <section id="result-panel" class="result" hidden>
            <div class="result-heading">
                <h2>Transcript</h2>
                <button id="copy" type="button">Copy text</button>
            </div>
            <pre id="transcript"></pre>
        </section>
    </main>
    <script>
        const form = document.querySelector("#transcription-form");
        const submit = document.querySelector("#submit");
        const status = document.querySelector("#status");
        const panel = document.querySelector("#result-panel");
        const transcript = document.querySelector("#transcript");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            submit.disabled = true;
            status.textContent = "Transcribing audio...";
            panel.hidden = true;
            try {
                const response = await fetch("/transcribe", { method: "POST", body: new FormData(form) });
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || "Transcription failed.");
                transcript.textContent = data.transcription;
                panel.hidden = false;
                status.textContent = "Transcription complete.";
            } catch (error) {
                status.textContent = error.message;
            } finally {
                submit.disabled = false;
            }
        });

        document.querySelector("#copy").addEventListener("click", async () => {
            await navigator.clipboard.writeText(transcript.textContent);
            status.textContent = "Transcript copied.";
        });
    </script>
</body>
</html>
""")


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    audio_file = request.files.get("audio")
    if audio_file is None or not audio_file.filename:
        return {"error": "Choose an audio file to transcribe."}, 400

    temp_path = None
    safe_filename = secure_filename(audio_file.filename)
    suffix = splitext(safe_filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp_path = temp.name
        audio_file.save(temp.name)

    try:
        language = request.form.get("language")
        options = {"language": language} if language else {}
        result = model.transcribe(temp_path, **options)
        return {"transcription": result["text"]}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug=True, use_reloader=False)
