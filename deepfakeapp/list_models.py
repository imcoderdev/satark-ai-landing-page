"""List available models using the Google Generative AI library"""
import google.generativeai as genai
import os

# Configure API
GEMINI_API_KEY = "AIzaSyBU4ls0_sslkyKRGHNJXzntEyx68PEPeGA"
genai.configure(api_key=GEMINI_API_KEY)

print("Available models:\n")
try:
    for model in genai.list_models():
        print(f"  • {model.name}")
        if 'flash' in model.name.lower():
            print(f"    ↳ FLASH MODEL FOUND!")
except Exception as e:
    print(f"Error: {e}")
