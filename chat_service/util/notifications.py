from typing import Any, Optional
import httpx


class NotificationClient:
    def __init__(self, server_key: Optional[str]) -> None:
        self.server_key = server_key
        self.base_url = "https://fcm.googleapis.com/fcm/send"

    async def send_push(self, token: str, title: str, body: str, data: Optional[dict[str, Any]] = None) -> None:
        if not self.server_key:
            return
        headers = {
            "Authorization": f"key={self.server_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "to": token,
            "notification": {"title": title, "body": body},
            "data": data or {},
        }
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(self.base_url, headers=headers, json=payload)
