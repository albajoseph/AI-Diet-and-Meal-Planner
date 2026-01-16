import json
import requests
from hstest import StageTest, CheckResult, dynamic_test

class FastAPIStageTest(StageTest):
    BASE_URL = "http://localhost:8000"

    @dynamic_test(time_limit=120_000)
    def test_root(self):
        try:
            response = requests.get(f"{self.BASE_URL}/")
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")
        
        if "Success" not in response_data.get("message", ""):
            return CheckResult.wrong(f"Expected 'Success' in the 'message' value, but got {response_data.get('message', '')}.")

        return CheckResult.correct()

    @dynamic_test(time_limit=120_000)
    def test_ask(self):
        payload = {
            "items": ["tomato", "chicken breast", "spinach", ""],
            "diet": "vegan"
        }

        try:
            response = requests.post(f"{self.BASE_URL}/ask", json=payload)
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            body = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")

        if "usable_items" not in body:
            return CheckResult.wrong("'usable_items' key is missing in response.")
        if "diet_filtered" not in body:
            return CheckResult.wrong("'diet_filtered' key is missing in response.")
        if "suggestions" not in body:
            return CheckResult.wrong("'suggestions' key is missing in response.")
        if not isinstance(body.get("suggestions"), list):
            return CheckResult.wrong("'suggestions' should be a list.")

        return CheckResult.correct()

    @dynamic_test(time_limit=120_000)
    def test_plan(self):
        payload = {"base_recipe": "Vegan Salad"}
        
        try:
            response = requests.post(f"{self.BASE_URL}/plan", json=payload)
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            body = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")

        if "title" not in body:
            return CheckResult.wrong("'title' key is missing in response.")
        if "ingredients" not in body or not isinstance(body["ingredients"], list):
            return CheckResult.wrong("'ingredients' key is missing or is not a list.")
        if "steps" not in body or not isinstance(body["steps"], list):
            return CheckResult.wrong("'steps' key is missing or is not a list.")

        return CheckResult.correct()

    @dynamic_test(time_limit=120_000)
    def test_recommend(self):
        payload = {
            "items": ["egg", "flour", "sugar", "milk"],
            "diet": "vegetarian",
            "recipe_count": 2
        }

        try:
            response = requests.post(f"{self.BASE_URL}/recommend", json=payload)
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Cannot connect to the server at 'http://localhost:8000'. Ensure the FastAPI app is running.")

        if response.status_code != 200:
            return CheckResult.wrong(f"Expected status code 200, but got {response.status_code}.")

        try:
            body = response.json()
        except json.JSONDecodeError:
            return CheckResult.wrong("Response is not valid JSON.")

        if "recipes" not in body or not isinstance(body["recipes"], list):
            return CheckResult.wrong("'recipes' key is missing or is not a list.")
        if len(body["recipes"]) != 2:
            return CheckResult.wrong("Expected 2 recipes in the response but got a different number.")

        first = body["recipes"][0]
        if "title" not in first:
            return CheckResult.wrong("First recipe is missing 'title'.")
        if "ingredients" not in first:
            return CheckResult.wrong("First recipe is missing 'ingredients'.")
        if "steps" not in first:
            return CheckResult.wrong("First recipe is missing 'steps'.")

        return CheckResult.correct()