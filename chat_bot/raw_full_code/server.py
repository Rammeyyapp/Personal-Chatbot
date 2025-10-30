from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
import httpx
import os
import asyncio
import ollama

# --- 1. Initialize FastAPI and MCP Server ---
app = FastAPI()

# Allow all origins for development (remove/modify for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp = FastMCP("my-personal-chatbot", app)

# --- 2. Define the LinkedIn Posting Tool ---
@mcp.tool()
async def post_linkedin(content: str) -> str:
    """
    Publishes a text post to a LinkedIn profile.
    Args:
        content: The text content of the post.
    """
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
    
    # Corrected payload that works with the LinkedIn API
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

# --- 3. The WebSocket Endpoint with Ollama Integration ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")

            # Define the tool for Ollama to use
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "post_linkedin",
                        "description": "Publishes a text post to a LinkedIn profile.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "The text content of the post to be published on LinkedIn.",
                                }
                            },
                            "required": ["content"],
                        },
                    },
                }
            ]

            # Use asyncio.to_thread to run the synchronous ollama.chat call
            response = await asyncio.to_thread(
                ollama.chat,
                model='qwen2:7b-instruct',
                messages=[
                    {
                        'role': 'system', 
                        'content': 'You are a helpful assistant with access to a tool for posting to LinkedIn. When a user asks you to post content on their behalf, you MUST use the `post_linkedin` tool to perform this action. You do not need to confirm with the user before using the tool. Just call the tool with the content provided by the user.'
                    },
                    {'role': 'user', 'content': data}
                ],
                tools=tools,
                options={
                    "temperature": 0.0
                }
            )

            # This is where the LLM's decision is handled
            # --- FIX: Changed this line to correctly check for the tool call ---
            if response['message'].get('tool_calls'):
                tool_call = response['message']['tool_calls'][0]['function']
                tool_name = tool_call['name']
                tool_args = tool_call['arguments']
                
                print(f"Calling tool: {tool_name} with arguments: {tool_args}")
                
                if tool_name == "post_linkedin":
                    reply = await post_linkedin(content=tool_args["content"])
                    await websocket.send_text(reply)
                else:
                    await websocket.send_text("❌ Error: Ollama called an unknown tool.")
            else:
                reply = response["message"]["content"]
                print(f"Model response (no tool call): {reply}")
                await websocket.send_text(reply)

    except Exception as e:
        print(f"❌ Connection closed: {e}")
    finally:
        print("🔌 WebSocket connection terminated")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)