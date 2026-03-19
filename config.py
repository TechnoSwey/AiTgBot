import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Класс конфигурации бота"""
    
    # Токен бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Настройки ProxyAPI
    PROXYAPI_KEY = os.getenv("PROXYAPI_KEY")
    PROXYAPI_BASE_URL = os.getenv("PROXYAPI_BASE_URL", "https://api.proxyapi.ru")
    
    # Модель по умолчанию
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    
    # Настройки сообщений
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4000"))
    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
    
    # База данных
    DATABASE_PATH = os.getenv("DATABASE_PATH", "chat_history.db")
    
    @classmethod
    def validate(cls):
        """Проверяет наличие обязательных переменных"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен в .env файле")
        if not cls.PROXYAPI_KEY:
            raise ValueError("PROXYAPI_KEY не установлен в .env файле")
