from fastapi import APIRouter,WebSocket,Request,WebSocketDisconnect
from util import template
import uuid

websocket_app = APIRouter(prefix="/chat")


@websocket_app.get("/")
async def chattemplate(request: Request):
    return template.TemplateResponse("chat.html",{"request":request})

@websocket_app.websocket("/")
async def chatapp(websocket:WebSocket):
    await websocket.accept() 
    while True:
        try:
            client_data = await websocket.receive_text()
            await websocket.send_text(f"broadcast from server {client_data}")
        except WebSocketDisconnect:
            print("client left the chat..")
            break