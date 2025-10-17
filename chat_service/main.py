from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from config.db import init_mongo, shutdown_mongo
from config.cache import init_redis, shutdown_redis
from controller.rest import router as rest_router
from controller.ws import router as ws_router

settings = get_settings()

app = FastAPI(title=settings.app_name)

# CORS - adjust for your gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await init_mongo()
    await init_redis()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await shutdown_redis()
    await shutdown_mongo()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


# Routers
app.include_router(rest_router, prefix="/api/chat", tags=["chat-rest"])
app.include_router(ws_router, tags=["chat-ws"])
