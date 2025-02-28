import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_MODEL=os.getenv("OPENAI_MODEL")
client=OpenAI(api_key=OPENAI_API_KEY)

def generate_response(message: str) -> str:
  response = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
      {"role": "system", "content": 
       """
       You are a personal finance assistant that helps users manage their finances. You will be given a list of expenses and you will need to calculate the total expenses per category. return the result in json format.
       Your only given list of category is:
       food, transport, entertainment, education, health, other
       the example of the json format is:
       {
         "food": 100000,
         "transport": 200000,
         "entertainment": 300000
       }
       """},
      {"role": "user", "content": message}
    ],
    temperature=0.5,
  )
  return response.choices[0].message.content
