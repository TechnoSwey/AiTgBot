import asyncio
import logging
from openai import OpenAI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import Config
from database import Database
from models import AVAILABLE_MODELS, RESPONSE_MODES, get_model_info, validate_temperature
from keyboards import (
    get_main_menu_keyboard, get_modes_keyboard, get_back_keyboard,
    get_openai_keyboard, get_anthropic_keyboard, get_deepseek_keyboard,
    get_google_keyboard, get_qwen_keyboard, get_other_keyboard
)

# Проверяем конфигурацию
Config.validate()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация компонентов
config = Config()
db = Database(config.DATABASE_PATH)

# Инициализация бота
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Кэш клиентов OpenAI для разных моделей
openai_clients = {}

def get_client_for_model(model_id: str) -> OpenAI:
    """Получает или создает клиент для модели"""
    if model_id not in openai_clients:
        model_info = get_model_info(model_id)
        client = OpenAI(
            api_key=config.PROXYAPI_KEY,
            base_url=f"{config.PROXYAPI_BASE_URL}{model_info['api_path']}"
        )
        openai_clients[model_id] = client
    return openai_clients[model_id]

def split_long_message(text: str, max_length: int = None) -> list:
    """Разбивает длинный текст на части"""
    if max_length is None:
        max_length = config.MAX_MESSAGE_LENGTH
    
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    sentences = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
    
    for sentence in sentences:
        if len(current_part) + len(sentence) <= max_length:
            current_part += sentence
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = sentence
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts

async def get_ai_response(user_message: str, user_id: int, chat_id: int) -> str:
    """Получает ответ от выбранной модели"""
    try:
        # Получаем настройки пользователя
        settings = db.get_user_settings(user_id, chat_id)
        model_id = settings.get("current_model", "deepseek-chat")
        mode = settings.get("response_mode", "normal")
        
        # Получаем информацию о модели и режиме
        model_info = get_model_info(model_id)
        mode_config = RESPONSE_MODES.get(mode, RESPONSE_MODES["normal"])
        
        # Получаем клиент для модели
        client = get_client_for_model(model_id)
        
        # Получаем историю
        history = db.get_chat_history(user_id, chat_id)
        
        # Формируем сообщения
        messages = []
        if history:
            messages.extend(history[-10:])
        messages.append({"role": "user", "content": user_message})
        
        logger.info(f"Запрос: user={user_id}, модель={model_id}, режим={mode}")
        
        # Отправляем запрос
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=validate_temperature(model_id, mode_config["temperature"]),
            max_tokens=mode_config["max_tokens"],
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return f"❌ Ошибка при обращении к модели: {str(e)[:200]}"

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Я бот с поддержкой множества AI-моделей:\n"
        "• ⭐ <b>OpenAI:</b> GPT-5.2, GPT-5 Mini, GPT-5.1 Codex\n"
        "• 🎭 <b>Claude:</b> Opus 4.5, Sonnet 4.5, Haiku 4.5\n"
        "• 🧠 <b>DeepSeek:</b> V3, Reasoner\n"
        "• ⚡ <b>Google:</b> Gemini 2.5 Flash\n"
        "• 🐉 <b>Qwen:</b> Max, Coder Plus\n"
        "• 🔧 <b>Другие:</b> GLM 4.6, Grok 3\n\n"
        "Используйте меню ниже для настройки:"
    )
    
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard()
    )

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    """Показывает главное меню"""
    await message.answer(
        text="🔹 <b>Главное меню</b>\nВыберите категорию модели или настройки:",
        reply_markup=get_main_menu_keyboard()
    )

@dp.message(Command("clear"))
async def cmd_clear(message: Message):
    """Очищает историю"""
    db.clear_history(message.from_user.id, message.chat.id)
    await message.answer("✅ История успешно очищена!")

