from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.db.session import get_db
from app.models.dish import Dish
from app.core.ai_assistant import process_order_request

router = APIRouter(prefix="/ai", tags=["ai-assistant"])


class ChatMessage(BaseModel):
    role: str  # user / assistant
    content: str


class ChatRequest(BaseModel):
    cafe_id: int
    message: str
    history: List[ChatMessage] = []


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Получаем меню кафе
    dishes = db.query(Dish).filter(
        Dish.cafe_id == request.cafe_id,
        Dish.is_available == True
    ).all()

    if not dishes:
        raise HTTPException(status_code=404, detail="Menu not found")

    menu_items = [
        {
            "id": d.id,
            "name": d.name,
            "price": d.price,
            "description": d.description,
            "calories": d.calories,
            "is_vegan": d.is_vegan,
            "is_vegetarian": d.is_vegetarian,
            "allergens": d.allergens,
        }
        for d in dishes
    ]

    history = [{"role": m.role, "content": m.content} for m in request.history]

    result = await process_order_request(request.message, menu_items, history)
    return result
