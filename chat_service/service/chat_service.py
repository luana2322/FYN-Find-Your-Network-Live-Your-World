from datetime import datetime
from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from repository.message_repository import MessageRepository
from repository.presence_repository import PresenceRepository


class ChatService:
    def __init__(self, db: AsyncIOMotorDatabase, presence: PresenceRepository) -> None:
        self.repo = MessageRepository(db)
        self.presence = presence

    async def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        type: str,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        shared_ref_id: Optional[str] = None,
    ) -> dict[str, Any]:
        conversation_id = await self.repo.ensure_conversation(sender_id, recipient_id)
        now = datetime.utcnow()
        doc: dict[str, Any] = {
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "type": type,
            "text": text,
            "image_url": image_url,
            "shared_ref_id": shared_ref_id,
            "status": "sent",
            "created_at": now,
            "updated_at": now,
        }
        message_id = await self.repo.insert_message(doc)
        doc["_id"] = message_id
        preview = text if text else ("[image]" if image_url else "[shared]")
        await self.repo.update_conversation_on_message(conversation_id, preview)
        return doc

    async def list_messages(self, conversation_id: str, limit: int = 50, cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
        return await self.repo.list_messages(conversation_id, limit, cursor)

    async def list_conversations(self, user_id: str, limit: int = 50, skip: int = 0) -> list[dict]:
        return await self.repo.list_conversations(user_id, limit, skip)

    async def update_message_status(self, message_id: str, status: str) -> None:
        await self.repo.update_message_status(message_id, status)
