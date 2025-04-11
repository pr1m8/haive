from fastapi import FastAPI
from src.api.api.connect4_api import connect4_api
from src.api.api.tic_tac_toe_api import tictactoe_api
# from db.api.chess_api import chess_api  # Add more as needed

# Create the master app
app = FastAPI(title="Agent Games API", version="1.0.0")

# Mount individual game APIs
app.include_router(connect4_api.app.router, prefix="/connect4", tags=["Connect4"])
app.include_router(tictactoe_api.app.router, prefix="/tictactoe", tags=["Tic Tac Toe"])
# app.include_router(chess_api.app.router, prefix="/chess", tags=["Chess"])  # Optional

# Optionally add health check
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Agent Games API!"}
