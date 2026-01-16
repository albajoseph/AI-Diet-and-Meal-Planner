import json
from models import RecipeResponse
from services.llm_client import LLMClient


class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, base_recipe: str) -> RecipeResponse:
        # Construct a prompt that enforces the specific JSON structure
        prompt = (
            f"Create a detailed cooking recipe for: {base_recipe}.\n"
            "Return a JSON object with:\n"
            "  title: string name of the dish\n"
            "  ingredients: list of strings (quantities included)\n"
            "  steps: list of objects, where each object has exactly two keys: "
            "'step_number' (integer) and 'instruction' (string).\n"
            "Respond ONLY with valid JSON."
        )

        response_dict = self.llm.call_model_json(prompt)

        return RecipeResponse(**response_dict)