# Chat Service

FastAPI-based microservice providing real-time 1-on-1 chat, WebRTC signaling, message history, and notifications in a microservices architecture.

## Quickstart

1. Create and populate a `.env` file using `.env.example`.
2. Install dependencies:

```bash
python -m venv .venv && . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

3. Run the service:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Features
- WebSocket 1-on-1 messaging and signaling
- MongoDB storage for messages and conversations (Motor)
- Redis presence tracking and ephemeral state
- FCM notification stub
- REST APIs for history, conversations, and message status

## Project Structure
```
chat_service/
├── controller/
├── service/
├── repository/
├── model/
├── schema/
├── util/
├── config/
└── main.py
```

## Environment
See `.env.example` for required variables.

## Notes
- This scaffold uses minimal auth stubs; integrate with your Auth service.
- WebRTC signaling is provided via WebSocket events (offer/answer/candidate/end).
