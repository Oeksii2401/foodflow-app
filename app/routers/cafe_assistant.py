from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os
from groq import Groq

from app.db.session import get_db
from app.models.cafe import Cafe
from app.models.dish import Dish
from app.models.menu_category import MenuCategory
from app.models.delivery_zone import DeliveryZone
from app.models.stripe_account import StripeAccount
from app.core.translations import TRANSLATIONS

router = APIRouter(prefix="/cafe/ai", tags=["cafe-assistant"])
templates = Jinja2Templates(directory="templates")
def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

ASSISTANT_TRANSLATIONS = {
    "de": {
        "title": "KI-Assistent",
        "subtitle": "hilft mit Speisekarte, Lieferung, Registrierung",
        "online": "KI online",
        "back": "← Dashboard",
        "placeholder": "Schreiben Sie Ihre Frage...",
        "send": "Senden",
        "btn_stripe": "💳 Stripe Connect",
        "btn_dish": "🍽️ Gerichtsbeschreibung",
        "btn_calories": "🔢 Kalorien berechnen",
        "btn_delivery": "🗺️ Lieferzonen",
        "btn_photo": "📸 Foto-Tipps",
        "btn_pricing": "💶 Preisgestaltung",
        "greeting": "Hallo! Ich bin Ihr KI-Assistent für das Café <strong>{cafe_name}</strong>. 👋<br><br>Ich kann Ihnen helfen mit:<br>• Stripe Connect Registrierung<br>• Speisekarte erstellen und gestalten<br>• Kalorien berechnen (KBJU)<br>• Lieferzonen einrichten<br>• Preisgestaltung in Deutschland<br><br>Womit fangen wir an?",
        "quick_stripe": "Hilf mir, Stripe Connect einzurichten",
        "quick_dish": "Hilf mir, eine Beschreibung für ein neues Gericht zu erstellen",
        "quick_calories": "Berechne Kalorien für ein Gericht",
        "quick_delivery": "Hilf mir, Lieferzonen einzurichten",
        "quick_photo": "Wie macht man ein gutes Foto von einem Gericht?",
        "quick_pricing": "Welche Preise soll ich für Gerichte in Deutschland festlegen?",
        "error": "❌ Verbindungsfehler. Bitte versuchen Sie es erneut.",
    },
    "en": {
        "title": "AI Assistant",
        "subtitle": "helps with menu, delivery, registration",
        "online": "AI online",
        "back": "← Dashboard",
        "placeholder": "Write your question...",
        "send": "Send",
        "btn_stripe": "💳 Stripe Connect",
        "btn_dish": "🍽️ Dish description",
        "btn_calories": "🔢 Calorie calculator",
        "btn_delivery": "🗺️ Delivery zones",
        "btn_photo": "📸 Photo tips",
        "btn_pricing": "💶 Pricing advice",
        "greeting": "Hello! I'm your AI assistant for café <strong>{cafe_name}</strong>. 👋<br><br>I can help you with:<br>• Stripe Connect registration<br>• Creating and formatting your menu<br>• Calorie calculation (macros)<br>• Setting up delivery zones<br>• Pricing strategy for Germany<br><br>Where shall we start?",
        "quick_stripe": "Help me set up Stripe Connect",
        "quick_dish": "Help me create a description for a new dish",
        "quick_calories": "Calculate calories for a dish",
        "quick_delivery": "Help me set up delivery zones",
        "quick_photo": "How do I take a good photo of a dish?",
        "quick_pricing": "What prices should I set for dishes in Germany?",
        "error": "❌ Connection error. Please try again.",
    },
    "ru": {
        "title": "AI-ассистент",
        "subtitle": "помогает с меню, доставкой, регистрацией",
        "online": "AI онлайн",
        "back": "← Дашборд",
        "placeholder": "Напишите вопрос...",
        "send": "Отправить",
        "btn_stripe": "💳 Stripe Connect",
        "btn_dish": "🍽️ Описание блюда",
        "btn_calories": "🔢 Расчёт КБЖУ",
        "btn_delivery": "🗺️ Зоны доставки",
        "btn_photo": "📸 Советы по фото",
        "btn_pricing": "💶 Ценообразование",
        "greeting": "Привет! Я ваш AI-ассистент для кафе <strong>{cafe_name}</strong>. 👋<br><br>Я помогу вам с:<br>• Регистрацией в Stripe Connect<br>• Созданием и оформлением меню<br>• Расчётом калорий (КБЖУ)<br>• Настройкой зон доставки<br>• Ценообразованием в Германии<br><br>С чего начнём?",
        "quick_stripe": "Помоги мне настроить Stripe Connect",
        "quick_dish": "Помоги создать описание для нового блюда",
        "quick_calories": "Рассчитай калории для блюда",
        "quick_delivery": "Помоги настроить зоны доставки",
        "quick_photo": "Как сделать хорошее фото блюда?",
        "quick_pricing": "Какие цены установить на блюда в Германии?",
        "error": "❌ Ошибка соединения. Попробуйте ещё раз.",
    },
    "uk": {
        "title": "AI-асистент",
        "subtitle": "допомагає з меню, доставкою, реєстрацією",
        "online": "AI онлайн",
        "back": "← Дашборд",
        "placeholder": "Напишіть питання...",
        "send": "Надіслати",
        "btn_stripe": "💳 Stripe Connect",
        "btn_dish": "🍽️ Опис страви",
        "btn_calories": "🔢 Розрахунок КБЖУ",
        "btn_delivery": "🗺️ Зони доставки",
        "btn_photo": "📸 Поради щодо фото",
        "btn_pricing": "💶 Ціноутворення",
        "greeting": "Привіт! Я ваш AI-асистент для кафе <strong>{cafe_name}</strong>. 👋<br><br>Я допоможу вам з:<br>• Реєстрацією в Stripe Connect<br>• Створенням та оформленням меню<br>• Розрахунком калорій (КБЖУ)<br>• Налаштуванням зон доставки<br>• Ціноутворенням у Німеччині<br><br>З чого почнемо?",
        "quick_stripe": "Допоможи налаштувати Stripe Connect",
        "quick_dish": "Допоможи створити опис для нової страви",
        "quick_calories": "Розрахуй калорії для страви",
        "quick_delivery": "Допоможи налаштувати зони доставки",
        "quick_photo": "Як зробити гарне фото страви?",
        "quick_pricing": "Які ціни встановити на страви у Німеччині?",
        "error": "❌ Помилка з'єднання. Спробуйте ще раз.",
    },
}

