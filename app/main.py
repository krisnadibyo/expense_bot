import os
from dotenv import load_dotenv
from fastapi import FastAPI
import httpx
import uvicorn
from app.schemas.message import RequestMessage


load_dotenv()

app= FastAPI()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
RECIPIENT_WAID=os.getenv("RECIPIENT_WAID")
VERSION=os.getenv("VERSION")

@app.get("/")
def index():
    return {"message": "Hello World"}

async def send_message(message: str):
  url=f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
  headers={
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
  }
  data={
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "type": "text",
    "to": RECIPIENT_WAID,
    "text": {
      "body": message
    }
  }
  async with httpx.AsyncClient() as client:
    response=await client.post(url, headers=headers, json=data)
    if response.status_code==200:
      return response.json()
    else:
      return {"message": "Failed to send message"}

@app.post("/send-message")
async def send_message_route(data: RequestMessage):
  return await send_message(data.message)
