# Skyy Compliment Module (Ollama Enhanced)

Skyy is an AI-powered compliment generator designed for Miami Dade College (MDC). It uses local AI models via Ollama for multimodal visual description and context-aware compliment generation, combined with speech recognition and synthesis.

## Features

- 🎤 Voice-activated trigger system ("Skyy, compliment me")
- 🔒 Privacy-first approach with explicit permission requests
- 👁️ **AI-powered visual description** using a local multimodal model (via Ollama)
- 🧠 **Context-aware compliment generation** tailored for MDC students using a local language model (via Ollama)
- 🗣️ Natural speech output for compliments and interactions
- 🏫 Designed with the MDC environment in mind

## Prerequisites

- Python 3.8+
- **Ollama installed and running:** [https://ollama.com/](https://ollama.com/)
- **Required Ollama Model:** A multimodal model capable of image description and text generation (e.g., `gemma3:4b` if it's multimodal in your setup, or alternatives like `llava`). You need to pull the model:
  ```bash
  # Example if using llava
  # ollama pull llava
  # Example if your gemma3:4b is multimodal
  ollama pull gemma3:4b
  ```
- Webcam
- Microphone
- Speaker/Audio output

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ChrisVivasAI/skyy_compliment.git
    cd skyy_compliment
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv skyy
    # On Windows:
    skyy\Scripts\activate
    # On Unix or MacOS:
    source skyy/bin/activate
    ```

3.  Install required packages (including `ollama`):
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

- **Ollama Model Name:** The application currently defaults to using `"gemma3:4b"` for both vision description and text generation. You can change this default model name directly in `modules/vision.py` and `modules/nlp.py` if you are using a different Ollama model (like `llava`).

## Usage

1.  **Ensure Ollama is running** in the background with the required model available.
2.  Activate your virtual environment:
    ```bash
    # On Windows:
    skyy\Scripts\activate
    # On Unix or MacOS:
    source skyy/bin/activate
    ```
3.  Run the main script:
    ```bash
    python main.py
    ```
4.  Wait for initialization (Camera, Ollama checks).
5.  Say "Skyy, compliment me".
6.  Grant permission when asked ("yes" or "no").
7.  Skyy will capture an image, send it to Ollama for description, use that description to ask Ollama for a compliment, and then speak the result.

## Project Structure

```
skyy_compliment/
├── main.py                 # Main application entry point
├── modules/
│   ├── __init__.py
│   ├── vision.py          # Image capture & AI description (Ollama)
│   ├── speech.py          # Speech recognition & synthesis
│   ├── nlp.py             # AI Compliment Generation (Ollama)
│   └── permission.py      # Permission handling
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## How It Works

1.  **Speech Recognition**: Listens for the "Skyy, compliment me" trigger.
2.  **Permission System**: Asks for user permission to use the camera.
3.  **Image Capture**: Captures a single frame from the webcam (`vision.py`).
4.  **AI Visual Description**: Sends the captured image to the configured multimodal Ollama model to get a text description of the person (`vision.py`).
5.  **AI Compliment Generation**: Takes the text description and sends it to the configured Ollama language model with a specialized prompt asking for a positive, appropriate compliment for an MDC student (`nlp.py`).
6.  **Speech Synthesis**: Speaks the generated compliment or any necessary interactions (`speech.py`).

## Privacy Considerations

- Camera access is requested explicitly each time.
- Images are processed locally via Ollama and not stored persistently by the application after processing. Base64 encoded images are sent to the local Ollama instance.
- Audio processing is done via the `speech_recognition` library (potentially using Google's service for the default recognition) and local TTS.
- Users can deny camera access, and the system will respond appropriately (currently falls back to generic spoken message, no compliment generated).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Ollama Team & Community:** For enabling local LLM execution.
- **Model Creators:** (Google for Gemma, or creators of LLaVA)
- OpenCV: For camera interaction.
- SpeechRecognition & PyTTSx3: For the voice interface.

## Contact

- Creator: Chris Vivas & Kevin Zagoya
- GitHub: [@ChrisVivasAI](https://github.com/ChrisVivasAI)