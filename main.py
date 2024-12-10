from rcs import (
    Action,
    Card,
    InboundActionMessage,
    InboundLocationMessage,
    InboundMediaMessage,
    InboundTextMessage,
    Pinnacle,
    SendRcsResponse,
)
from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

load_dotenv()

KEY: str | None = os.getenv("PINNACLE_API_KEY")
if not KEY:
    raise ValueError("No key provided")

client = Pinnacle(api_key=KEY)

app = FastAPI()


@app.post("/")
async def root(request: Request):
    # Parse the incoming JSON payload
    data = await request.json()
    print(data)
    
    message_id = data.get("messageId")
    status = data.get("status")
    
    # Collect status updates - https://docs.trypinnacle.app/api-reference/receive-msg-statuses#receive-message-statuses
    print(f"Message {message_id} status updated to: {status}")
    
    return {"status": "success"}


@app.get("/send")
async def send_message():
    response = client.send.rcs(
        to="+16287261512",
        from_="test",
        text="Did you get this?",
        status_callback="https://ghost-related-humbly.ngrok-free.app",
    )
    return {"status": "message sent", "response": response}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
