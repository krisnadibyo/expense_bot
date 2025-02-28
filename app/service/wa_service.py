import os
from dotenv import load_dotenv
from fastapi import Response
from fastapi.responses import JSONResponse
import httpx

from app.service.openai_service import generate_response

load_dotenv()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
RECIPIENT_WAID=os.getenv("RECIPIENT_WAID")
VERSION=os.getenv("VERSION")
VERIFY_TOKEN=os.getenv("VERIFY_TOKEN")

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
    
async def handle_message(data: dict):
  if data.get('object') != 'whatsapp_business_account':
    return {'success': False, 'message': 'Not a WhatsApp webhook'}
  
  incoming_message = []
  for entry in data.get("entry", []):
    for change in entry.get("changes", []):
      value = change.get("value")
      # Check for incoming messages from clients
      if 'messages' in value and value['messages']:
        for message in value['messages']:
          incoming_message.append({
            'from': message.get('from'),
            'message_id': message.get('id'),
            'timestamp': message.get('timestamp'),
            'content': message.get('text', {}).get('body') if message.get('type') == 'text' else None,
            'type': message.get('type')
          })
        message_str=incoming_message[0].get('content')
        response=generate_response(message_str)
        await send_message(response)

async def verify_webhook(mode: str, token: str, challenge: str):
  if mode == "subscribe" and token == VERIFY_TOKEN:
    return Response(content=challenge, media_type="text/plain")
  else:
    return JSONResponse(
      status_code=403,
      content={
        "error": "Forbidden",
        "message": await send_message("Unauthorized webhook verification attempt")
      }
    )