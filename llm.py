from openai import OpenAI
from google import genai
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

openaiClient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

geminiClient = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

groqClient = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_openai(prompt, profiles):
  file = open("default-prompt.txt")

  final_prompt = prompt.strip()
  if prompt.strip() == "":
    final_prompt = file.read()
  
  response = openaiClient.responses.create(
    model="gpt-4o-mini",
    input=[
      {"role": "user", "content": "Here are several profiles in an array: " + profiles + "\n\n" + final_prompt}
    ]
  )

  file.close()

  return response.output_text

def call_gemini(prompt, profiles):
  file = open("default-prompt.txt")

  final_prompt = prompt.strip()
  if prompt.strip() == "":
    final_prompt = file.read()

  query = "Here are several profiles in an array: " + profiles + "\n\n" + final_prompt
  
  response = geminiClient.models.generate_content(model = "gemini-2.0-flash", contents = query)

  file.close()

  return response.text

def call_groq(prompt, profiles):
  file = open("default-prompt.txt")

  final_prompt = prompt.strip()
  if prompt.strip() == "":
    final_prompt = file.read()
  
  query = "Here are several profiles in an array: " + profiles + "\n\n" + final_prompt

  chat_completion = groqClient.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": query,
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
  )

  file.close()
  
  return chat_completion.choices[0].message.content