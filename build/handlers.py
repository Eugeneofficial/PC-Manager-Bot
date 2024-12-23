import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils import (
    load_config, save_config, get_system_info, take_screenshot,
    get_processes, kill_process, get_drives_info,
    shutdown_pc, restart_pc, sleep_pc, lock_pc,
    get_user_language, get_text
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

POWER_KEYBOARD = [
    [
        InlineKeyboardButton("🔄 Перезагрузка", callback_data="restart"),
        InlineKeyboardButton("⭕ Выключение", callback_data="shutdown"),
    ],
    [
        InlineKeyboardButton("😴 Сон", callback_data="sleep"),
        InlineKeyboardButton("🔒 Блокировка", callback_data="lock"),
    ],
    [InlineKeyboardButton("« Назад", callback_data="main_menu")],
]

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if not update.effective_message:
        return

    help_text = (
        "🤖 *Команды бота:*\n\n"
        "/start - Запустить бота\n"
        "/help - Показать это сообщение\n"
        "/search - Поиск файлов (укажите путь и маску)\n\n"
        "📱 *Доступные функции через меню:*\n\n"
        "💻 Системная информация - Показать нформацию о системе\n"
        "📁 Список файлов - Просмотр файлов в текущей директории\n"
        "📸 Скриншот - Сделать снимок экрана\n"
        "⚙️ Управление питанием - Управление питанием ПК\n"
        "📊 Процессы - Просмотр запущенных процессов\n"
        "💾 Диски - Информация о дисках\n"
    )
    
    await update.effective_message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )

async def search_files_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search command."""
    if not update.effective_message:
        return

    if not context.args or len(context.args) < 2:
        await update.effective_message.reply_text(
            "❌ Пожалуйста, укажите путь и маску поиска.\n"
            "Пример: /search C:\\Users *.txt"
        )
        return

    path = context.args[0]
    pattern = context.args[1]

    try:
        import glob
        files = glob.glob(os.path.join(path, "**", pattern), recursive=True)
        
        if not files:
            await update.effective_message.reply_text(
                f"🔍 Файлы по маске {pattern} в {path} не найдены."
            )
            return

        response = f"🔍 Найденные файлы по маске {pattern} в {path}:\n\n"
        for file in files[:10]:  # Limit to 10 files
            response += f"📄 {file}\n"
        
        if len(files) > 10:
            response += f"\n...и еще {len(files) - 10} файлов"

        await update.effective_message.reply_text(response)

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Произошла ошибка при поиске файлов.\n"
            "Проверьте путь и права доступа."
        )

async def system_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle system information request."""
    if not update.effective_message:
        return
    
    try:
        info = await get_system_info()
        await update.effective_message.reply_text(info, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"System info error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при получении систмной информации."
        )

async def file_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle file list request."""
    if not update.effective_message:
        return
    
    try:
        path = os.getcwd()
        files = os.listdir(path)
        
        response = f"📂 Файлы в директории {path}:\n\n"
        
        for item in files[:15]:  # Limit to 15 items
            if os.path.isdir(os.path.join(path, item)):
                response += f"📁 {item}/\n"
            else:
                response += f"📄 {item}\n"
                
        if len(files) > 15:
            response += f"\n...и еще {len(files) - 15} файлов"
            
        await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(f"File list error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при получении списка файлов."
        )

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle screenshot request."""
    if not update.effective_message:
        return
    
    try:
        screenshot_path = await take_screenshot()
        with open(screenshot_path, 'rb') as photo:
            await update.effective_message.reply_photo(photo)
        os.remove(screenshot_path)  # Clean up
    except Exception as e:
        logger.error(f"Screenshot error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при создании скриншота."
        )

async def power_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show power management menu."""
    if not update.effective_message:
        return

    keyboard = InlineKeyboardMarkup(POWER_KEYBOARD)
    await update.effective_message.reply_text(
        "⚙️ Управление питанием:\nВыберите действие:",
        reply_markup=keyboard
    )

async def process_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle process list request."""
    if not update.effective_message:
        return
    
    try:
        processes = get_processes()
        response = "📊 Запущенные процессы:\n\n"
        
        for proc in processes[:15]:  # Limit to 15 processes
            response += f"🔹 {proc['name']} (PID: {proc['pid']}) - {proc['memory_mb']:.1f} MB\n"
            
        if len(processes) > 15:
            response += f"\n...и еще {len(processes) - 15} процессов"
            
        await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(f"Process list error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при получении списка процессов."
        )

