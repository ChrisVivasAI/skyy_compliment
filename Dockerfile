FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for OpenCV, PyAudio (SpeechRecognition/PyTTSx3),
# and potentially other libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    # For audio input/output
    portaudio19-dev \
    # python3-pyaudio might not be needed if installed via pip, but keep portaudio dev files
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Ensure ollama is listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# --- Ollama Configuration ---
# Set the default host for the Ollama server.
# 'host.docker.internal' works on Docker Desktop (Windows/Mac) to reach the host.
# On Linux, you might need to override this at runtime, e.g.,
# docker run -e OLLAMA_HOST='http://<host_ip>:11434' ... your_image
# Or use --network="host" (less secure).
ENV OLLAMA_HOST="http://host.docker.internal:11434"

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "main.py"] 