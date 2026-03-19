"""Конфигурация моделей через ProxyAPI (только актуальные)"""

AVAILABLE_MODELS = {
    # ===== OpenAI (ChatGPT) =====
    "openai/gpt-5.2": {
        "name": "🤖 GPT-5.2",
        "provider": "OpenAI",
        "description": "Флагманская модель OpenAI, топ по всем метрикам",
        "max_tokens": 16384,
        "temperature_range": (0.0, 2.0),
        "api_path": "/openai/v1",
        "category": "openai",
        "context_length": "128K"
    },
    "openai/gpt-5-mini": {
        "name": "⚡ GPT-5 Mini",
        "provider": "OpenAI",
        "description": "Легкая и быстрая модель для повседневных задач",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/openai/v1",
        "category": "openai",
        "context_length": "64K"
    },
    "openai/gpt-5.1-codex-max": {
        "name": "💻 GPT-5.1 Codex",
        "provider": "OpenAI",
        "description": "Специализирована для программирования и технических задач",
        "max_tokens": 16384,
        "temperature_range": (0.0, 2.0),
        "api_path": "/openai/v1",
        "category": "openai",
        "context_length": "128K"
    },
    
    # ===== Anthropic (Claude) =====
    "anthropic/claude-opus-4-5": {
        "name": "🎭 Claude Opus 4.5",
        "provider": "Anthropic",
        "description": "Самая мощная модель Claude для сложных задач",
        "max_tokens": 8192,
        "temperature_range": (0.0, 1.0),
        "api_path": "/anthropic/v1",
        "category": "anthropic",
        "context_length": "200K"
    },
    "anthropic/claude-sonnet-4-5": {
        "name": "📝 Claude Sonnet 4.5",
        "provider": "Anthropic",
        "description": "Универсальная модель, баланс скорости и качества",
        "max_tokens": 8192,
        "temperature_range": (0.0, 1.0),
        "api_path": "/anthropic/v1",
        "category": "anthropic",
        "context_length": "180K"
    },
    "anthropic/claude-haiku-4-5": {
        "name": "🌪️ Claude Haiku 4.5",
        "provider": "Anthropic",
        "description": "Быстрая модель для простых задач",
        "max_tokens": 4096,
        "temperature_range": (0.0, 1.0),
        "api_path": "/anthropic/v1",
        "category": "anthropic",
        "context_length": "150K"
    },
    
    # ===== DeepSeek =====
    "deepseek-chat": {
        "name": "🧠 DeepSeek V3",
        "provider": "DeepSeek",
        "description": "Универсальная модель для общих задач",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/deepseek/v1",
        "category": "deepseek",
        "context_length": "128K"
    },
    "deepseek-reasoner": {
        "name": "🔍 DeepSeek Reasoner",
        "provider": "DeepSeek",
        "description": "С улучшенными способностями к рассуждению",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/deepseek/v1",
        "category": "deepseek",
        "context_length": "128K"
    },
    
    # ===== Google Gemini =====
    "gemini/gemini-2.5-flash": {
        "name": "⚡ Gemini 2.5 Flash",
        "provider": "Google",
        "description": "Быстрая модель от Google для оперативных ответов",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/gemini/v1",
        "category": "google",
        "context_length": "1M"
    },
    
    # ===== Qwen (Alibaba) =====
    "qwen3-max": {
        "name": "🐉 Qwen3 Max",
        "provider": "Alibaba",
        "description": "Флагманская модель Qwen",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/qwen/v1",
        "category": "qwen",
        "context_length": "128K"
    },
    "qwen3-coder-plus": {
        "name": "👨‍💻 Qwen3 Coder Plus",
        "provider": "Alibaba",
        "description": "Специализирована для программирования",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/qwen/v1",
        "category": "qwen",
        "context_length": "128K"
    },
    
    # ===== GLM =====
    "glm-4.6": {
        "name": "🎯 GLM 4.6",
        "provider": "Zhipu",
        "description": "Мощная китайская мультиязычная модель",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/glm/v1",
        "category": "other",
        "context_length": "128K"
    },
    
    # ===== xAI =====
    "grok/grok-3": {
        "name": "💎 Grok 3",
        "provider": "xAI",
        "description": "Модель от xAI с доступом к реальному времени",
        "max_tokens": 8192,
        "temperature_range": (0.0, 2.0),
        "api_path": "/grok/v1",
        "category": "other",
        "context_length": "128K"
    }
}

# Режимы ответов
RESPONSE_MODES = {
    "short": {
        "name": "🟢 Краткий",
        "max_tokens": 512,
        "temperature": 0.5,
        "description": "Максимально краткие ответы, только суть"
    },
    "normal": {
        "name": "🟡 Обычный",
        "max_tokens": 1024,
        "temperature": 0.7,
        "description": "Сбалансированные ответы"
    },
    "detailed": {
        "name": "🔴 Подробный",
        "max_tokens": 2048,
        "temperature": 0.9,
        "description": "Развернутые ответы с деталями"
    }
}

# Категории для меню
MODEL_CATEGORIES = {
    "openai": {
        "name": "⭐ OpenAI (ChatGPT)",
        "emoji": "⭐",
        "models": ["openai/gpt-5.2", "openai/gpt-5-mini", "openai/gpt-5.1-codex-max"]
    },
    "anthropic": {
        "name": "🎭 Anthropic (Claude)",
        "emoji": "🎭",
        "models": ["anthropic/claude-opus-4-5", "anthropic/claude-sonnet-4-5", "anthropic/claude-haiku-4-5"]
    },
    "deepseek": {
        "name": "🧠 DeepSeek",
        "emoji": "🧠",
        "models": ["deepseek-chat", "deepseek-reasoner"]
    },
    "google": {
        "name": "⚡ Google",
        "emoji": "⚡",
        "models": ["gemini/gemini-2.5-flash"]
    },
    "qwen": {
        "name": "🐉 Qwen",
        "emoji": "🐉",
        "models": ["qwen3-max", "qwen3-coder-plus"]
    },
    "other": {
        "name": "🔧 Другие модели",
        "emoji": "🔧",
        "models": ["glm-4.6", "grok/grok-3"]
    }
}

def get_model_info(model_id: str) -> dict:
    """Возвращает информацию о модели"""
    return AVAILABLE_MODELS.get(model_id, AVAILABLE_MODELS["deepseek-chat"])

def get_models_by_category(category: str = None) -> dict:
    """Возвращает модели по категории"""
    if category and category in MODEL_CATEGORIES:
        model_ids = MODEL_CATEGORIES[category]["models"]
        return {mid: AVAILABLE_MODELS[mid] for mid in model_ids if mid in AVAILABLE_MODELS}
    return AVAILABLE_MODELS

def validate_temperature(model_id: str, temperature: float) -> float:
    """Проверяет, что температура в допустимом диапазоне для модели"""
    model_info = get_model_info(model_id)
    min_temp, max_temp = model_info["temperature_range"]
    return max(min_temp, min(temperature, max_temp))