async def drives_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle drives information request."""
    if not update.effective_message:
        return
    
    try:
        drives = get_drives_info()
        response = "💾 Информация о дисках:\n\n"
        
        for drive in drives:
            response += (
                f"🔹 Диск {drive['device']}:\n"
                f"   Всего: {drive['total_gb']:.1f} GB\n"
                f"   Свободно: {drive['free_gb']:.1f} GB\n"
                f"   Использовано: {drive['used_percent']}%\n\n"
            )
            
        await update.effective_message.reply_text(response)
    except Exception as e:
        logger.error(f"Drives info error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при получении ин��ормации о дисках."
        )

async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle support author request."""
    if not update.effective_message:
        return
    
    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id)
    
    await update.effective_message.reply_text(
        get_text('support_text', lang),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True  # Чтобы ссылка не разворачивалась в превью
    )

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language change request."""
    if not update.effective_message:
        return
    
    keyboard = get_language_keyboard()
    await update.effective_message.reply_text(
        "🌐 Выберите язык / Select language:",
        reply_markup=keyboard
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries."""
    if not update.callback_query:
        return

    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    try:
        # Language selection
        if query.data.startswith("lang_"):
            lang = query.data.replace("lang_", "")
            user_id = str(update.effective_user.id)
            
            # Save user's language preference
            config = load_config()
            if not config:
                config = {}
            if user_id not in config:
                config[user_id] = {}
            config[user_id]['language'] = lang
            save_config(config)
            
            # Update keyboard and send message
            keyboard = get_main_keyboard(lang)
            await query.message.reply_text(
                get_text('language_selected', lang),
                reply_markup=keyboard
            )
            await query.message.delete()
            return

        # Other callbacks
        if query.data == "main_menu":
            user_id = str(update.effective_user.id)
            lang = get_user_language(user_id)
            keyboard = get_main_keyboard(lang)
            await query.message.reply_text(
                get_text('start', lang),
                reply_markup=keyboard
            )
            await query.message.delete()
        elif query.data == "power_menu":
            await power_menu_handler(update, context)
        elif query.data == "shutdown":
            await shutdown_pc(update, context)
        elif query.data == "restart":
            await restart_pc(update, context)
        elif query.data == "sleep":
            await sleep_pc(update, context)
        elif query.data == "lock":
            await lock_pc(update, context)
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        await query.message.reply_text(
            "❌ Произошла ошибка при выполнении команды."
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all non-command messages."""
    if not update.effective_message or not update.effective_message.text:
        return

    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id)
    text = update.effective_message.text

    # Handle different button presses
    if text == get_text('system_info', lang):
        await system_info_handler(update, context)
    elif text == get_text('screenshot', lang):
        await screenshot_handler(update, context)
    elif text == get_text('files', lang):
        await file_list_handler(update, context)
    elif text == get_text('processes', lang):
        await process_list_handler(update, context)
    elif text == get_text('power', lang):
        await power_menu_handler(update, context)
    elif text == get_text('drives', lang):
        await drives_info_handler(update, context)
    elif text == get_text('support_author', lang):
        await support_handler(update, context)
    elif text == get_text('language', lang):
        await language_handler(update, context)
    else:
        # Show main menu for unknown commands
        keyboard = get_main_keyboard(lang)
        await update.effective_message.reply_text(
            get_text('start', lang),
            reply_markup=keyboard
        )

async def file_transfer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle file uploads."""
    if not update.effective_message or not update.effective_message.document:
        return

    try:
        file = await context.bot.get_file(update.effective_message.document.file_id)
        filename = update.effective_message.document.file_name or "downloaded_file"
        
        # Download the file
        await file.download_to_drive(filename)
        
        await update.effective_message.reply_text(
            f"✅ Файл {filename} успешно загружен!"
        )
    except Exception as e:
        logger.error(f"File transfer error: {str(e)}")
        await update.effective_message.reply_text(
            "❌ Ошибка при загрузке файла."
        )
