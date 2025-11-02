import asyncio
import websockets

SERVER_URL = "ws://localhost:8000/ws"  # WebSocket endpoint

async def main():
    while True:  # Reconnect loop
        try:
            async with websockets.connect(SERVER_URL) as websocket:
                print("✅ Connected to MCP Server")

                while True:
                    msg = input("You: ").strip()
                    if not msg:
                        continue

                    await websocket.send(msg)
                    reply = await websocket.recv()
                    print(f"Server: {reply}")

        except websockets.exceptions.ConnectionClosed as e:
            print(f"⚠ Connection lost: {e}. Reconnecting in 3s...")
            await asyncio.sleep(3)  # Wait before retry
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(3)  # Wait before retry

if _name_ == "_main_":
    asyncio.run(main())