class OwnerChatMessage(BaseModel):
    role: str
    content: str

class OwnerChatRequest(BaseModel):
    cafe_id: int
    message: str
    history: List[OwnerChatMessage] = []
    lang: Optional[str] = "ru"

def get_cafe_context(cafe_id: int, db: Session) -> str:
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()
    if not cafe:
        return "Кафе не найдено."
    dishes = db.query(Dish).filter(Dish.cafe_id == cafe_id).all()
    categories = db.query(MenuCategory).filter(MenuCategory.cafe_id == cafe_id).all()
    zones = db.query(DeliveryZone).filter(DeliveryZone.cafe_id == cafe_id).all()
    stripe = db.query(StripeAccount).filter(StripeAccount.cafe_id == cafe_id).first()
    stripe_status = "connected" if (stripe and stripe.stripe_account_id) else "not connected"
    dishes_info = ""
    for d in dishes[:20]:
        flags = []
        if getattr(d, 'is_vegan', False): flags.append("vegan")
        if getattr(d, 'is_vegetarian', False): flags.append("vegetarian")
        cal = getattr(d, 'calories', None)
        allergens = getattr(d, 'allergens', None)
        dishes_info += f"  - {d.name} ({d.price}€)"
        if cal: dishes_info += f", {cal} kcal"
        if allergens: dishes_info += f", allergens: {allergens}"
        if flags: dishes_info += f" [{', '.join(flags)}]"
        dishes_info += "\n"
    zones_info = "\n".join([f"  - {z.name}: {z.delivery_price}€, min order {z.min_order}€" for z in zones]) or "  no zones configured"
    return f"""Cafe: {cafe.name}
Stripe Connect: {stripe_status}
Menu categories: {len(categories)}
Dishes: {len(dishes)}
Delivery zones: {len(zones)}

Dishes:
{dishes_info if dishes_info else '  menu is empty'}

Delivery zones:
{zones_info}"""

SYSTEM_PROMPT = """You are an AI assistant for cafe owners on the FoodFlow platform (Germany).
Help owners set up their cafe as effectively as possible.

You help with:
1. ONBOARDING — FoodFlow and Stripe Connect registration (explain each step in simple language)
2. MENU — generate dish names and descriptions, calculate macros (KBJU/KBZH) from ingredients
3. MENU TYPES — tag dishes (halal, vegan, vegetarian, kids menu, allergen-free)
4. PHOTOS — tips for appetizing food photography
5. DELIVERY — delivery zone setup and pricing for Germany
6. PRICING — pricing advice for the German market

IMPORTANT: Always respond in the same language the owner writes in (DE/EN/RU/UK).
If the owner describes dish ingredients — always calculate calories, protein, fat, carbs.
If the owner asks for a dish description — provide 2-3 variants to choose from.
Be friendly, specific, practical. Use the cafe context provided to give personalized advice."""

