import dearpygui.dearpygui as dpg
import json
import os
import webbrowser
import locale
import sys
import requests
from datetime import datetime
import logging
import subprocess

VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/Eugeneofficial/PC-Manager-Bot/master/version.json"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_manager.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        # Настройка кодировки для Windows
        if sys.platform.startswith('win'):
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleCP(65001)
            kernel32.SetConsoleOutputCP(65001)
            if sys.stdout.encoding != 'utf-8':
                sys.stdout.reconfigure(encoding='utf-8')

        self.version = VERSION
        self.bot_process = None
        
        # Инициализация DPG
        dpg.create_context()
        
        # Определение языка
        self.current_lang = 'ru'
        
        # Загрузка конфигурации
        self.config = self.load_config()
        
        # Создание интерфейса
        self.setup_gui()
        
    def load_config(self):
        """Загрузка конфигурации"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'TELEGRAM_TOKEN': '', 'AUTHORIZED_USERS': []}
            
    def setup_gui(self):
        """Настройка интерфейса"""
        # Создаем viewport
        dpg.create_viewport(
            title="PC Manager Bot",
            width=800,
            height=600,
            resizable=False
        )
        
        # Основное окно
        with dpg.window(tag="main_window", label="PC Manager Bot", width=800, height=600):
            with dpg.group():
                # Поле для токена
                dpg.add_text("Telegram Bot Token:")
                dpg.add_input_text(
                    tag="token_input",
                    default_value=self.config.get('TELEGRAM_TOKEN', ''),
                    width=400
                )
                
                # Поле для ID пользователей
                dpg.add_text("Authorized User IDs:")
                dpg.add_input_text(
                    tag="user_id_input",
                    default_value=','.join(map(str, self.config.get('AUTHORIZED_USERS', []))),
                    width=400
                )
                
                # Кнопки
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Save & Start",
                        callback=self.save_and_exit,
                        width=200
                    )
                    dpg.add_button(
                        label="Clear",
                        callback=self.clear_settings,
                        width=200
                    )
        
        # Настройка и отображение viewport
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        
    def start_bot(self):
        """Запуск бота"""
        try:
            logger.info("Starting bot process...")
            # Останавливаем предыдущий процесс, если он существует
            if self.bot_process:
                self.stop_bot()
            
            # Запускаем бота в фоновом режиме
            if sys.platform.startswith('win'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                self.bot_process = subprocess.Popen(
                    [sys.executable, 'bot.py'],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.bot_process = subprocess.Popen([sys.executable, 'bot.py'])
            
            logger.info("Bot process started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False

    def stop_bot(self):
        """Остановка бота"""
        try:
            if self.bot_process:
                logger.info("Stopping bot process...")
                self.bot_process.terminate()
                self.bot_process.wait()
                self.bot_process = None
                logger.info("Bot process stopped")
        except Exception as e:
            logger.error(f"Failed to stop bot: {e}")

    def save_and_exit(self):
        """Сохранение настроек и запуск бота"""
        try:
            # Получение значений
            token = dpg.get_value("token_input").strip()
            user_ids = dpg.get_value("user_id_input").strip()
            
            # Проверка токена
            if not token:
                self.show_error("Bot token is required!")
                return
                
            # Проверка ID пользователей
            try:
                user_id_list = [int(uid.strip()) for uid in user_ids.split(',') if uid.strip()]
                if not user_id_list:
                    raise ValueError()
            except ValueError:
                self.show_error("Invalid user ID format!")
                return
                
            # Сохранение конфигурации
            config = {
                'TELEGRAM_TOKEN': token,
                'AUTHORIZED_USERS': user_id_list
            }
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            # Запускаем бота
            if self.start_bot():
                self.show_success("Settings saved and bot started successfully!")
            else:
                self.show_error("Settings saved but failed to start bot!")
            
        except Exception as e:
            logger.error(f"Save and start error: {e}")
            self.show_error(f"Error: {str(e)}")

    def clear_settings(self):
        """Очистка настроек"""
        dpg.set_value("token_input", "")
        dpg.set_value("user_id_input", "")
        
    def show_error(self, message):
        """Показ ошибки"""
        with dpg.window(
            label="Error",
            modal=True,
            no_close=True,
            width=300,
            height=100,
            pos=(250, 250)
        ) as modal_id:
            dpg.add_text(message)
            dpg.add_button(
                label="OK",
                width=-1,
                callback=lambda: dpg.delete_item(modal_id)
            )
            
    def show_success(self, message):
        """Показ успешного сообщения"""
        with dpg.window(
            label="Success",
            modal=True,
            no_close=True,
            width=300,
            height=100,
            pos=(250, 250)
        ) as modal_id:
            dpg.add_text(message)
            dpg.add_button(
                label="OK",
                width=-1,
                callback=lambda: dpg.delete_item(modal_id)
            )
            
    def run(self):
        """Запуск приложения"""
        try:
            while dpg.is_dearpygui_running():
                dpg.render_dearpygui_frame()
        finally:
            dpg.destroy_context()

if __name__ == "__main__":
    manager = BotManager()
    manager.run() 