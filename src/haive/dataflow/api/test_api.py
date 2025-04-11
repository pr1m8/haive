from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import asyncio
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

# Setup DB connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI(title="Checkpoint API")

@app.websocket("/ws/checkpoints/{thread_id}")
async def websocket_checkpoints(websocket: WebSocket, thread_id: str = "connect4_match_7a3c0258"):
    await websocket.accept()
    try:
        with SessionLocal() as session:
            result = session.execute(
                text("SELECT * FROM public.checkpoints WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            ).mappings()

            for row in result:
                await websocket.send_text(json.dumps(dict(row)))
                await asyncio.sleep(2)  # Delay between rows

        await websocket.close()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for thread_id={thread_id}")
@app.websocket("/ws/battleship/{thread_id}")
async def websocket_battleship(websocket: WebSocket, thread_id: str = "38385721-6ba5-4426-981b-d45787519b2f"):
    await websocket.accept()
    try:
        with SessionLocal() as session:
            result = session.execute(
                text("SELECT * FROM public.checkpoints WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            ).mappings()

            for row in result:
                await websocket.send_text(json.dumps(dict(row)))
                await asyncio.sleep(2)  # Delay between rows

        await websocket.close()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for thread_id={thread_id}")

@app.websocket("/ws/chess/{thread_id}")
async def websocket_chess(websocket: WebSocket, thread_id: str = "31e8a7f8-2c78-460a-85ce-0e3f9773f277"):
    await websocket.accept()
    try:
        with SessionLocal() as session:
            result = session.execute(
                text("SELECT * FROM public.checkpoints WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            ).mappings()

            for row in result:
                await websocket.send_text(json.dumps(dict(row)))
                await asyncio.sleep(2)  # Delay between rows

        await websocket.close()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for thread_id={thread_id}")


@app.websocket("/ws/checkers/{thread_id}")
async def websocket_checkers(websocket: WebSocket, thread_id: str = "31e8a7f8-2c78-460a-85ce-0e3f9773f277"):
    await websocket.accept()
    try:
        with SessionLocal() as session:
            result = session.execute(
                text("SELECT * FROM public.checkpoints WHERE thread_id = :thread_id"),
                {"thread_id": thread_id}
            ).mappings()

            for row in result:
                await websocket.send_text(json.dumps(dict(row)))
                await asyncio.sleep(2)  # Delay between rows

        await websocket.close()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for thread_id={thread_id}")
