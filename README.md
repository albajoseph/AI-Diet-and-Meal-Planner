# AI Diet & Meal Planner 🥗🤖

A multi-agent AI application built with **FastAPI** that helps users plan meals based on ingredients they already have. It utilizes specialized AI agents to filter inventory, apply dietary restrictions (Vegan, Keto, etc.), and generate detailed, step-by-step cooking recipes using Groq's Llama 3 LLM.

## 🚀 Features

* **Intelligent Inventory Management:** The `InventoryAgent` filters user input to identify valid, usable cooking ingredients.
* **Dietary Customization:** The `DietAgent` filters ingredients based on specific dietary needs (e.g., Vegan, Gluten-Free, Keto).
* **Smart Orchestration:** A `ManagerAgent` coordinates the workflow, seamlessly passing data between inventory checks and dietary filtering.
* **Generative Recipe Planning:** The `PlannerAgent` generates complete, step-by-step recipes with precise ingredient lists.
* **Production Ready:** Includes structured logging and is fully containerized with **Docker** for easy deployment.

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python 3.12)
* **AI/LLM:** Groq API (Llama-3.1-8b-instant)
* **Architecture:** Multi-Agent System (Inventory, Diet, Manager, Planner)
* **Deployment:** Docker, Uvicorn

## 📂 Project Structure

```text
.
├── agents/                 # specialized AI agents
│   ├── inventory_agent.py  # cleans/validates ingredients
│   ├── diet_agent.py       # checks dietary rules
│   ├── manager_agent.py    # orchestrates the workflow
│   └── planner_agent.py    # generates full recipes
├── services/
│   └── llm_client.py       # handles Groq API communication
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic data models
├── logger_config.py        # Centralized logging configuration
├── Dockerfile              # Container configuration
└── .env                    # API keys (not committed)

```

## ⚡ Getting Started

### Prerequisites

* Python 3.12+
* A [Groq Cloud](https://console.groq.com) API Key

### 1. Installation

Clone the repository:

```bash
git clone https://github.com/albajoseph/ai-diet-meal-planner.git
cd ai-diet-meal-planner

```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows (Git Bash)
pip install fastapi uvicorn requests python-dotenv

```

### 2. Configuration

Create a `.env` file in the root directory and add your Groq API key:

```env
LLM_API_KEY=gsk_your_actual_key_here

```

### 3. Running the App

**Using Python:**

```bash
uvicorn main:app --reload

```

**Using Docker:**

```bash
docker build -t ai-diet-planner .
docker run -p 8000:8000 -e LLM_API_KEY=your_key_here ai-diet-planner

```

## 📡 API Endpoints

Once running, access the interactive docs at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/inventory` | Cleans a list of raw ingredients. |
| `POST` | `/diet` | Filters ingredients by diet and suggests ideas. |
| `POST` | `/ask` | **Orchestrator:** Combines inventory & diet checks. |
| `POST` | `/plan` | Generates a full recipe from a dish name. |
| `POST` | `/recommend` | **Full Flow:** Takes ingredients -> returns full recipes. |

## 🧪 Example Usage

**Request (`/recommend`):**

```json
{
  "items": ["tofu", "bell pepper", "soy sauce"],
  "diet": "vegan",
  "recipe_count": 1
}

```

**Response:**

```json
{
  "recipes": [
    {
      "title": "Vegan Tofu Stir-Fry",
      "ingredients": ["tofu", "bell pepper", "soy sauce"],
      "steps": [
        { "step_number": 1, "instruction": "Press tofu and cut into cubes." },
        { "step_number": 2, "instruction": "Stir fry tofu until golden..." }
      ]
    }
  ]
}

```
