from fastapi import FastAPI
from pydantic import BaseModel
from treys import Card
from .poker_logic import simulate_win_probability

app = FastAPI()

class HandRequest(BaseModel):
    hole: list[str]  # e.g. ["As", "Kd"]
    board: list[str]  # e.g. ["7h", "Ts", "2d"]

@app.post("/simulate")
def simulate(request: HandRequest):
    try:
        hole_cards = [Card.new(c) for c in request.hole]
        board_cards = [Card.new(c) for c in request.board]
    except:
        return {"error": "Invalid card format. Use like 'As', 'Kd', '7h'..."}

    result = simulate_win_probability(hole_cards, board_cards)
    return result
