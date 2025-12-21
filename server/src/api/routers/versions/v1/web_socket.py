# ws.py
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
import json

router = APIRouter()
connections: Dict[str, Set[WebSocket]] = {}

async def broadcast(room: str, payload: dict):
    dead = []
    for web_socket in connections.get(room, set()):
        if web_socket.application_state != WebSocketState.CONNECTED:
            dead.append(web_socket)
            continue
        await web_socket.send_text(json.dumps(payload))
    for web_socket in dead:
        connections[room].discard(web_socket)

@router.websocket("/web-socket/tickets/{room}")
async def tickets_web_socket(websocket: WebSocket, room: str):
    await websocket.accept()
    connections.setdefault(room, set()).add(websocket)
    try:
        while True:
            await websocket.receive_text()  # opcional: escuchar pings/mensajes del cliente
    except WebSocketDisconnect:
        connections[room].discard(websocket)

# Ejemplo de uso en tu lógica cuando cambia un ticket:
# await broadcast(room=str(ticket_id), payload={"type": "updated", "ticketId": str(ticket_id), "status": new_status})
# o por grupo/usuario: room = f"user:{assignee_id}"
