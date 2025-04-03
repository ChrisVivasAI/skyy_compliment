import cv2
# import numpy as np # No longer directly needed
import os
import ollama
import base64
import io
import traceback
# import re # No longer needed for parsing here

# Force CPU usage and reduce memory consumption
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Ensure Ollama library is available (should be from previous steps)

class VisionAnalyzer:
    def __init__(self, model_name="gemma3:4b"):
        """Initializes the VisionAnalyzer using a local multimodal Ollama model."""
        self.model_name = model_name
        self.camera = None
        print(f"VisionAnalyzer initialized to use Ollama model: {self.model_name} for image description.", flush=True)

    def initialize_camera(self):
        """Initialize camera with error handling"""
        print("Initializing camera...", flush=True)
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("Could not access camera")
            # Allow camera to warm up
            for _ in range(5):
                 self.camera.read()
            print("Camera initialized successfully", flush=True)
            return self.camera
        except Exception as e:
            print(f"Camera initialization error: {str(e)}", flush=True)
            raise

    def _encode_image_to_base64(self, frame):
        """Encodes a cv2 frame (numpy array) into base64 string."""
        try:
            # Encode the frame to PNG format in memory
            is_success, buffer = cv2.imencode(".png", frame)
            if not is_success:
                 raise ValueError("Could not encode image to PNG format")
            # Convert buffer to bytes
            image_bytes = buffer.tobytes()
            # Encode bytes to base64 string
            base64_string = base64.b64encode(image_bytes).decode('utf-8')
            return base64_string
        except Exception as e:
            print(f"Error encoding image: {e}", flush=True)
            return None

    def _create_vision_prompt(self):
        """Creates the prompt for the multimodal model to describe the person."""
        # Changed prompt to ask for description instead of structured features
        prompt = """Analyze the attached image of a person, likely a student. Provide a brief, objective description focusing on their general appearance, expression, and any notable clothing or items. Example: 'A student with short dark hair smiling slightly, wearing a blue hoodie and glasses.'"""
        return prompt

    def capture_and_analyze(self):
        """Capture image and get a description using the multimodal Ollama model."""
        analysis_result = {"description": None, "error": None} # Standardized return format
        try:
            if not self.camera or not self.camera.isOpened():
                self.initialize_camera()

            print("Capturing image for description...", flush=True)
            ret, frame = self.camera.read()
            if not ret or frame is None:
                raise Exception("Failed to capture valid image frame")

            base64_image = self._encode_image_to_base64(frame)
            if not base64_image:
                raise Exception("Failed to encode image")

            prompt = self._create_vision_prompt()

            print(f"Sending image and description prompt to Ollama model: {self.model_name}...", flush=True)
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [base64_image]
                    }
                ]
            )

            if response and 'message' in response and 'content' in response['message']:
                description = response['message']['content'].strip()
                print(f"Received description from Ollama:\n---\n{description}\n---", flush=True)
                analysis_result["description"] = description
                return analysis_result # Return description successfully
            else:
                 raise Exception("Invalid response format from Ollama (Vision)")

        except Exception as e:
            error_message = f"Error during image description: {str(e)}"
            print(error_message, flush=True)
            print(traceback.format_exc(), flush=True)
            analysis_result["error"] = error_message
            return analysis_result # Return error state

    def __del__(self):
        """Cleanup resources"""
        if self.camera and self.camera.isOpened():
            self.camera.release()
            print("Camera released.", flush=True)

    # Removed OpenCV cascade loading and _analyze_colors method 