from fastapi import APIRouter, Depends, Query
from config.db import get_db
from config.cache import get_redis
from service.chat_service import ChatService
from schema.message import SendMessageRequest, PaginatedMessagesResponse, MessageResponse, ConversationResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis

router = APIRouter()


def get_chat_service(db: AsyncIOMotorDatabase = Depends(get_db), redis_client: Redis = Depends(get_redis)) -> ChatService:
    from repository.presence_repository import PresenceRepository

    presence = PresenceRepository(redis_client)
    return ChatService(db, presence)


@router.post("/messages", response_model=MessageResponse)
async def send_message(req: SendMessageRequest, svc: ChatService = Depends(get_chat_service), user_id: str = Query(..., description="Sender user id (stub)")) -> MessageResponse:
    doc = await svc.send_message(
        sender_id=user_id,
        recipient_id=req.recipient_id,
        type=req.type,
        text=req.text,
        image_url=req.image_url,
        shared_ref_id=req.shared_ref_id,
    )
    return MessageResponse(
        id=str(doc["_id"]),
        conversation_id=doc["conversation_id"],
        sender_id=doc["sender_id"],
        recipient_id=doc["recipient_id"],
        type=doc["type"],
        text=doc.get("text"),
        image_url=doc.get("image_url"),
        shared_ref_id=doc.get("shared_ref_id"),
        status=doc["status"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


@router.get("/messages", response_model=PaginatedMessagesResponse)
async def list_messages(conversation_id: str, limit: int = 50, cursor: str | None = None, svc: ChatService = Depends(get_chat_service)) -> PaginatedMessagesResponse:
    items, next_cursor = await svc.list_messages(conversation_id, limit, cursor)
    return PaginatedMessagesResponse(
        items=[
            MessageResponse(
                id=str(m["_id"]),
                conversation_id=m["conversation_id"],
                sender_id=m["sender_id"],
                recipient_id=m["recipient_id"],
                type=m["type"],
                text=m.get("text"),
                image_url=m.get("image_url"),
                shared_ref_id=m.get("shared_ref_id"),
                status=m["status"],
                created_at=m["created_at"],
                updated_at=m["updated_at"],
            )
            for m in items
        ],
        next_cursor=next_cursor,
    )


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(user_id: str, svc: ChatService = Depends(get_chat_service)) -> list[ConversationResponse]:
    docs = await svc.list_conversations(user_id)
    return [
        ConversationResponse(
            id=str(c["_id"]),
            user_a_id=c["user_a_id"],
            user_b_id=c["user_b_id"],
            last_message_at=c["last_message_at"],
            last_message_preview=c.get("last_message_preview"),
            created_at=c["created_at"],
            updated_at=c["updated_at"],
        )
        for c in docs
    ]
