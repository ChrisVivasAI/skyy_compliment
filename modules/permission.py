class PermissionHandler:
    def __init__(self, speech_processor=None):
        # Use the provided speech processor or create a new one
        if speech_processor:
            self.speech = speech_processor
        else:
            from .speech import SpeechProcessor
            self.speech = SpeechProcessor()
        
    def request_permission(self):
        """Request permission to analyze visual data for a compliment"""
        self.speech.speak("To give you a personalized compliment, I'll need to take a quick look at you. Is that okay? Please say yes or no.")
        
        # Listen for response
        response = self.speech.listen()
        
        if not response:
            self.speech.speak("I didn't hear your response. For privacy reasons, I won't proceed with the visual analysis.")
            return False
            
        # Check for affirmative response
        response = response.lower()
        if "yes" in response or "sure" in response or "okay" in response or "ok" in response:
            self.speech.speak("Thank you! Just a moment while I observe.")
            return True
        else:
            self.speech.speak("No problem. I respect your privacy and won't use the camera.")
            return False 