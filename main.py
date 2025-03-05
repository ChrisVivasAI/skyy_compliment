import argparse
import sys
import traceback
import os

# Force TensorFlow to use CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# Reduce TensorFlow logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from modules.vision import VisionAnalyzer
from modules.speech import SpeechProcessor
from modules.nlp import ComplimentGenerator
from modules.permission import PermissionHandler

# Enable immediate output flushing
print("Initializing application...", flush=True)

class ComplimentModule:
    def __init__(self):
        print("Creating VisionAnalyzer...", flush=True)
        self.vision = VisionAnalyzer()
        print("Creating SpeechProcessor...", flush=True)
        self.speech = SpeechProcessor()
        print("Creating ComplimentGenerator...", flush=True)
        self.nlp = ComplimentGenerator()
        print("Creating PermissionHandler...", flush=True)
        self.permission = PermissionHandler()
        print("All modules initialized.", flush=True)
        
    def process_request(self):
        # 1. Listen for trigger phrase
        print("Listening for trigger phrase...", flush=True)
        request = self.speech.listen_for_trigger("Skyy, compliment me")
        if not request:
            return False
            
        # 2. Ask for and verify permission
        if not self.permission.request_permission():
            self.speech.speak("I need your permission to observe you for a moment to give a personalized compliment.")
            return False
            
        # 3. Capture and analyze visual data
        visual_features = self.vision.capture_and_analyze()
        
        # 4. Generate personalized compliment
        compliment = self.nlp.generate_compliment(visual_features)
        
        # 5. Deliver the compliment
        self.speech.speak(compliment)
        return True

if __name__ == "__main__":
    try:
        print("Starting Compliment Module...", flush=True)
        compliment_module = ComplimentModule()
        print("Initialized successfully!", flush=True)
        
        while True:
            try:
                print("\nListening for 'Skyy, compliment me'...", flush=True)
                result = compliment_module.process_request()
                if not result:
                    print("No valid trigger phrase detected, trying again...", flush=True)
            except KeyboardInterrupt:
                print("\nExiting program...", flush=True)
                break
            except Exception as e:
                print(f"Error during processing: {str(e)}", flush=True)
                traceback.print_exc()
    except Exception as e:
        print(f"Error during initialization: {str(e)}", flush=True)
        traceback.print_exc()
        sys.exit(1) 