import httpx
from app.core.config import get_settings

settings = get_settings()


async def send_telegram_message(text: str) -> bool:
    """Отправить сообщение в Telegram."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML",
                },
                timeout=5,
            )
            return res.status_code == 200
    except Exception:
        return False


async def notify_new_order(order) -> None:
    """Уведомление о новом заказе."""
    items_text = "\n".join([
        f"  • {item.dish_name} × {item.quantity} = {item.dish_price * item.quantity:.2f} €"
        for item in order.items
    ])
    text = (
        f"🍕 <b>Новый заказ #{order.id}</b>\n\n"
        f"👤 {order.customer_name}\n"
        f"📞 {order.customer_phone or '—'}\n"
        f"📍 {order.delivery_address or 'Самовывоз'}\n\n"
        f"<b>Состав:</b>\n{items_text}\n\n"
        f"💰 <b>Итого: {order.total:.2f} €</b>\n"
        f"💬 {order.comment or '—'}"
    )
    await send_telegram_message(text)
