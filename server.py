from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

# Create FastAPI app
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

@mcp.tool()
async def hello_world() -> str:
    return "Hello, World!"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")

            if data.strip().lower() == "hello":
                reply = await hello_world()
            else:
                reply = f"Echo: {data}"

            await websocket.send_text(reply)

    except Exception as e:
        print(f"❌ Connection closed: {e}")
    finally:
        print("🔌 WebSocket connection terminated")