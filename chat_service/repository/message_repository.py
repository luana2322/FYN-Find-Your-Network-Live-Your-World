from datetime import datetime
from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class MessageRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.messages = db.get_collection("messages")
        self.conversations = db.get_collection("conversations")
        self.messages.create_index([("conversation_id", 1), ("created_at", -1)])
        self.conversations.create_index([("user_a_id", 1), ("user_b_id", 1)], unique=True)
        self.conversations.create_index([("last_message_at", -1)])

    async def ensure_conversation(self, user_a_id: str, user_b_id: str) -> str:
        a, b = sorted([user_a_id, user_b_id])
        doc = await self.conversations.find_one({"user_a_id": a, "user_b_id": b})
        now = datetime.utcnow()
        if doc:
            return str(doc["_id"])
        result = await self.conversations.insert_one({
            "user_a_id": a,
            "user_b_id": b,
            "last_message_at": now,
            "last_message_preview": None,
            "created_at": now,
            "updated_at": now,
        })
        return str(result.inserted_id)

    async def insert_message(self, message: dict[str, Any]) -> str:
        result = await self.messages.insert_one(message)
        return str(result.inserted_id)

    async def update_conversation_on_message(self, conversation_id: str, preview: Optional[str]) -> None:
        now = datetime.utcnow()
        await self.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"last_message_at": now, "last_message_preview": preview, "updated_at": now}},
        )

    async def list_messages(self, conversation_id: str, limit: int = 50, cursor: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
        query: dict[str, Any] = {"conversation_id": conversation_id}
        if cursor:
            query["_id"] = {"$lt": ObjectId(cursor)}
        cursor_db = self.messages.find(query).sort("_id", -1).limit(limit)
        items = [doc async for doc in cursor_db]
        next_cursor = str(items[-1]["_id"]) if items else None
        return items, next_cursor

    async def list_conversations(self, user_id: str, limit: int = 50, skip: int = 0) -> list[dict]:
        return [
            doc async for doc in self.conversations.find({"$or": [{"user_a_id": user_id}, {"user_b_id": user_id}]}).sort("last_message_at", -1).skip(skip).limit(limit)
        ]

    async def update_message_status(self, message_id: str, status: str) -> None:
        await self.messages.update_one({"_id": ObjectId(message_id)}, {"$set": {"status": status, "updated_at": datetime.utcnow()}})
