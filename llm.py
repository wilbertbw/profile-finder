from google import genai

client = genai.Client(api_key = "AIzaSyC3E9e_BjrYH2NojxLuugDpFD8JDAy5CDs")

def call_LLM(prompt, profile):
  query = "Here is a person's profile: " + profile + "\n\n" + prompt
  
  response = client.models.generate_content(model = "gemini-2.0-flash", contents = query)

  return response.text