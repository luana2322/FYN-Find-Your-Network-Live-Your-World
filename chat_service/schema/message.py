from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

MessageType = Literal["text", "image", "post", "reel"]
MessageStatus = Literal["sent", "delivered", "read"]


class SendMessageRequest(BaseModel):
    recipient_id: str = Field(...)
    type: MessageType = Field(default="text")
    text: Optional[str] = None
    image_url: Optional[str] = None
    shared_ref_id: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    recipient_id: str
    type: MessageType
    text: Optional[str] = None
    image_url: Optional[str] = None
    shared_ref_id: Optional[str] = None
    status: MessageStatus
    created_at: datetime
    updated_at: datetime


class ConversationResponse(BaseModel):
    id: str
    user_a_id: str
    user_b_id: str
    last_message_at: datetime
    last_message_preview: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PaginatedMessagesResponse(BaseModel):
    items: list[MessageResponse]
    next_cursor: Optional[str] = None
