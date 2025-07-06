import httpx
import os
import asyncio

GROUPME_BOT_ID = os.getenv("BOT_ID")
TOKEN = os.getenv("TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
BASE_URL = os.getenv("BASE_URL")

first_message = "Good Evening! Please like this message if you can pick up late plates today!"

def second_message(user: str):
    return f'Thank you to {user} for volunteering!\nEveryone else, please like this message if you need a late plate picked up!'

async def sendFirstMessage(text: str = first_message) -> str:
    url = f"{BASE_URL}/bots/post"
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
    
async def sendSecondMessage(text: str):
    url = f"{BASE_URL}/bots/post"
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    async with httpx.AsyncClient() as client: 
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            print(f'Failed to send second message: {response.text}')
            return None
        await asyncio.sleep(1)

        print(f"Second message successfully sent: {response.text}")
        return None

async def getLatestBotMessageId(text: str) -> str:
    url = f"{BASE_URL}/groups/{GROUP_ID}/messages?token={os.getenv('TOKEN')}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"limit": 5})
        messages = response.json().get("response", {}).get("messages", [])
        for message in messages:
            if message.get("text") == text and message.get("sender_type") == "bot":
                return message.get("id")
        return None
    
async def waitForFirstLike(message_id: str):
    url = f"{BASE_URL}/groups/{GROUP_ID}/messages/{message_id}?token={TOKEN}"
    while True:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch message: {response.text}")
                return None
            data = response.json().get("response", "message")
            liked_by = data.get("favorited_by", [])
            print("Python type of liked by: ", str(type(liked_by)))

            # Assuming its a list of strings
            if len(liked_by) > 0:
                user_id = liked_by[0]
                users = await getAllUsersInGroup()
                return getUserNameById(user_id, users)
        await asyncio.sleep(10)

def getUserNameById(user_id: str, users: list) -> str:
    for user in users:
        if user["id"] == user_id:
            return user["name"]
    return None
    
async def getAllUsersInGroup() -> list:
    url = f'{BASE_URL}/groups/{GROUP_ID}?token={TOKEN}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print("Failed to fetch group details")
            return None
        group_data = response.json().get("response", {})
        group_users = group_data.get("members", [])
        return [{"id": user.get("user_id"), "name": user.get("nickname")} for user in group_users]
    
async def messageFlow():
    first_message_id = await sendFirstMessage()
    first_like_uname = await waitForFirstLike(first_message_id)
    if first_like_uname:
        second_message = second_message(first_like_uname)
        sendSecondMessage(second_message)

def main():
    print("Starting process")
    asyncio.run(messageFlow())

if __name__ == "__main__":
    main()