@router.post("/chat")
async def owner_chat(req: OwnerChatRequest, db: Session = Depends(get_db)):
    cafe_context = get_cafe_context(req.cafe_id, db)
    system = SYSTEM_PROMPT + f"\n\n=== CAFE CONTEXT ===\n{cafe_context}"
    messages = [{"role": m.role, "content": m.content} for m in req.history[-8:]]
    messages.append({"role": "user", "content": req.message})
    try:
        response = get_groq_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return {"message": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/page/{cafe_id}", response_class=HTMLResponse)
async def assistant_page(cafe_id: int, request: Request, db: Session = Depends(get_db), lang: str = "ru"):
    cafe = db.query(Cafe).filter(Cafe.id == cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    t = ASSISTANT_TRANSLATIONS.get(lang, ASSISTANT_TRANSLATIONS["ru"])
    return templates.TemplateResponse(
        request=request,
        name="cafe/assistant.html",
        context={"cafe": cafe, "t": t, "lang": lang}
    )


class DishGenerateRequest(BaseModel):
    cafe_id: int
    dish_input: str  # название или состав блюда
    lang: Optional[str] = "ru"

@router.post("/generate-dish")
async def generate_dish(req: DishGenerateRequest, db: Session = Depends(get_db)):
    cafe = db.query(Cafe).filter(Cafe.id == req.cafe_id).first()
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")

    prompt = f"""You are a professional menu copywriter for restaurants in Germany.

The cafe owner provided this dish input: "{req.dish_input}"

Generate exactly 3 name+description variants for this dish.
Also provide translations into DE, EN, RU, UK for the best variant (variant 1).
Also calculate approximate calories and macros if ingredients are mentioned.

Respond ONLY with valid JSON, no markdown, no explanation:
{{
  "variants": [
    {{
      "name": "dish name",
      "description": "appetizing description 1-2 sentences"
    }},
    {{
      "name": "dish name variant 2",
      "description": "appetizing description 1-2 sentences"
    }},
    {{
      "name": "dish name variant 3", 
      "description": "appetizing description 1-2 sentences"
    }}
  ],
  "translations": {{
    "de": {{"name": "...", "description": "..."}},
    "en": {{"name": "...", "description": "..."}},
    "ru": {{"name": "...", "description": "..."}},
    "uk": {{"name": "...", "description": "..."}}
  }},
  "calories": 450,
  "protein": 32,
  "fat": 18,
  "carbs": 45,
  "tags": ["vegan", "halal", "vegetarian", "kids"]
}}

tags array should only include tags that actually apply to this dish.
If no ingredients mentioned, omit calories/protein/fat/carbs fields."""

    try:
        response = get_groq_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.8,
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PhotoAnalyzeRequest(BaseModel):
    cafe_id: int
    image_base64: str
    lang: Optional[str] = "ru"

@router.post("/analyze-photo")
async def analyze_photo(req: PhotoAnalyzeRequest, db: Session = Depends(get_db)):
    prompts = {
        "ru": "Ты эксперт по фуд-фотографии для ресторанов. Оцени это фото блюда по шкале 1-10 и дай конкретные советы по улучшению. Структура ответа: 1) Оценка X/10 2) Что хорошо 3) Что улучшить 4) Конкретные советы по пересъёмке. Отвечай на русском.",
        "de": "Du bist ein Food-Fotografie-Experte für Restaurants. Bewerte dieses Gericht-Foto auf einer Skala von 1-10 und gib konkrete Verbesserungstipps. Antworte auf Deutsch.",
        "en": "You are a food photography expert for restaurants. Rate this dish photo on a scale of 1-10 and give specific improvement tips. Reply in English.",
        "uk": "Ти експерт з фуд-фотографії для ресторанів. Оціни це фото страви за шкалою 1-10 і дай конкретні поради щодо покращення. Відповідай українською.",
    }
    prompt = prompts.get(req.lang, prompts["ru"])
    try:
        response = get_groq_client().chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{req.image_base64}"}}
            ]}],
            max_tokens=1024,
        )
        return {"message": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
