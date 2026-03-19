from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models import RESPONSE_MODES

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    
    buttons = [
        [InlineKeyboardButton(text="⭐ OpenAI (ChatGPT)", callback_data="cat_openai")],
        [InlineKeyboardButton(text="🎭 Anthropic (Claude)", callback_data="cat_anthropic")],
        [InlineKeyboardButton(text="🧠 DeepSeek", callback_data="cat_deepseek")],
        [InlineKeyboardButton(text="⚡ Google", callback_data="cat_google")],
        [InlineKeyboardButton(text="🐉 Qwen", callback_data="cat_qwen")],
        [InlineKeyboardButton(text="🔧 Другие модели", callback_data="cat_other")],
        [InlineKeyboardButton(text="🎯 Режимы ответов", callback_data="menu_modes")],
        [InlineKeyboardButton(text="⚙️ Текущие настройки", callback_data="show_settings")],
        [InlineKeyboardButton(text="📜 История", callback_data="show_history")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="show_help")],
        [InlineKeyboardButton(text="🗑 Очистить историю", callback_data="clear_history")]
    ]
    
    for button in buttons:
        builder.row(button[0])
    
    return builder.as_markup()

def get_openai_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для OpenAI моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🤖 GPT-5.2 (флагман)", callback_data="model_openai/gpt-5.2"))
    builder.row(InlineKeyboardButton(text="⚡ GPT-5 Mini (быстрая)", callback_data="model_openai/gpt-5-mini"))
    builder.row(InlineKeyboardButton(text="💻 GPT-5.1 Codex (код)", callback_data="model_openai/gpt-5.1-codex-max"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_anthropic_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для Claude моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🎭 Claude Opus 4.5 (мощная)", callback_data="model_anthropic/claude-opus-4-5"))
    builder.row(InlineKeyboardButton(text="📝 Claude Sonnet 4.5 (универсальная)", callback_data="model_anthropic/claude-sonnet-4-5"))
    builder.row(InlineKeyboardButton(text="🌪️ Claude Haiku 4.5 (быстрая)", callback_data="model_anthropic/claude-haiku-4-5"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_deepseek_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для DeepSeek моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🧠 DeepSeek V3 (универсальная)", callback_data="model_deepseek-chat"))
    builder.row(InlineKeyboardButton(text="🔍 DeepSeek Reasoner (рассуждения)", callback_data="model_deepseek-reasoner"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_google_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для Google моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="⚡ Gemini 2.5 Flash", callback_data="model_gemini/gemini-2.5-flash"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_qwen_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для Qwen моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🐉 Qwen3 Max (флагман)", callback_data="model_qwen3-max"))
    builder.row(InlineKeyboardButton(text="👨‍💻 Qwen3 Coder Plus (код)", callback_data="model_qwen3-coder-plus"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_other_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для других моделей"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🎯 GLM 4.6", callback_data="model_glm-4.6"))
    builder.row(InlineKeyboardButton(text="💎 Grok 3", callback_data="model_grok/grok-3"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_modes_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора режима ответов"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text=RESPONSE_MODES["short"]["name"], callback_data="mode_short"))
    builder.row(InlineKeyboardButton(text=RESPONSE_MODES["normal"]["name"], callback_data="mode_normal"))
    builder.row(InlineKeyboardButton(text=RESPONSE_MODES["detailed"]["name"], callback_data="mode_detailed"))
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    
    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура только с кнопкой назад"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_main"))
    return builder.as_markup()
