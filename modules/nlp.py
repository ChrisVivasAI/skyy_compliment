import random
from transformers import pipeline

class ComplimentGenerator:
    def __init__(self, use_transformer=True):
        self.use_transformer = use_transformer
        
        # Initialize the transformer-based text generation if enabled
        if use_transformer:
            try:
                self.generator = pipeline('text-generation', model='gpt2')
            except:
                print("Warning: Transformer model not available. Falling back to rule-based approach.")
                self.use_transformer = False
        
        # Define compliment templates for rule-based generation
        self.templates = {
            # Smile-based compliments
            "smile": [
                "Your smile lights up the room!",
                "You have such a warm and inviting smile.",
                "The way you smile is truly wonderful."
            ],
            # Eyes-based compliments
            "eyes": [
                "Your eyes have such a captivating spark.",
                "The kindness in your eyes is inspiring.",
                "Your eyes reflect such a thoughtful soul."
            ],
            # Color-based compliments (for clothing)
            "colors": {
                "red": "That shade of red really brings out your confidence!",
                "blue": "That blue color complements you perfectly.",
                "green": "That green looks absolutely stunning on you.",
                "yellow": "That yellow adds such a cheerful vibe to your look!",
                "purple": "That purple gives you such a regal presence.",
                "black": "Your style is so elegant and sophisticated.",
                "white": "You look so fresh and polished!",
                # Add more colors as needed
            },
            # Emotion-based compliments
            "emotion": {
                "happy": "Your positivity is contagious!",
                "neutral": "You have such a composed and confident presence.",
                "surprise": "Your expressive nature makes conversations with you so engaging!",
                "sad": "Your thoughtful demeanor shows such emotional depth.",
                # Add more emotions as needed
            },
            # Generic compliments (fallback)
            "generic": [
                "You have an amazing presence.",
                "You seem like someone who really makes a difference.",
                "You bring such valuable energy to any space you're in.",
                "Your uniqueness is truly refreshing.",
                "You have an admirable way of carrying yourself."
            ]
        }
    
    def generate_compliment(self, visual_features):
        """Generate a personalized compliment based on visual features"""
        if not visual_features or "error" in visual_features:
            # Fallback if vision analysis failed
            return random.choice(self.templates["generic"])
        
        if self.use_transformer:
            return self._generate_with_transformer(visual_features)
        else:
            return self._generate_with_rules(visual_features)
    
    def _generate_with_rules(self, features):
        """Rule-based compliment generation using templates"""
        compliments = []
        
        # Add a smile-based compliment if face was detected
        if features.get("face_detected", False):
            compliments.append(random.choice(self.templates["smile"]))
        
        # Add a color-based compliment if colors were detected
        if "colors" in features and features["colors"]:
            for color in features["colors"]:
                if color in self.templates["colors"]:
                    compliments.append(self.templates["colors"][color])
                    break
        
        # Add an emotion-based compliment
        if "emotion" in features and features["emotion"]:
            emotion = features["emotion"]
            if emotion in self.templates["emotion"]:
                compliments.append(self.templates["emotion"][emotion])
        
        # Add eyes compliment
        compliments.append(random.choice(self.templates["eyes"]))
        
        # If no specific compliments were added, use a generic one
        if not compliments:
            compliments.append(random.choice(self.templates["generic"]))
        
        # Return a randomly selected compliment from the candidate list
        return random.choice(compliments)
    
    def _generate_with_transformer(self, features):
        """Generate a compliment using a transformer model with visual features as context"""
        # Create a prompt based on features
        prompt = "Give a kind compliment to someone who "
        
        if features.get("emotion"):
            prompt += f"appears {features['emotion']}, "
        
        if features.get("colors"):
            color_text = ", ".join(features["colors"])
            prompt += f"is wearing {color_text}, "
            
        # Complete the prompt
        prompt += "and deserves to feel appreciated:"
        
        # Generate text
        try:
            result = self.generator(prompt, max_length=50, num_return_sequences=1)
            generated_text = result[0]['generated_text']
            
            # Extract just the compliment part (after the prompt)
            compliment = generated_text.replace(prompt, "").strip()
            
            # If the compliment is empty or too short, fall back to rule-based
            if len(compliment) < 20:
                return self._generate_with_rules(features)
                
            return compliment
        except Exception as e:
            print(f"Error in transformer-based generation: {e}")
            return self._generate_with_rules(features) 