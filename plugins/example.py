from utils import BotPlugin
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

class Plugin(BotPlugin):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "Example Plugin"
        self.version = "1.0.0"
        self.description = "Пример плагина для демонстрации API"
        
    async def on_load(self):
        """Вызывается при загрузке плагина"""
        print(f"[{self.name}] Plugin loaded!")
        
    async def on_command(self, command: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команд"""
        if command == "example":
            await update.effective_message.reply_text(
                f"🔌 *{self.name}* v{self.version}\n"
                f"Это пример работы плагина!\n\n"
                f"Описание: {self.description}",
                parse_mode=ParseMode.MARKDOWN
            )
        
    async def on_message(self, message: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка сообщений"""
        # Пример: отвечаем на сообщение "ping"
        if message.lower() == "ping":
            await update.effective_message.reply_text("pong!")
        
    def get_commands(self) -> list:
        """Список доступных команд"""
        return ["example"] 