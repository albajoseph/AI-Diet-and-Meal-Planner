from pydantic import BaseModel
from typing import List

# --- Input Models ---
class InventoryInput(BaseModel):
    items: List[str]

class DietInput(BaseModel):
    items: List[str]
    diet: str

# --- Output Models ---
class InventoryResponse(BaseModel):
    usable_items: List[str]
    message: str

class DietResponse(BaseModel):
    compatible_items: List[str]
    suggested_recipe_ideas: List[str]

# --- New Models for Stage 3 ---

class AskInput(BaseModel):
    items: List[str]
    diet: str

class ManagerResponse(BaseModel):
    usable_items: List[str]
    diet_filtered: List[str]
    suggestions: List[str]

# --- New Models for Stage 4 ---

class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class RecipeResponse(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[RecipeStep]

class PlanInput(BaseModel):
    base_recipe: str

class RecommendInput(BaseModel):
    items: List[str]
    diet: str
    recipe_count: int = 2  # Default to 2 if not provided

class RecommendResponse(BaseModel):
    recipes: List[RecipeResponse]