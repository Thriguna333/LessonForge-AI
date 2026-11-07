
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Get API key locally from .env or from Streamlit Cloud Secrets
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        API_KEY = None

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Configure it in .env or Streamlit Secrets."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAMES = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash"
]


def generate_response(prompt: str) -> str:
    """Generate a response with automatic model fallback."""

    errors = []

    for model_name in MODEL_NAMES:
        try:
            print(f"Trying model: {model_name}")

            response = client.interactions.create(
                model=model_name,
                input=prompt
            )

            if not response.output_text:
                raise ValueError("Gemini returned an empty response.")

            print(f"Success using: {model_name}")
            return response.output_text

        except Exception as error:
            print(f"{model_name} failed: {error}")
            errors.append(f"{model_name}: {error}")

    raise RuntimeError(
        "All Gemini models failed:\n" + "\n".join(errors)
    )
