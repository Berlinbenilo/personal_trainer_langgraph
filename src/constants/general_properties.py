import os
from dotenv import load_dotenv

load_dotenv()

model_config = {"openai": {
    'temperature': 0,
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-4o-mini"
}}

model_provider = "openai"

workout_types = ["Upper Body Strength", "Lower Body Strength", "Active Recovery (Cardio/Yoga)", "Full Body Strength", "Rest"]
