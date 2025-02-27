import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from app.schemas.message import RequestMessage


load_dotenv()

app= FastAPI()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
RECIPIENT_WAID=os.getenv("RECIPIENT_WAID")
VERSION=os.getenv("VERSION")
VERIFY_TOKEN=os.getenv("VERIFY_TOKEN")

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

@app.get("/webhooks")
async def webhooks(request: Request):
  print(request.query_params)
  mode = request.query_params.get("hub.mode")
  token = request.query_params.get("hub.verify_token")
  challenge = request.query_params.get("hub.challenge")
  if mode == "subscribe" and token == VERIFY_TOKEN:
    logging.info("WEBHOOK_VERIFIED")
    return Response(content=challenge, media_type="text/plain")
  else:
    return JSONResponse(
      status_code=403,
      content={
        "error": "Forbidden",
        "message": await send_message("Unauthorized webhook verification attempt")
      }
    )
@app.post("/webhooks")
async def webhooks(request: Request):
  data=await request.json()
  print(data)
  return {"message": "Webhooks Received"}
