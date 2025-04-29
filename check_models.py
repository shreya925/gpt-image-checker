import openai
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models = client.models.list()

print("\n🔍 Available models for your API key:")
for m in models.data:
    print("-", m.id)
