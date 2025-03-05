# Skyy Compliment Module

Skyy is an AI-powered compliment generator that uses computer vision and speech recognition to give personalized compliments. The system watches and listens for the trigger phrase "Skyy, compliment me" and then, with permission, analyzes the user to generate contextual compliments.

## Features

- 🎤 Voice-activated trigger system
- 🔒 Privacy-first approach with explicit permission requests
- 👁️ Computer vision analysis for personalized compliments
- 🗣️ Natural speech output
- 🎨 Color and appearance analysis
- 😊 Emotion detection

## Prerequisites

- Python 3.8+
- Webcam
- Microphone
- Speaker/Audio output

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ChrisVivasAI/skyy_compliment.git
    cd skyy_compliment
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv skyy
    # On Windows:
    skyy\Scripts\activate
    # On Unix or MacOS:
    source skyy/bin/activate
    ```

3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Activate your virtual environment:
    ```bash
    # On Windows:
    skyy\Scripts\activate
    # On Unix or MacOS:
    source skyy/bin/activate
    ```

2. Run the main script:
    ```bash
    python main.py
    ```

3. Wait for initialization, then say "Skyy, compliment me"
4. Grant permission when asked
5. Receive your personalized compliment!

## How It Works

1. **Speech Recognition**: Continuously listens for the trigger phrase "Skyy, compliment me"
2. **Permission System**: Asks for explicit permission before using the camera
3. **Visual Analysis**: 
   - Face detection
   - Emotion recognition
   - Color analysis
4. **Compliment Generation**: Uses analyzed features to generate contextual compliments
5. **Speech Synthesis**: Delivers the compliment through text-to-speech

## Privacy Considerations

- Camera access is requested explicitly each time
- No images or audio are stored
- All processing is done locally
- Users can deny camera access and still receive generic compliments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for computer vision capabilities
- Speech Recognition for voice interface
- PyTTSx3 for text-to-speech functionality

## Contact

- Creator: Chris Vivas
- GitHub: [@ChrisVivasAI](https://github.com/ChrisVivasAI)
