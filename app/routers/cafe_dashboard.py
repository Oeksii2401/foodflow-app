import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import Dict, List

from app.db.session import get_db
from app.models.order import Order
from app.models.cafe import Cafe
from app.core.deps import get_current_active_user
from app.models.user import User

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/cafe", tags=["cafe-dashboard"])


# WebSocket менеджер подключений
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, cafe_id: int):
        await websocket.accept()
        if cafe_id not in self.active_connections:
            self.active_connections[cafe_id] = []
        self.active_connections[cafe_id].append(websocket)

    def disconnect(self, websocket: WebSocket, cafe_id: int):
        if cafe_id in self.active_connections:
            self.active_connections[cafe_id].remove(websocket)

    async def broadcast_to_cafe(self, cafe_id: int, message: dict):
        if cafe_id in self.active_connections:
            for connection in self.active_connections[cafe_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass


manager = ConnectionManager()


@router.get("/dashboard/{cafe_id}", response_class=HTMLResponse)
async def dashboard_page(cafe_id: int, request: Request, db: Session = Depends(get_db)):
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    orders = db.query(Order).filter(
        Order.cafe_id == cafe_id
    ).order_by(Order.created_at.desc()).limit(50).all()
    return templates.TemplateResponse(request=request, name="cafe/dashboard.html", context={
        "cafe": cafe,
        "orders": orders,
    })


@router.websocket("/ws/{cafe_id}")
async def websocket_endpoint(websocket: WebSocket, cafe_id: int):
    await manager.connect(websocket, cafe_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, cafe_id)


@router.patch("/orders/{order_id}/status")
async def update_order_status_cafe(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)

    # Уведомляем всех подключённых через WebSocket
    await manager.broadcast_to_cafe(order.cafe_id, {
        "type": "status_update",
        "order_id": order.id,
        "status": status,
    })

    return {"ok": True, "status": status}
