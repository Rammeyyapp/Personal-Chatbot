from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp = FastMCP("my-personal-chatbot", app)

@mcp.tool()
async def post_linkedin(content: str) -> str:
    linkedin_user_id = os.getenv("LINKEDIN_USER_ID")
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

    if not access_token or not linkedin_user_id:
        return "❌ Error: LinkedIn access token or user ID not found."

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "author": f"urn:li:person:{linkedin_user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return f"✅ Successfully posted to LinkedIn. Post ID: {response.json().get('id', 'N/A')}"
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return f"❌ Failed to post to LinkedIn. HTTP Error: {e.response.status_code}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"❌ Failed to post to LinkedIn. Error: {e}"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")

            if data.startswith("post_linkedin:"):
                content = data.split(":", 1)[1].strip()
                print(f"Calling post_linkedin tool with content: '{content}'")
                reply = await post_linkedin(content)
            else:
                reply = f"Echo: {data}"

            await websocket.send_text(reply)

    except Exception as e:
        print(f"❌ Connection closed: {e}")
    finally:
        print("🔌 WebSocket connection terminated")

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)