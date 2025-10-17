from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

MessageType = Literal["text", "image", "post", "reel"]
MessageStatus = Literal["sent", "delivered", "read"]


@dataclass
class Message:
    id: Optional[str]
    conversation_id: str
    sender_id: str
    recipient_id: str
    type: MessageType
    text: Optional[str]
    image_url: Optional[str]
    shared_ref_id: Optional[str]
    status: MessageStatus
    created_at: datetime
    updated_at: datetime


@dataclass
class Conversation:
    id: Optional[str]
    user_a_id: str
    user_b_id: str
    last_message_at: datetime
    last_message_preview: Optional[str]
    created_at: datetime
    updated_at: datetime
