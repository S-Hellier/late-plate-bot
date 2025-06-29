import httpx
import os

GROUPME_BOT_ID = os.getenv("BOT_ID")  # You should set this in .env or environment

async def sendGroupMeMessage(text: str):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 202:
            print(f"Failed to send message: {response.text}")
        return response
