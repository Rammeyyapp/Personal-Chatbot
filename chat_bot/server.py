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
from typing import Dict, List, Any
import requests 
from datetime import datetime

# IMPORTS FOR EMAIL FUNCTIONALITY
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. Initialize FastAPI and MCP Server ---
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
# Initialize MCP serverx
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

# ====================================================================
# HELPER FUNCTION: Simulates looking up 3-letter station codes
# ====================================================================
def get_station_code(city_name: str) -> str:
    """Simple placeholder function to convert city names to 3-letter codes."""
    mapping = {
    "madurai": "MDU",
    "chennai": "MAS",
    "coimbatore": "CBE",
    "delhi": "NDLS",
    "mumbai": "CSTM", # Or another major station code
    # You can also use the codes directly if the user provides them
    "mdu": "MDU",
    "mas": "MAS" 
    }
    return mapping.get(city_name.lower().strip(), city_name.strip().upper())

# --- 2. Define the LinkedIn Posting Tool ---
@register_tool("post_linkedin")
async def post_linkedin(content: str) -> str:
# ... (rest of post_linkedin function remains unchanged)
    """
    Publishes a text post to a LinkedIn profile.
    Args:
    content: The text content of the post.
    """
    linkedin_user_id = os.getenv("LINKEDIN_USER_ID")
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")

    if not access_token or not linkedin_user_id:
        return "❌ Error: LinkedIn access token or user ID not found. Check .env file."

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

# --- 3. Define the Email Sending Tool ---
@register_tool("send_email")
async def send_email_tool(recipient: str, subject: str, body: str) -> str:
# ... (rest of send_email_tool function remains unchanged)
    """
    Sends an email to a specified recipient with a subject and body.
    Args:
    recipient: The email address of the person to receive the email.
    subject: The subject line of the email.
    body: The main content of the email.
    """
    # NOTE: You MUST set these environment variables in your .env file
    # for the email to work.
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return "❌ Error: Email credentials not found. Check SENDER_EMAIL/SENDER_PASSWORD in .env file."
    
    # Handle empty subject/body with defaults
    final_subject = subject.strip() if subject else "Message from your Chatbot Assistant"
    final_body = body.strip() if body else "This is a quick message sent via your chatbot assistant."
    
    try:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient
        message["Subject"] = final_subject 
        message.attach(MIMEText(final_body, "plain")) 

        # NOTE: SMTPLIB is a blocking library. We define a blocking function
        def blocking_send():
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, recipient, message.as_string())

        # and run it in a thread pool executor to keep FastAPI (async) responsive.
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, blocking_send)
        
        return f"✅ Email successfully sent to {recipient}."
    
    except smtplib.SMTPAuthenticationError:
        return "❌ Error: Failed to login. Check your SENDER_EMAIL and SENDER_PASSWORD (App Password required for Gmail)."
    except Exception as e:
        print(f"Error sending email: {e}")
        return f"❌ Failed to send email. Error: {str(e)}"

# --- 4. Define the Train Search Tool ---
@register_tool("search_trains")
async def search_trains(source_city: str, destination_city: str, date_of_journey: str) -> str:
# ... (rest of search_trains function remains unchanged)
    """
    Searches for available trains between two cities on a specific date.
    Args:
    source_city: The starting city name or 3-letter station code (e.g., 'Madurai' or 'MDU').
    destination_city: The destination city name or 3-letter station code (e.g., 'Chennai' or 'MAS').
    date_of_journey: The date of travel in YYYY-MM-DD format (e.g., '2025-10-03').
    """
    # 1. API Setup & Credentials
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")
    
    if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
        return "❌ Error: RAPIDAPI_KEY or RAPIDAPI_HOST environment variables not set. Please check your .env file."

    API_URL = f"https://{RAPIDAPI_HOST}/api/v3/trainBetweenStations" 
    
    # 2. Convert City Names to Station Codes and Validate Date
    source_code = get_station_code(source_city)
    destination_code = get_station_code(destination_city)
    
    try:
    # Validate date format (yyyy-mm-dd)
        datetime.strptime(date_of_journey, '%Y-%m-%d')
    except ValueError:
        return f"Error: Date format must be YYYY-MM-DD, received {date_of_journey}. Cannot proceed."
    
    # 3. Define Headers and Parameters
    headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    params = {
    "fromStationCode": source_code,
    "toStationCode": destination_code,
    "dateOfJourney": date_of_journey
    }

    # Define the blocking function to run in the executor
    def blocking_search():
    # Use requests.get (synchronous)
        return requests.get(API_URL, headers=headers, params=params, timeout=30)

    # 4. Make the Real API Request using the thread pool
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, blocking_search)
        response.raise_for_status() 
        data = response.json()
        
        # Check for API-specific success status and extract the data list
        train_data = data.get('data', [])
        
        if not data.get('status'):
            return f"Train API failed with message: {data.get('message', 'Unknown Error')}"

        if not train_data:
            return f"No trains found from {source_city} ({source_code}) to {destination_city} ({destination_code}) on {date_of_journey}. API message: {data.get('message', 'Success but no data')}"

        # 5. Format the result for the user
        result_lines = [f"🚆 Found {len(train_data)} trains from {source_city} to {destination_city} on {date_of_journey}:"]
        result_lines.append("---------------------------------------------------")

        # Loop through ALL results
        for i, train in enumerate(train_data): 
        # Use EXACT JSON keys from your successful response
            name = train.get('train_name', 'N/A')
            number = train.get('train_number', 'N/A')
            dep_time = train.get('from_std', 'N/A')
            arr_time = train.get('to_sta', 'N/A')
            duration = train.get('duration', 'N/A')
            # The class_type is a list, join it with commas for a neat display
            classes = ", ".join(train.get('class_type', []))
            
            result_lines.append(f"**{i+1}. {name} ({number})**")
            result_lines.append(f"   Dep: {dep_time}, Arr: {arr_time}")
            result_lines.append(f"   Duration: {duration}")
            result_lines.append(f"   Classes: {classes}")
            # Add a blank line between trains for readability
            result_lines.append("") 

        # Format as a pre-formatted block (using triple backticks) for neat display
        return "\n".join(result_lines)

    except requests.exceptions.HTTPError as e:
        # Handles 4xx or 5xx errors from the API endpoint
        return f"❌ Train API returned an error: {e.response.status_code}. Details: {e.response.text}"
    except requests.exceptions.RequestException as e:
        # Handles connection errors, timeouts
        return f"❌ Failed to connect to Train API. Network Error: {str(e)}"
    except Exception as e:
        return f"An unexpected internal error occurred: {str(e)}"

