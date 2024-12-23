import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters, Application
from telegram.constants import ParseMode

from utils import (
    get_system_info, get_processes, get_drives,
    shutdown_pc, restart_pc, sleep_pc, lock_pc,
    get_user_language, get_text,
    create_backup, get_network_info, generate_qr, run_as_admin
)

logger = logging.getLogger(__name__)

# Keyboard layouts
def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Get main keyboard for specified language."""
    keyboard = [
        [
            KeyboardButton(get_text('system_info', lang)),
            KeyboardButton(get_text('screenshot', lang))
        ],
        [
            KeyboardButton(get_text('files', lang)),
            KeyboardButton(get_text('processes', lang))
        ],
        [
            KeyboardButton(get_text('power', lang)),
            KeyboardButton(get_text('drives', lang))
        ],
        [
            KeyboardButton(get_text('support_author', lang)),
            KeyboardButton(get_text('language', lang))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Get language selection keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if not update.effective_message:
        return

    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id)
    
    keyboard = get_main_keyboard(lang)
    await update.effective_message.reply_text(
        get_text('start', lang),
        reply_markup=keyboard
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all non-command messages."""
    if not update.effective_message or not update.effective_message.text:
        return

    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id)
    text = update.effective_message.text

    try:
        # Handle different button presses
        if text == get_text('system_info', lang):
            info = get_system_info()
            response = (
                f"💻 *Системная информация:*\n\n"
                f"🖥 Платформа: `{info['platform']}`\n"
                f"⚡️ Процессор: {info['processor']}\n"
                f"🧮 Ядер: {info['cpu_cores']}\n"
                f"📊 Загрузка CPU: {info['cpu_usage']}%\n\n"
                f"🎮 Память:\n"
                f"Всего: {info['memory_total'] / (1024**3):.1f} GB\n"
                f"Использовано: {info['memory_percent']}%\n\n"
                f"💾 Диск C:\n"
                f"Всего: {info['disk_total'] / (1024**3):.1f} GB\n"
                f"Использовано: {info['disk_percent']}%"
            )
            await update.effective_message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            
        elif text == get_text('screenshot', lang):
            try:
                import pyautogui
                screenshot_path = "screenshot.png"
                pyautogui.screenshot(screenshot_path)
                with open(screenshot_path, 'rb') as photo:
                    await update.effective_message.reply_photo(photo)
                os.remove(screenshot_path)
            except Exception as e:
                await update.effective_message.reply_text(f"❌ Ошибка: {str(e)}")
                
        elif text == get_text('files', lang):
            path = os.getcwd()
            files = os.listdir(path)
            response = f"📂 Файлы в {path}:\n\n"
            for item in files[:15]:
                if os.path.isdir(os.path.join(path, item)):
                    response += f"📁 {item}/\n"
                else:
                    response += f"📄 {item}\n"
            if len(files) > 15:
                response += f"\n...и еще {len(files) - 15} файлов"
            await update.effective_message.reply_text(response)
            
        elif text == get_text('processes', lang):
            processes = get_processes()
            response = "📊 Процессы:\n\n"
            for proc in processes[:15]:
                response += f"🔹 {proc['name']} (PID: {proc['pid']})\n"
            if len(processes) > 15:
                response += f"\n...и еще {len(processes) - 15} процессов"
            await update.effective_message.reply_text(response)
            
        elif text == get_text('power', lang):
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔄 Перезагрузка", callback_data="restart"),
                    InlineKeyboardButton("⭕️ Выключение", callback_data="shutdown")
                ],
                [
                    InlineKeyboardButton("😴 Сон", callback_data="sleep"),
                    InlineKeyboardButton("🔒 Блокировка", callback_data="lock")
                ]
            ])
            await update.effective_message.reply_text(
                "⚙️ Управление питанием:",
                reply_markup=keyboard
            )
            
        elif text == get_text('drives', lang):
            drives = get_drives()
            response = "💾 Диски:\n\n"
            for drive in drives:
                total_gb = drive['total'] / (1024**3)
                free_gb = drive['free'] / (1024**3)
                response += (
                    f"🔹 {drive['device']}\n"
                    f"Всего: {total_gb:.1f} GB\n"
                    f"Свободно: {free_gb:.1f} GB\n"
                    f"Занято: {drive['percent']}%\n\n"
                )
            await update.effective_message.reply_text(response)
            
        elif text == get_text('language', lang):
            keyboard = get_language_keyboard()
            await update.effective_message.reply_text(
                "🌐 Выберите язык / Select language:",
                reply_markup=keyboard
            )
            
        elif text == get_text('support_author', lang):
            await update.effective_message.reply_text(
                "💰 Поддержать автора:\n\n"
                "🔗 GitHub: https://github.com/Eugeneofficial\n"
                "💳 Donation Alerts: https://www.donationalerts.com/r/eugene_official"
            )
            
    except Exception as e:
        logger.error(f"Message handler error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Произошла ошибка при выполнении команды."
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries."""
    if not update.callback_query:
        return

    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    try:
        if query.data == "shutdown":
            if shutdown_pc():
                await query.message.reply_text("⭕️ Выключение компьютера...")
            else:
                await query.message.reply_text("❌ Ошибка при выключении")
                
        elif query.data == "restart":
            if restart_pc():
                await query.message.reply_text("🔄 Перезагрузка компьютера...")
            else:
                await query.message.reply_text("❌ Ошибка при перезагрузке")
                
        elif query.data == "sleep":
            if sleep_pc():
                await query.message.reply_text("😴 Перевод компьютера в спящий режим...")
            else:
                await query.message.reply_text("❌ Ошибка при переводе в спящий режим")
                
        elif query.data == "lock":
            if lock_pc():
                await query.message.reply_text("🔒 Блокировка компьютера...")
            else:
                await query.message.reply_text("❌ Ошибка при блокировке")
                
        elif query.data.startswith("lang_"):
            lang = query.data.replace("lang_", "")
            user_id = str(update.effective_user.id)
            
            try:
                with open('bot_profiles.json', 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
            except:
                profiles = {}
                
            if user_id not in profiles:
                profiles[user_id] = {}
            profiles[user_id]['language'] = lang
            
            with open('bot_profiles.json', 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=4, ensure_ascii=False)
            
            keyboard = get_main_keyboard(lang)
            await query.message.reply_text(
                "✅ Язык успешно изменен!" if lang == "ru" else "✅ Language changed successfully!",
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        await query.message.reply_text("❌ Произошла ошибка при выполнении команды")

def setup_handlers(application: Application) -> None:
    """Setup all handlers for the application."""
    try:
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        logger.info("All handlers have been set up successfully")
    except Exception as e:
        logger.error(f"Setup Handlers error: {str(e)}")
        raise
