from typing import List
from models import ManagerResponse
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent

class ManagerAgent:
    def __init__(self):
        # Initialize the sub-agents
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, items: List[str], diet: str) -> ManagerResponse:
        # 1. ORCHESTRATION STEP: Validation
        # Pass raw items to Inventory Agent
        inventory_result = self.inventory_agent.run(items)
        cleaned_items = inventory_result.usable_items

        # 2. ORCHESTRATION STEP: Logic
        # Pass the CLEANED items to Diet Agent
        diet_result = self.diet_agent.run(cleaned_items, diet)

        # 3. ORCHESTRATION STEP: Response Construction
        # Map the results to the ManagerResponse structure
        return ManagerResponse(
            usable_items=cleaned_items,
            diet_filtered=diet_result.compatible_items,
            suggestions=diet_result.suggested_recipe_ideas
        )