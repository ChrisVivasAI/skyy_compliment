import cv2
import numpy as np
import os

# Force CPU usage and reduce memory consumption
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class VisionAnalyzer:
    def __init__(self):
        print("Initializing VisionAnalyzer...", flush=True)
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if self.face_cascade.empty():
                raise Exception("Error loading face cascade classifier")
            self.camera = None
            print("Face detection model loaded successfully", flush=True)
            
        except Exception as e:
            print(f"Error during VisionAnalyzer initialization: {str(e)}", flush=True)
            raise
    
    def initialize_camera(self):
        """Initialize camera with error handling"""
        print("Initializing camera...", flush=True)
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("Could not access camera")
            print("Camera initialized successfully", flush=True)
            return self.camera
        except Exception as e:
            print(f"Camera initialization error: {str(e)}", flush=True)
            raise
    
    def capture_and_analyze(self):
        """Capture image and extract visual features for compliment generation"""
        try:
            # Initialize camera if not already done
            if not self.camera:
                self.initialize_camera()
            
            # Capture frame
            print("Capturing image...", flush=True)
            ret, frame = self.camera.read()
            if not ret:
                raise Exception("Failed to capture image")
            
            # Analyze using multiple approaches
            features = {}
            
            # Basic face detection
            print("Detecting face...", flush=True)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                features["face_detected"] = True
                x, y, w, h = faces[0]  # Use the first face detected
                face_img = frame[y:y+h, x:x+w]
                
                # Simple smile detection using Haar cascade
                smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
                smiles = smile_cascade.detectMultiScale(gray[y:y+h, x:x+w], 1.7, 20)
                features["emotion"] = "happy" if len(smiles) > 0 else "neutral"
                
                # Basic color analysis
                try:
                    non_face = frame.copy()
                    cv2.rectangle(non_face, (x, y), (x+w, y+h), (0, 0, 0), -1)
                    colors = self._analyze_colors(non_face)
                    features["colors"] = colors
                except Exception as e:
                    print(f"Color analysis error: {str(e)}", flush=True)
                    features["colors"] = []
            else:
                features["face_detected"] = False
                print("No face detected in image", flush=True)
            
            return features
            
        except Exception as e:
            print(f"Error during image capture and analysis: {str(e)}", flush=True)
            return {"error": str(e)}
    
    def _analyze_colors(self, image):
        """Extract dominant colors from image using a simpler approach"""
        try:
            # Reduce image size for faster processing
            small = cv2.resize(image, (32, 32))
            pixels = small.reshape(-1, 3)
            
            # Calculate average color
            avg_color = np.mean(pixels, axis=0)
            b, g, r = avg_color.astype(int)
            
            # Simple color classification
            colors = []
            if r > 150 and g < 100 and b < 100:
                colors.append("red")
            elif r > 150 and g > 150 and b < 100:
                colors.append("yellow")
            elif r < 100 and g > 150 and b < 100:
                colors.append("green")
            elif r > 150 and g > 150 and b > 150:
                colors.append("white")
            elif r < 100 and g < 100 and b < 100:
                colors.append("black")
            elif abs(r - g) < 30 and abs(g - b) < 30:
                colors.append("neutral")
            
            return colors
            
        except Exception as e:
            print(f"Color analysis error: {str(e)}", flush=True)
            return []
    
    def __del__(self):
        """Cleanup resources"""
        if self.camera:
            self.camera.release() 