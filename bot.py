import os
import json
import logging
import platform
import psutil
import shutil
import socket
import requests
import subprocess
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def load_config():
    """Загрузка конфигурации"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_main_keyboard():
    """Создает основную клавиатуру"""
    keyboard = [
        [KeyboardButton("💻 Система"), KeyboardButton("📸 Скриншот")],
        [KeyboardButton("📊 Процессы"), KeyboardButton("🔌 Питание")],
        [KeyboardButton("💾 Диски"), KeyboardButton("📁 Файлы")],
        [KeyboardButton("📦 Архивация"), KeyboardButton("🌐 IP адрес")],
        [KeyboardButton("▶️ Запуск EXE")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_power_keyboard():
    """Создает клавиатуру управления питанием"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Перезагрузка", callback_data="restart"),
            InlineKeyboardButton("⭕️ Выключение", callback_data="shutdown")
        ],
        [
            InlineKeyboardButton("😴 Сон", callback_data="sleep"),
            InlineKeyboardButton("🔒 Блокировка", callback_data="lock")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    config = load_config()
    if not config or update.effective_user.id not in config.get('AUTHORIZED_USERS', []):
        await update.message.reply_text("⚠️ У вас нет прав для использования этого бота.")
        return

    await update.message.reply_text(
        "*PC Manager Bot*\n\nВыберите действие:",
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    config = load_config()
    if not config or update.effective_user.id not in config.get('AUTHORIZED_USERS', []):
        await update.message.reply_text("⚠️ У вас нет прав для использования этого бота.")
        return

    text = update.message.text
    
    if text == "💻 Система":
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            response = (
                "*Системная информация*\n\n"
                f"🖥 *Платформа:* `{platform.platform()}`\n"
                f"⚡️ *Процессор:* `{platform.processor()}`\n"
                f"🧮 *Ядер:* `{psutil.cpu_count()}`\n"
                f"📊 *Загрузка CPU:* `{cpu_percent}%`\n\n"
                f"🎮 *Память:*\n"
                f"Всего: `{memory.total / (1024**3):.1f} GB`\n"
                f"Использовано: `{memory.percent}%`\n\n"
                f"💾 *Диск C:*\n"
                f"Всего: `{disk.total / (1024**3):.1f} GB`\n"
                f"Использовано: `{disk.percent}%`"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    elif text == "📸 Скриншот":
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            with open("screenshot.png", 'rb') as photo:
                await update.message.reply_photo(photo)
            os.remove("screenshot.png")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    elif text == "📊 Процессы":
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if pinfo['cpu_percent'] > 0:
                        processes.append(pinfo)
                except:
                    pass
                    
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            response = "*Активные процессы*\n\n"
            for proc in processes[:10]:
                response += f"🔹 `{proc['name']}`\n" \
                           f"CPU: `{proc['cpu_percent']:.1f}%` | RAM: `{proc['memory_percent']:.1f}%`\n\n"
                           
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    elif text == "🔌 Питание":
        await update.message.reply_text(
            "*Управление питанием*\nВыберите действие:",
            reply_markup=get_power_keyboard(),
            parse_mode='Markdown'
        )
        
    elif text == "💾 Диски":
        try:
            response = "*Информация о дисках*\n\n"
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    response += f"🔹 *{partition.device}*\n" \
                               f"Всего: `{usage.total / (1024**3):.1f} GB`\n" \
                               f"Свободно: `{usage.free / (1024**3):.1f} GB`\n" \
                               f"Занято: `{usage.percent}%`\n\n"
                except:
                    pass
                    
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    elif text == "📁 Файлы":
        try:
            path = os.getcwd()
            files = os.listdir(path)
            
            response = f"*Текущая папка:* `{path}`\n\n"
            for item in files[:15]:
                if os.path.isdir(os.path.join(path, item)):
                    response += f"📁 `{item}/`\n"
                else:
                    response += f"📄 `{item}`\n"
                    
            if len(files) > 15:
                response += f"\n...и еще {len(files) - 15} файлов"
                
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    elif text == "📦 Архивация":
        await update.message.reply_text(
            "Отправьте путь к папке, которую нужно архивировать.\n"
            "Например: `C:\\Files\\MyFolder`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'archive_path'
        
    elif text == "🌐 IP адрес":
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            external_ip = requests.get('https://api.ipify.org').text
            
            response = (
                "*Сетевая информация*\n\n"
                f"🖥 *Имя компьютера:* `{hostname}`\n"
                f"🏠 *Локальный IP:* `{local_ip}`\n"
                f"🌍 *Внешний IP:* `{external_ip}`"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        
    elif text == "▶️ Запуск EXE":
        await update.message.reply_text(
            "Отправьте путь к EXE файлу для запуска.\n"
            "Например: `C:\\Program Files\\App\\program.exe`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'exe_path'
        
    elif 'waiting_for' in context.user_data:
        if context.user_data['waiting_for'] == 'archive_path':
            if os.path.exists(text) and os.path.isdir(text):
                try:
                    archive_name = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                    archive_path = os.path.join(os.getcwd(), archive_name)
                    shutil.make_archive(archive_path[:-4], 'zip', text)
                    
                    with open(archive_path, 'rb') as f:
                        await update.message.reply_document(f)
                    os.remove(archive_path)
                except Exception as e:
                    await update.message.reply_text(f"❌ Ошибка при создании архива: {str(e)}")
            else:
                await update.message.reply_text("❌ Указанная папка не существует")
                
        elif context.user_data['waiting_for'] == 'exe_path':
            if os.path.exists(text) and text.lower().endswith('.exe'):
                try:
                    subprocess.Popen(text)
                    await update.message.reply_text("✅ Программа запущена")
                except Exception as e:
                    await update.message.reply_text(f"❌ Ошибка при запуске программы: {str(e)}")
            else:
                await update.message.reply_text("❌ Указанный файл не существует или не является EXE")
                
        del context.user_data['waiting_for']

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "shutdown":
            os.system('shutdown /s /t 1')
            await query.message.reply_text("⭕️ Выключение компьютера...")
            
        elif query.data == "restart":
            os.system('shutdown /r /t 1')
            await query.message.reply_text("🔄 Перезагрузка компьютера...")
            
        elif query.data == "sleep":
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            await query.message.reply_text("😴 Перевод компьютера в спящий режим...")
            
        elif query.data == "lock":
            os.system('rundll32.exe user32.dll,LockWorkStation')
            await query.message.reply_text("🔒 Блокировка компьютера...")
            
    except Exception as e:
        await query.message.reply_text(f"❌ Ошибка: {str(e)}")

def main():
    """Запуск бота"""
    config = load_config()
    if not config:
        print("Ошибка загрузки конфигурации!")
        return

    app = Application.builder().token(config['TELEGRAM_TOKEN']).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
