import sqlite3
import logging
from typing import List, Dict, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    """Класс для работы с базой данных SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Ошибка БД: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Инициализация таблиц в базе данных"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица для истории сообщений
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    model TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Индекс для быстрого поиска
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_history 
                ON chat_history (user_id, chat_id, timestamp)
            """)
            
            # Таблица для настроек пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    chat_id INTEGER NOT NULL,
                    current_model TEXT DEFAULT 'deepseek-chat',
                    response_mode TEXT DEFAULT 'normal',
                    max_history INTEGER DEFAULT 10,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("База данных инициализирована")
    
    def save_message(self, user_id: int, chat_id: int, role: str, content: str, model: str = None):
        """Сохраняет сообщение в историю"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history (user_id, chat_id, role, content, model)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, chat_id, role, content, model))
            
            # Ограничиваем историю
            self._trim_history(conn, user_id, chat_id)
    
    def _trim_history(self, conn, user_id: int, chat_id: int):
        """Оставляет только последние сообщения"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT max_history FROM user_settings 
            WHERE user_id = ? AND chat_id = ?
        """, (user_id, chat_id))
        
        row = cursor.fetchone()
        max_history = row['max_history'] if row else 10
        
        cursor.execute("""
            DELETE FROM chat_history 
            WHERE user_id = ? AND chat_id = ? 
            AND id NOT IN (
                SELECT id FROM chat_history 
                WHERE user_id = ? AND chat_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            )
        """, (user_id, chat_id, user_id, chat_id, max_history * 2))
    
    def get_chat_history(self, user_id: int, chat_id: int) -> List[Dict[str, str]]:
        """Получает историю переписки"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content FROM chat_history 
                WHERE user_id = ? AND chat_id = ? 
                ORDER BY timestamp ASC 
                LIMIT 20
            """, (user_id, chat_id))
            
            return [{"role": row["role"], "content": row["content"]} for row in cursor.fetchall()]
    
    def clear_history(self, user_id: int, chat_id: int):
        """Очищает историю переписки"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM chat_history 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            logger.info(f"История очищена для user_id={user_id}")
    
    def get_user_settings(self, user_id: int, chat_id: int) -> Dict[str, Any]:
        """Получает настройки пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_settings 
                WHERE user_id = ? AND chat_id = ?
            """, (user_id, chat_id))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            
            # Настройки по умолчанию
            return {
                "user_id": user_id,
                "chat_id": chat_id,
                "current_model": "deepseek-chat",
                "response_mode": "normal",
                "max_history": 10
            }
    
    def set_model(self, user_id: int, chat_id: int, model: str):
        """Устанавливает модель для пользователя"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_settings 
                (user_id, chat_id, current_model, response_mode, max_history, updated_at)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT response_mode FROM user_settings WHERE user_id = ?), 'normal'),
                    COALESCE((SELECT max_history FROM user_settings WHERE user_id = ?), 10),
                    CURRENT_TIMESTAMP)
            """, (user_id, chat_id, model, user_id, user_id))
            logger.info(f"Модель изменена для user_id={user_id}: {model}")
    
    def set_response_mode(self, user_id: int, chat_id: int, mode: str):
        """Устанавливает режим ответов"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_settings 
                (user_id, chat_id, response_mode, current_model, max_history, updated_at)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT current_model FROM user_settings WHERE user_id = ?), 'deepseek-chat'),
                    COALESCE((SELECT max_history FROM user_settings WHERE user_id = ?), 10),
                    CURRENT_TIMESTAMP)
            """, (user_id, chat_id, mode, user_id, user_id))
            logger.info(f"Режим изменен для user_id={user_id}: {mode}")
