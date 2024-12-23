import os
import ctypes
from telegram import InlineKeyboardButton
from plugins import BotPlugin

class SystemPlugin(BotPlugin):
    @property
    def name(self) -> str:
        return "Система"
        
    @property
    def description(self) -> str:
        return "Управление системой и правами администратора"
        
    @property
    def buttons(self) -> list:
        return [
            [
                InlineKeyboardButton("💻 Права админа", callback_data="system_admin"),
                InlineKeyboardButton("🔌 Выключение", callback_data="system_shutdown")
            ]
        ]
        
    async def handle_callback(self, callback_data: str, update, context) -> bool:
        if callback_data == "system_admin":
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", __file__, None, 1)
                await update.callback_query.message.reply_text("✅ Права администратора получены")
            except Exception as e:
                await update.callback_query.message.reply_text(f"❌ Ошибка: {str(e)}")
            return True
            
        elif callback_data == "system_shutdown":
            try:
                os.system('shutdown /s /t 60')
                await update.callback_query.message.reply_text("🔌 Компьютер будет выключен через 1 минуту")
            except Exception as e:
                await update.callback_query.message.reply_text(f"❌ Ошибка: {str(e)}")
            return True
            
        return False 