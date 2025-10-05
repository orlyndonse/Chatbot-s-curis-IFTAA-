import google.generativeai as genai
from src.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

print("Modèles disponibles pour generateContent:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")