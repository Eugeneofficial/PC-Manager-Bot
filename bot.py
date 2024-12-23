import json
import logging
import os
import platform
import psutil
import pyautogui
import subprocess
import sys
import time
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from functools import wraps

# Настройка логирования с выводом в консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """Загрузка конфигурации"""
    try:
        print("Загрузка конфигурации...")
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"Конфигурация загружена: {config}")
            return config
    except Exception as e:
        print(f"Ошибка ��агрузки конфига: {e}")
        logger.error(f"Ошибка загрузки конфига: {e}")
        return None

def check_auth(func):
    """Декоратор для проверки авторизации пользователя"""
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        config = load_config()
        if not config:
            logger.error("Не удалось загрузить конфигурацию")
            await update.message.reply_text("Ошибка загрузки конфигурации")
            return
            
        user_id = update.effective_user.id
        if user_id not in config['AUTHORIZED_USERS']:
            logger.warning(f"Попытка неавторизованного доступа от пользователя {user_id}")
            await update.message.reply_text("У вас нет доступа к этому боту")
            return
            
        return await func(self, update, context)
    return wrapper

class PCManagerBot:
    def __init__(self):
        self.config = load_config()
        if not self.config:
            raise ValueError("Не удалось загрузить конфигурацию")
            
        self.app = Application.builder().token(self.config['TELEGRAM_TOKEN']).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
    @check_auth
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        keyboard = [
            ['💻 Система', '📸 Скриншот', '🎥 Камера'],
            ['📊 Процессы', '🔌 Питание', '🎤 Микрофон'],
            ['💾 Диски', '📁 Файлы', '🔄 Обновить'],
            ['⚡ Админ', '⚙️ Настройки', '❌ Выключить'],
            ['🖥️ Монитор', '🔊 Громкость', '🌡️ CPU'],
            ['📶 Wi-Fi', '🔒 Блокировка', '📱 USB'],
            ['🎮 Игры', '🖨️ Принтер', '⌨️ Клавиатура'],
            ['🔍 Поиск', '📥 Загрузки', '📤 Отправить'],
            ['🎵 Музыка', '🎬 Видео', '📺 Стрим'],
            ['🔆 Яркость', '🕹️ Мышь', '📋 Буфер'],
            ['📱 Телефон', '🌐 Браузер', '📧 Почта'],
            ['⏰ Таймер', '📅 Календарь', '🔔 Напоминания'],
            ['🎨 Цвета', '🔧 Службы', '📈 Графики'],
            ['🌐 IP', '🔌 Порты', '📡 DNS'],
            ['🛡️ Firewall', '🔒 UAC', '🔑 Права'],
            ['📊 Сеть', '💽 SMART', '🔄 BIOS'],
            ['🗄️ Реестр', '📦 Пакеты', '🔧 Драйверы'],
            ['🚀 Автозагрузка', '📝 Логи', '🔍 Ошибки'],
            ['⚡ Питание', '🌡️ Сенсоры', '🔊 Аудио'],
            ['🔒 Группы', '👥 Юзеры', '🗃️ Шары']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"👋 Привет! Я бот для управления компьютером.\n"
            f"💻 Система: {platform.system()} {platform.release()}\n"
            f"🖥️ Компьютер: {platform.node()}",
            reply_markup=reply_markup
        )

    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота...")
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

if __name__ == '__main__':
    print("Запуск бота...")
    try:
        print("Инициализация PCManagerBot...")
        bot = PCManagerBot()
        print("Запуск polling...")
        bot.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)
