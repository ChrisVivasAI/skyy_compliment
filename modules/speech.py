import speech_recognition as sr
import pyttsx3
import difflib

class SpeechProcessor:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        # Set properties (optional)
        self.engine.setProperty('rate', 175)  # Speed
        self.engine.setProperty('volume', 0.9)  # Volume
        
        # Adjust for ambient noise when initializing
        with self.microphone as source:
            print("Adjusting for ambient noise...", flush=True)
            self.recognizer.adjust_for_ambient_noise(source)
        
    def listen_for_trigger(self, trigger_phrase):
        """Listen for the trigger phrase with fuzzy matching"""
        try:
            with self.microphone as source:
                print("Listening for trigger phrase...", flush=True)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}", flush=True)
                
                # Use fuzzy string matching to be more lenient with the trigger phrase
                similarity = difflib.SequenceMatcher(None, text, trigger_phrase.lower()).ratio()
                if similarity > 0.8:  # 80% similarity threshold
                    print("Trigger phrase detected!", flush=True)
                    return True
                    
                # Also check if the words are present, even if not exact
                trigger_words = set(trigger_phrase.lower().split())
                heard_words = set(text.split())
                if len(trigger_words.intersection(heard_words)) >= len(trigger_words) - 1:
                    print("Trigger phrase detected!", flush=True)
                    return True
                    
                return False
                
            except sr.UnknownValueError:
                print("Error in speech recognition: ", flush=True)
                return False
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service: {str(e)}", flush=True)
                return False
                
        except sr.WaitTimeoutError:
            print("Error in speech recognition: listening timed out while waiting for phrase to start", flush=True)
            return False
    
    def listen(self):
        """Listen for any speech and return the recognized text"""
        try:
            with self.microphone as source:
                print("Listening...", flush=True)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Heard: {text}", flush=True)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio", flush=True)
                return None
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service: {str(e)}", flush=True)
                return None
                
        except sr.WaitTimeoutError:
            print("Listening timed out", flush=True)
            return None
    
    def speak(self, text):
        """Speak the given text"""
        print(f"Speaking: {text}", flush=True)
        self.engine.say(text)
        self.engine.runAndWait() 