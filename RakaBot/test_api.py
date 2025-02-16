import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_huggingface_connection():
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": "Hello!"}
        )
        if response.status_code == 200:
            print("✅ HuggingFace API connection successful!")
            print(f"Response: {response.json()[0]['generated_text']}")
        else:
            print(f"❌ API Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    test_huggingface_connection()