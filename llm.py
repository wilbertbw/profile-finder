from openai import OpenAI
from google import genai
from groq import Groq
import os
import time
import json
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

  responses = []

  final_prompt = prompt.strip()
  if prompt.strip() == "":
    final_prompt = file.read()
  
  for profile in profiles:
    query = "Here is a profile:\n" + profile + "\n\n" + final_prompt
  
    response = geminiClient.models.generate_content(model = "gemini-2.0-flash", contents = query)

    response_text = response.text

    if (response.text[:8].strip() == "```json") and (response.text[-4:].strip() == "```"):
      response_text = response.text[8:-4].strip()
    elif (response.text[:8].strip() == "```json"):
      response_text = response_text[8:].strip()
    elif (response.text[-4:].strip() == "```"):
      response_text = response_text[:-4].strip()

    if (type(json.loads(response_text)) == type([])):
      response_dict = json.loads(response_text)[0]
    else:
      response_dict = json.loads(response_text)

    responses.append(response_dict)

    time.sleep(4)

  file.close()

  return responses

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