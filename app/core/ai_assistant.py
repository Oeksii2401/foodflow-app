from groq import Groq
from app.core.config import get_settings

settings = get_settings()


def get_groq_client():
    return Groq(api_key=settings.GROQ_API_KEY)


async def process_order_request(user_message: str, menu_items: list, chat_history: list = []) -> dict:
    """
    Обрабатывает запрос пользователя и подбирает блюда из меню.
    
    menu_items: список блюд [{"id": 1, "name": "Маргарита", "price": 9.9, 
                               "description": "...", "calories": 800,
                               "is_vegan": False, "is_vegetarian": True,
                               "allergens": "глютен, лактоза"}]
    chat_history: история диалога [{"role": "user/assistant", "content": "..."}]
    """
    client = get_groq_client()

    # Формируем описание меню для AI
    menu_text = "\n".join([
        f"- ID:{item['id']} {item['name']} ({item['price']} €)"
        + (f", {item['calories']} ккал" if item.get('calories') else "")
        + (" [веган]" if item.get('is_vegan') else "")
        + (" [вегетарианское]" if item.get('is_vegetarian') else "")
        + (f", аллергены: {item['allergens']}" if item.get('allergens') else "")
        + (f" — {item['description']}" if item.get('description') else "")
        for item in menu_items
    ])

    system_prompt = f"""Ты дружелюбный AI-ассистент в кафе. Помогаешь клиентам выбрать блюда.

МЕНЮ КАФЕ:
{menu_text}

ТВОИ ЗАДАЧИ:
1. Понять что хочет клиент (даже если пишет расплывчато — "хочу есть", "что-нибудь лёгкое")
2. Предложить подходящие блюда из меню (только те что есть в списке выше)
3. Уточнить предпочтения если нужно (веган, аллергии, диета, без свинины и т.д.)
4. Показать калорийность если клиент спрашивает или на диете
5. Отвечать на языке клиента (RU/DE/EN/UK)

ФОРМАТ ОТВЕТА (всегда JSON):
{{
  "message": "текст ответа для клиента",
  "suggested_dishes": [1, 3],  // ID блюд которые рекомендуешь (пустой массив если просто уточняешь)
  "ask_preferences": false  // true если нужно уточнить предпочтения
}}

ВАЖНО: отвечай ТОЛЬКО валидным JSON, без markdown блоков."""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()

    try:
        import json
        # Убираем markdown если есть
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content)
    except Exception:
        return {
            "message": content,
            "suggested_dishes": [],
            "ask_preferences": False
        }
