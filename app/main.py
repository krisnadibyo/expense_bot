
from fastapi import FastAPI, Request
from app.schemas.message import RequestMessage
from app.service.openai_service import generate_response
from app.service.wa_service import handle_message, send_message, verify_webhook

app= FastAPI()

@app.get("/webhooks")
async def webhooks(request: Request):
  return await verify_webhook(request)
  
@app.post("/webhooks")
async def webhooks(request: Request):
  data=await request.json()
  await handle_message(data)
  return {"message": "Webhooks Received"}

