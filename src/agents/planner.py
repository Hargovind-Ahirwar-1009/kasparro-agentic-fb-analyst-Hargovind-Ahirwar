import os
from src.utils.logger import setup_logger

logger = setup_logger("planner_agent")

class PlannerAgent:
    def __init__(self, llm_client):
        self.llm = llm_client

    def _load_prompt(self, filename):
        with open(os.path.join("prompts", filename), "r") as f:
            return f.read()

    def create_plan(self, user_query):
        logger.info(f"Planning for query: {user_query}")
        
        template = self._load_prompt("planner_prompt.md")
        prompt = template.format(user_query=user_query)
        
        return self.llm.generate(prompt, json_mode=True)