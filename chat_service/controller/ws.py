from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from config.db import get_db
from config.cache import get_redis
from service.chat_service import ChatService
from repository.presence_repository import PresenceRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis
import json

router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id: str) -> None:
        self.active.pop(user_id, None)

    async def send_to_user(self, user_id: str, message: str) -> None:
        ws = self.active.get(user_id)
        if ws is not None:
            await ws.send_text(message)


manager = ConnectionManager()


def get_service() -> ChatService:
    db: AsyncIOMotorDatabase = get_db()
    redis_client: Redis = get_redis()
    presence = PresenceRepository(redis_client)
    return ChatService(db, presence)


@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket, user_id: str = Query(...)) -> None:
    svc = get_service()
    await manager.connect(user_id, websocket)
    await svc.presence.set_online(user_id, connection_id=user_id)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data: dict[str, Any] = json.loads(raw)
            except Exception:
                await websocket.send_text(raw)
                continue

            event = data.get("event")
            if event == "send_message":
                payload = data.get("data", {})
                msg = await svc.send_message(
                    sender_id=user_id,
                    recipient_id=payload.get("recipient_id"),
                    type=payload.get("type", "text"),
                    text=payload.get("text"),
                    image_url=payload.get("image_url"),
                    shared_ref_id=payload.get("shared_ref_id"),
                )
                # echo back to sender
                await websocket.send_text(json.dumps({"event": "message_ack", "data": {"id": str(msg["_id"])}}))
                # forward to recipient if connected
                await manager.send_to_user(payload.get("recipient_id"), json.dumps({"event": "new_message", "data": msg}, default=str))
            elif event in {"offer", "answer", "candidate", "end"}:
                target = data.get("to")
                await manager.send_to_user(target, json.dumps(data))
            else:
                await websocket.send_text(json.dumps({"event": "echo", "data": data}))
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(user_id)
        await svc.presence.set_offline(user_id)
