FROM python:3.11-slim

WORKDIR /app

# Install system dependency needed by Whisper for audio decoding
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

CMD ["sh", "-c", "exec gunicorn --workers 1 --timeout 1800 --bind 0.0.0.0:${PORT:-10000} ui_interface:app"]
