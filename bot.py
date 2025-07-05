import httpx
import os
import asyncio

GROUPME_BOT_ID = os.getenv("BOT_ID")
TOKEN = os.getenv("TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

message = "Good Evening! Please like this message if you can pick up late plates today!"

def second_message(user: str):
    return f'Thank you to {user} for volunteering!\nEveryone else, please like this message if you need a late plate picked up!'

async def sendGroupMeMessage(text: str = message) -> str:
    url = f"https://api.groupme.com/v3/bots/post?token={os.getenv('TOKEN')}"
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code != 202:
            print(f"Failed to send message: {response.text}")
            return None
        await asyncio.sleep(1)
    
        return await getLatestBotMessageId(text)

async def getLatestBotMessageId(text: str) -> str:
    url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages?token={os.getenv('TOKEN')}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"limit": 5})
        messages = response.json().get("response", {}).get("messages", [])
        for message in messages:
            if message.get("text") == text and message.get("sender_type") == "bot":
                return message.get("id")
        return None
    
async def waitForFirstLike(message_id: str):
    url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages/{message_id}?token={TOKEN}"
    seen_likes = set()
    while True:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch message: {response.text}")
                return None
            data = response.json().get("response", {})
            liked_by = data.get("favorited_by", [])
            new_likes = [uid for uid in liked_by if uid not in seen_likes]
            if new_likes:
                user_id = new_likes[0]
                user_name = await getUserNameById(user_id)
                await sendGroupMeMessage("")
                return
        await asyncio.sleep(5)

async def getUserNameById(user_id: str) -> str:
    url = f"https://api.groupme.com/v3/users/{user_id}?token={TOKEN}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch user: {response.text}")
            return None
        user_data = response.json().get("response", {})
        return user_data.get("name", "Unknown User")