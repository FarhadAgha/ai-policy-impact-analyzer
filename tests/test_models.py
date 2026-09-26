import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"Key loaded: {api_key[:10]}..." if api_key else "No key found!")

client = Groq(api_key=api_key)

models = client.models.list()
print("\nModels available to this key:")
for m in models.data:
    print(f"  - {m.id}")