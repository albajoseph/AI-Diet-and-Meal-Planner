from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# --- Imports ---
from models import (
    InventoryInput, InventoryResponse,
    DietInput, DietResponse,
    AskInput, ManagerResponse,
    PlanInput, RecipeResponse,
    RecommendInput, RecommendResponse
)
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent
from agents.manager_agent import ManagerAgent
from agents.planner_agent import PlannerAgent

# Import the logger
from logger_config import get_logger

# Load environment variables
load_dotenv()

# Initialize Logger
logger = get_logger("ai_planner")

app = FastAPI(title="AI Diet & Meal Planner")

# Initialize Agents
inventory_agent = InventoryAgent()
diet_agent = DietAgent()
manager_agent = ManagerAgent()
planner_agent = PlannerAgent()


@app.get("/")
def health_check():
    return {"message": "Success!"}


@app.post("/inventory", response_model=InventoryResponse)
def check_inventory(input_data: InventoryInput):
    return inventory_agent.run(input_data.items)


@app.post("/diet", response_model=DietResponse)
def filter_diet(input_data: DietInput):
    return diet_agent.run(input_data.items, input_data.diet)


# --- Updated Endpoints with Logging ---

@app.post("/ask", response_model=ManagerResponse)
def ask_manager(input_data: AskInput):
    logger.info(f"Received /ask request: items={input_data.items}, diet={input_data.diet}")
    try:
        result = manager_agent.run(input_data.items, input_data.diet)

        # Log the suggestions count or content
        logger.info(f"/ask response: generated {len(result.suggestions)} suggestions")
        return result
    except Exception as e:
        logger.error(f"Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan", response_model=RecipeResponse)
def generate_plan(input_data: PlanInput):
    logger.info(f"Received /plan request: base_recipe='{input_data.base_recipe}'")
    try:
        result = planner_agent.run(input_data.base_recipe)

        logger.info(f"/plan response: generated title='{result.title}'")
        return result
    except Exception as e:
        logger.error(f"Error in /plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommend", response_model=RecommendResponse)
def recommend_recipes(input_data: RecommendInput):
    logger.info(
        f"Received /recommend request: items={input_data.items}, diet={input_data.diet}, count={input_data.recipe_count}")
    try:
        # 1. Manager Step
        manager_result = manager_agent.run(input_data.items, input_data.diet)
        ideas = manager_result.suggestions[:input_data.recipe_count]

        # 2. Planner Step
        full_recipes = []
        for idea in ideas:
            recipe = planner_agent.run(idea)
            full_recipes.append(recipe)

        logger.info(f"/recommend response: returning {len(full_recipes)} full recipes")
        return RecommendResponse(recipes=full_recipes)

    except Exception as e:
        logger.error(f"Error in /recommend: {e}")
        raise HTTPException(status_code=500, detail=str(e))