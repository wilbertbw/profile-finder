from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

def call_LLM(prompt, profile):
  response = client.responses.create(
    model="gpt-4o-mini",
    input=[
      {"role": "user", "content": "Here is a person's profile: " + profile + "\n\n" + prompt}
    ]
  )

  return response.output_text