import openai
import base64
import os
import csv
from dotenv import load_dotenv
from datetime import datetime

# Load your API key from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Log result to CSV
def log_to_csv(image_path, response_text):
    with open("vision_log.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().isoformat(), image_path, response_text])
    print("Logged to vision_log.csv")

# Ask GPT-4o about the image
def ask_gpt_about_image(image_path, question="Is this trashcan full?"):
    image_base64 = image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful maintenance robot assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}
        ],
        max_tokens=100
    )

    reply = response.choices[0].message.content
    print("\nGPT-4o Response:", reply)
    log_to_csv(image_path, reply)
    return reply


if __name__ == "__main__":
    image_path = "test_images/trashcan01.jpg"
    if not os.path.exists(image_path):
        print("Image not found. Place a test image at:", image_path)
    else:
        ask_gpt_about_image(image_path)
