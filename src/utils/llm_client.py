import os
import json
from groq import Groq
from dotenv import load_dotenv
from src.utils.logger import setup_logger

load_dotenv()
logger = setup_logger("llm_client")

class LLMClient:
    def __init__(self, model="llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
            
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt, system_prompt="You are a helpful AI assistant.", json_mode=False):
        try:
            logger.info(f"Sending request to Groq ({self.model}) | JSON Mode: {json_mode}")
            
            # Groq requires explicit 'json_object' type for JSON mode
            response_format = {"type": "json_object"} if json_mode else {"type": "text"}
            
            # Llama 3 instruction tuning requires we mention JSON in the text prompt too
            if json_mode and "json" not in system_prompt.lower():
                system_prompt += " Respond ONLY in valid JSON."

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1, # Keep it factual, not creative
                response_format=response_format
            )

            content = chat_completion.choices[0].message.content
            
            if json_mode:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON. Raw content: {content}")
                    return {"error": "Invalid JSON returned by Groq"}
            
            return content

        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            return None