# --- 5. Define the Weather Tool ⭐ NEW TOOL ADDED ---
@register_tool("get_current_weather")
async def get_current_weather(city_name: str) -> str:
    """
    Fetches the current weather conditions for a specified city.
    Args:
    city_name: The name of the city for which to fetch the weather (e.g., 'Chennai' or 'London').
    """
    # NOTE: You MUST set the WEATHER_API_KEY in your .env file
    API_KEY = os.environ.get("WEATHER_API_KEY")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    if not API_KEY:
        return "❌ Error: Weather API Key not configured. Check WEATHER_API_KEY in .env file."

    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # Use Celsius
    }

    # Define the blocking function to run in the executor
    def blocking_weather_fetch():
        # Use requests.get (synchronous)
        return requests.get(BASE_URL, params=params, timeout=15)

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, blocking_weather_fetch)
        response.raise_for_status() 
        data = response.json()

        # Check for city not found error from the API
        if data.get("cod") == "404":
            return f"❌ City/Area '{city_name}' not found. Please try a different location."

        # Extract relevant weather details
        weather_info = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature_c": data.get("main", {}).get("temp"),
            "feels_like_c": data.get("main", {}).get("feels_like"),
            "humidity_percent": data.get("main", {}).get("humidity"),
            "condition": data.get("weather", [{}])[0].get("main"),
            "description": data.get("weather", [{}])[0].get("description").title(),
            "wind_speed_m_s": data.get("wind", {}).get("speed")
        }
        
        # Format the result for the user
        result = (
            f"☀️ **Current Weather in {weather_info['city']}, {weather_info['country']}**:\n"
            f"- **Condition**: {weather_info['description']} ({weather_info['condition']})\n"
            f"- **Temperature**: {weather_info['temperature_c']}°C (Feels like {weather_info['feels_like_c']}°C)\n"
            f"- **Humidity**: {weather_info['humidity_percent']}%\n"
            f"- **Wind Speed**: {weather_info['wind_speed_m_s']} m/s"
        )
        return result

    except requests.exceptions.HTTPError as e:
        return f"❌ Weather API returned an error: {e.response.status_code}. Details: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Failed to connect to Weather API. Network Error: {str(e)}"
    except Exception as e:
        return f"An unexpected internal error occurred: {str(e)}"

# --- 6. API Endpoints (No Changes to Logic) ---
@app.get("/tools")
async def get_tools() -> List[Dict[str, Any]]:
# ... (rest of get_tools function remains unchanged)
    tools_list = []
    
    for name, func in TOOLS_REGISTRY.items():
        sig = inspect.signature(func)
        docstring = inspect.getdoc(func) or ""
        
        description = docstring.strip().split("\nArgs:")[0].strip()
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            param_type = "string" 
            parameters["properties"][param_name] = {
                "type": param_type,
                "description": f"The content for the {param_name} parameter."
            }
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)

        tools_list.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })
    
    return tools_list

@app.post("/execute_tool")
async def execute_tool(request: Request):
# ... (rest of execute_tool function remains unchanged)
    try:
        request_body_bytes = await request.body()
        request_body_str = request_body_bytes.decode('utf-8')
        tool_call = json.loads(request_body_str)
        
        print(f"Received JSON tool call: {tool_call}")
        
        tool_name = tool_call.get("action")
        arguments = tool_call.get("arguments", {})

        tool_function = TOOLS_REGISTRY.get(tool_name)
        
        if tool_function:
            sig = inspect.signature(tool_function)
            
            if inspect.iscoroutinefunction(tool_function):
                tool_result = await tool_function(**arguments)
            else:
                tool_result = tool_function(**arguments)
            
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