@dp.callback_query()
async def process_callbacks(callback: CallbackQuery):
    """Обработчик всех callback'ов"""
    await callback.answer()
    
    payload = callback.data
    
    # Главное меню
    if payload == "back_to_main":
        await callback.message.edit_text(
            text="🔹 <b>Главное меню</b>\nВыберите категорию модели или настройки:",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # Категории моделей
    if payload == "cat_openai":
        await callback.message.edit_text(
            text="⭐ <b>Модели OpenAI (ChatGPT):</b>\n\nВыберите модель:",
            reply_markup=get_openai_keyboard()
        )
        return
    
    if payload == "cat_anthropic":
        await callback.message.edit_text(
            text="🎭 <b>Модели Anthropic (Claude):</b>\n\nВыберите модель:",
            reply_markup=get_anthropic_keyboard()
        )
        return
    
    if payload == "cat_deepseek":
        await callback.message.edit_text(
            text="🧠 <b>Модели DeepSeek:</b>\n\nВыберите модель:",
            reply_markup=get_deepseek_keyboard()
        )
        return
    
    if payload == "cat_google":
        await callback.message.edit_text(
            text="⚡ <b>Модели Google:</b>\n\nВыберите модель:",
            reply_markup=get_google_keyboard()
        )
        return
    
    if payload == "cat_qwen":
        await callback.message.edit_text(
            text="🐉 <b>Модели Qwen:</b>\n\nВыберите модель:",
            reply_markup=get_qwen_keyboard()
        )
        return
    
    if payload == "cat_other":
        await callback.message.edit_text(
            text="🔧 <b>Другие модели:</b>\n\nВыберите модель:",
            reply_markup=get_other_keyboard()
        )
        return
    
    if payload == "menu_modes":
        await callback.message.edit_text(
            text="🎯 <b>Выберите режим ответов:</b>\n\n"
                 "🟢 Краткий - только суть\n"
                 "🟡 Обычный - сбалансированно\n"
                 "🔴 Подробный - развернутые ответы",
            reply_markup=get_modes_keyboard()
        )
        return
    
    if payload == "show_settings":
        settings = db.get_user_settings(callback.from_user.id, callback.message.chat.id)
        model_id = settings.get("current_model", "deepseek-chat")
        mode = settings.get("response_mode", "normal")
        
        model_info = get_model_info(model_id)
        mode_config = RESPONSE_MODES.get(mode, RESPONSE_MODES["normal"])
        
        text = (
            "⚙️ <b>Текущие настройки</b>\n\n"
            f"🤖 <b>Модель:</b> {model_info['name']}\n"
            f"📝 {model_info['description']}\n"
            f"📊 Контекст: {model_info['context_length']}\n\n"
            f"🎯 <b>Режим:</b> {mode_config['name']}\n"
            f"📊 {mode_config['description']}\n"
            f"• Температура: {mode_config['temperature']}\n"
            f"• Макс. токенов: {mode_config['max_tokens']}"
        )
        
        await callback.message.edit_text(
            text=text,
            reply_markup=get_back_keyboard()
        )
        return
    
    if payload == "show_history":
        history = db.get_chat_history(callback.from_user.id, callback.message.chat.id)
        if not history:
            text = "📭 <b>История сообщений пуста</b>"
        else:
            text = "📜 <b>Последние сообщения:</b>\n\n"
            for msg in history[-10:]:
                role = "👤" if msg["role"] == "user" else "🤖"
                content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                text += f"{role}: {content}\n\n"
        
        await callback.message.edit_text(
            text=text,
            reply_markup=get_back_keyboard()
        )
        return
    
    if payload == "clear_history":
        db.clear_history(callback.from_user.id, callback.message.chat.id)
        await callback.message.edit_text(
            text="✅ История успешно очищена!",
            reply_markup=get_back_keyboard()
        )
        return
    
    if payload == "show_help":
        help_text = (
            "❓ <b>Помощь</b>\n\n"
            "🔹 <b>Главное меню</b> - выбор категории модели\n"
            "🔹 <b>Выбор модели</b> - разные модели для разных задач\n"
            "🔹 <b>Режимы ответов</b>:\n"
            "   • 🟢 Краткий - только суть (512 токенов)\n"
            "   • 🟡 Обычный - сбалансированно (1024 токена)\n"
            "   • 🔴 Подробный - развернуто (2048 токенов)\n\n"
            "📝 <b>Совет:</b> Для программирования выбирайте GPT-5.1 Codex или Qwen3 Coder Plus\n"
            "Для сложных задач - Claude Opus 4.5 или GPT-5.2\n\n"
            "Команды:\n"
            "/start - начать работу\n"
            "/menu - показать меню\n"
            "/clear - очистить историю\n\n"
            "Просто отправляйте сообщения, и бот ответит выбранной моделью!"
        )
        
        await callback.message.edit_text(
            text=help_text,
            reply_markup=get_back_keyboard()
        )
        return
    
    # Выбор конкретной модели
    if payload.startswith("model_"):
        model_id = payload.replace("model_", "")
        if model_id in AVAILABLE_MODELS:
            db.set_model(callback.from_user.id, callback.message.chat.id, model_id)
            model_info = get_model_info(model_id)
            
            await callback.message.edit_text(
                text=f"✅ <b>Модель изменена</b>\n\nТеперь используется:\n<b>{model_info['name']}</b>\n\n{model_info['description']}\n\nКонтекст: {model_info['context_length']}",
                reply_markup=get_back_keyboard()
            )
        return
    
    # Выбор режима
    if payload.startswith("mode_"):
        mode = payload.replace("mode_", "")
        if mode in RESPONSE_MODES:
            db.set_response_mode(callback.from_user.id, callback.message.chat.id, mode)
            mode_config = RESPONSE_MODES[mode]
            
            await callback.message.edit_text(
                text=f"✅ <b>Режим изменен</b>\n\nТеперь используется:\n<b>{mode_config['name']}</b>\n\n{mode_config['description']}\n\nТемпература: {mode_config['temperature']}\nМакс. токенов: {mode_config['max_tokens']}",
                reply_markup=get_back_keyboard()
            )
        return

@dp.message()
async def handle_message(message: Message):
    """Обработчик текстовых сообщений"""
    # Сохраняем сообщение пользователя
    settings = db.get_user_settings(message.from_user.id, message.chat.id)
    db.save_message(
        message.from_user.id,
        message.chat.id,
        "user",
        message.text,
        settings.get("current_model")
    )
    
    # Показываем индикатор печати
    await bot.send_chat_action(message.chat.id, action="typing")
    
    try:
        # Получаем ответ от AI
        response_text = await get_ai_response(
            message.text,
            message.from_user.id,
            message.chat.id
        )
        
        # Сохраняем ответ
        db.save_message(
            message.from_user.id,
            message.chat.id,
            "assistant",
            response_text,
            settings.get("current_model")
        )
        
        # Разбиваем на части и отправляем
        parts = split_long_message(response_text)
        for i, part in enumerate(parts):
            if i == 0:
                await message.answer(part)
            else:
                await asyncio.sleep(0.5)
                await message.answer(part)
                
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer(f"❌ Ошибка: {str(e)[:200]}")

async def main():
    """Запуск бота"""
    logger.info("🚀 Запуск Telegram бота...")
    logger.info(f"Доступно моделей: {len(AVAILABLE_MODELS)}")
    logger.info(f"База данных: {config.DATABASE_PATH}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
