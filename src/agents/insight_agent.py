import os
from src.utils.logger import setup_logger

logger = setup_logger("insight_agent")

class InsightAgent:
    def __init__(self, llm_client):
        self.llm = llm_client

    def _load_prompt(self, filename):
        with open(os.path.join("prompts", filename), "r") as f:
            return f.read()

    def generate_insights(self, data_summary):
        logger.info("Generating insights from data...")
        
        template = self._load_prompt("insight_prompt.md")
        trends_str = str(data_summary.get('trends', []))
        prompt = template.format(data_trends=trends_str)
        
        return self.llm.generate(prompt, json_mode=True)