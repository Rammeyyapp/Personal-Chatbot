from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
import httpx
import os
import asyncio
import json
import inspect

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

# Our custom tool registry to map tool names to function objects
TOOLS_REGISTRY = {}

def register_tool(tool_name: str):
    """A custom decorator to both register with MCP and our local registry."""
    def decorator(func):
        # First, apply the original mcp.tool decorator
        mcp.tool()(func)
        # Then, register the function in our own dictionary
        TOOLS_REGISTRY[tool_name] = func
        return func
    return decorator

# --- 2. Define the LinkedIn Posting Tool ---
@register_tool("post_linkedin")
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

# --- 3. Dynamic Tool Execution Endpoint ---
@app.post("/execute_tool")
async def execute_tool(request: Request):
    """
    Receives a JSON tool call from the client and dynamically executes the corresponding tool.
    This endpoint uses our centralized registry to look up and run the tool function.
    """
    try:
        request_body_bytes = await request.body()
        request_body_str = request_body_bytes.decode('utf-8')
        tool_call = json.loads(request_body_str)
        
        print(f"Received JSON tool call: {tool_call}")
        
        tool_name = tool_call.get("action")
        arguments = tool_call.get("arguments", {})

        # Dynamically get the tool function from our custom registry
        tool_function = TOOLS_REGISTRY.get(tool_name)
        
        if tool_function:
            # Check if arguments match the function's signature for robustness
            sig = inspect.signature(tool_function)
            
            missing_args = [param for param in sig.parameters if param not in arguments]
            if missing_args:
                raise HTTPException(status_code=400, detail=f"Missing required arguments for '{tool_name}': {', '.join(missing_args)}")

            tool_result = await tool_function(**arguments)
            return {"result": tool_result}
        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found.")
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in request body.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)