import os
from src.utils.logger import setup_logger

logger = setup_logger("creative_agent")

class CreativeAgent:
    def __init__(self, llm_client):
        self.llm = llm_client

    def _load_prompt(self, filename):
        with open(os.path.join("prompts", filename), "r") as f:
            return f.read()

    def improve_creatives(self, low_performing_ads):
        if not low_performing_ads:
            return {"message": "No low performing ads found."}

        logger.info(f"Generating copy for {len(low_performing_ads)} ads")
        
        template = self._load_prompt("creative_prompt.md")
        prompt = template.format(low_performing_ads=low_performing_ads)
        
        return self.llm.generate(prompt, json_mode=True)