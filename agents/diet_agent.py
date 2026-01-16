import json
from models import DietResponse
from services.llm_client import LLMClient
from typing import List


class DietAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: List[str], diet: str) -> DietResponse:
        prompt = (
            f"You are a diet expert. User has these ingredients: {json.dumps(items)}.\n"
            f"Dietary restriction: {diet}.\n"
            "Return a JSON object with:\n"
            "  compatible_items: List of ingredients from the input that fit the diet.\n"
            "  suggested_recipe_ideas: List of exactly 5 recipe names based on compatible items.\n"
            "Respond ONLY with valid JSON."
        )

        response_dict = self.llm.call_model_json(prompt)

        # Validate and return using Pydantic
        return DietResponse(**response_dict)