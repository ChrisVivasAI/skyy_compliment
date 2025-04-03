import random
import ollama
import traceback

class ComplimentGenerator:
    def __init__(self, model_name="gemma3:4b"):
        """Initializes the ComplimentGenerator using a local Ollama text model."""
        self.model_name = model_name
        print(f"ComplimentGenerator initialized to use Ollama model: {self.model_name} for text generation.", flush=True)
        self.generic_compliments = [
            "Your dedication is clear, keep up the great work at MDC!",
            "You bring a positive energy to the campus!",
            "It's great to see students like you engaged and present!",
            "Your potential is shining bright!",
            "Keep pushing forward with your studies, you're doing great!"
        ]

    def _create_compliment_prompt(self, description):
        """Creates a prompt for the Ollama text model based on the image description."""
        # New prompt incorporating description and MDC context
        prompt = f"""You are Skyy, a friendly AI assistant at Miami Dade College (MDC). Your task is to generate a short, positive, encouraging, and appropriate compliment for an MDC student based *only* on the following visual description obtained from an image.

Visual Description of Student:
"{description}"

Instructions:
- Generate a single, kind compliment inspired by the description.
- Keep it concise (1-2 sentences).
- Focus on positive attributes like energy, focus, style (respectfully), or perceived effort.
- Ensure the compliment is appropriate and respectful for a college environment. Avoid overly personal or potentially awkward comments.
- If the description is vague or unhelpful, provide a general encouraging compliment suitable for an MDC student.
- Do NOT repeat the description in your compliment.

Appropriate Compliment:"""
        return prompt

    def generate_compliment(self, analysis_result):
        """Generate a personalized compliment using the description from the vision module."""
        
        # Extract description, handle potential errors from vision module
        description = None
        if analysis_result and isinstance(analysis_result, dict):
            if analysis_result.get("error"):
                 print(f"Vision module reported an error: {analysis_result['error']}. Using generic compliment.", flush=True)
            else:
                 description = analysis_result.get("description")
        
        if not description:
             print("No valid description received from vision module. Using generic compliment.", flush=True)
             return random.choice(self.generic_compliments)

        # Create the prompt for the text model
        prompt = self._create_compliment_prompt(description)
        print(f"Generated Compliment Prompt for Ollama:\n---\n{prompt}\n---", flush=True)

        try:
            print(f"Sending request to Ollama text model: {self.model_name}...", flush=True)
            # Using the same model, but now for text generation based on description
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )

            if response and 'message' in response and 'content' in response['message']:
                compliment = response['message']['content'].strip()
                print(f"Received compliment from Ollama: {compliment}", flush=True)

                # Basic safety/quality check
                if len(compliment) < 5 or "sorry" in compliment.lower() or "cannot" in compliment.lower() or description.lower() in compliment.lower(): # Added check to avoid echoing description
                     print("Ollama response unsatisfactory or echoed description, falling back to generic compliment.", flush=True)
                     return random.choice(self.generic_compliments)

                # Clean up potential markdown quotes or prefix
                compliment = compliment.replace("Appropriate Compliment:", "").replace("*","").replace('"','').strip()
                # Ensure it ends reasonably (e.g., with punctuation)
                if compliment and compliment[-1].isalnum():
                     compliment += "."
                
                # Return the processed compliment if everything is okay
                return compliment
            
            else:
                 print("Ollama response format invalid (NLP), falling back to generic compliment.", flush=True)
                 return random.choice(self.generic_compliments)

        except Exception as e:
            print(f"Error during Ollama text generation: {str(e)}", flush=True)
            print(traceback.format_exc(), flush=True)
            print("Falling back to generic compliment.", flush=True)
            return random.choice(self.generic_compliments)

    # Removed _generate_with_rules, _generate_with_transformer, and self.templates 