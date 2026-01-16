import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables (api key)
load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def call_model_json(self, prompt: str) -> Dict[str, Any]:
        """
        Sends a prompt to Groq and expects a JSON response.
        """
        if not self.api_key:
            raise ValueError("LLM_API_KEY is not set in the .env file")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            # This forces the LLM to output valid JSON
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise error for 4xx/5xx status codes

            data = response.json()
            content_str = data["choices"][0]["message"]["content"]

            # Parse string content into a Python dictionary
            return json.loads(content_str)

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return {}