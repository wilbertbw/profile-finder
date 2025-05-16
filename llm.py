from openai import OpenAI

client = OpenAI(
  api_key="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"
)

def call_LLM(prompt, profile):
  response = client.responses.create(
    model="gpt-4o-mini",
    input=[
      {"role": "user", "content": "Here is a person's profile: " + profile + "\n\n" + prompt}
    ]
  )

  return response.output_text