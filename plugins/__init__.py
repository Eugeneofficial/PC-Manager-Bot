from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes

class BotPlugin(ABC):
    """Базовый класс для плагинов бота"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Название плагина"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Описание плагина"""
        pass
        
    @property
    def buttons(self) -> list:
        """Кнопки для добавления в интерфейс бота"""
        return []
        
    @abstractmethod
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка сообщений"""
        pass 