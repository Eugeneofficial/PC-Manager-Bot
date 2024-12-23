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

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def load_config():
    """Загрузка конфигурации"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except Exception as e:
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
            # Новые кнопки для сисадмина
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
        
    @check_auth
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        text = update.message.text
        
        if text == '💻 Обновить':
            await self.start_command(update, context)
            return
            
        if text == '💻 Система':
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            await update.message.reply_text(
                f"💻 Система:\n"
                f"CPU: {cpu}%\n"
                f"RAM: {memory.percent}%\n"
                f"Диск: {disk.percent}%\n"
            )
            
        elif text == '📸 Скриншот':
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save("screenshot.png")
                await update.message.reply_photo(open("screenshot.png", "rb"))
                os.remove("screenshot.png")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
                
        elif text == '🎥 Камера':
            try:
                import cv2
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    await update.message.reply_text("❌ Камера не найдена")
                    return
                    
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite("camera.jpg", frame)
                    await update.message.reply_photo(open("camera.jpg", "rb"))
                    os.remove("camera.jpg")
                cap.release()
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
                
        elif text == '🎤 Микрофон':
            try:
                import pyaudio
                import wave
                
                audio = pyaudio.PyAudio()
                stream = audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)
                
                await update.message.reply_text("🎤 Запись звука (10 секунд)...")
                
                frames = []
                for _ in range(0, 440):
                    data = stream.read(1024, exception_on_overflow=False)
                    frames.append(data)
                
                stream.stop_stream()
                stream.close()
                audio.terminate()
                
                with wave.open("audio.wav", 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(44100)
                    wf.writeframes(b''.join(frames))
                
                await update.message.reply_audio(open("audio.wav", "rb"))
                os.remove("audio.wav")
                
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка записи звука: {str(e)}")
                
        elif text == '📊 Процессы':
            processes = []
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except:
                    pass
                    
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            text = "📊 Топ процессов по CPU:\n\n"
            
            for proc in processes[:10]:
                text += f"{proc['name']}: CPU {proc['cpu_percent']}%, RAM {proc['memory_percent']:.1f}%\n"
                
            await update.message.reply_text(text)
            
        elif text == '🔌 Питание':
            battery = psutil.sensors_battery()
            if battery:
                status = "🔌 Заряжается" if battery.power_plugged else "🔋 От батареи"
                await update.message.reply_text(
                    f"Батарея: {battery.percent}%\n"
                    f"Статус: {status}"
                )
            else:
                await update.message.reply_text("❌ Информация о батарее недоступна")
                
        elif text == '💾 Диски':
            text = "💾 Диски:\n\n"
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    text += f"{part.device}:\n"
                    text += f"Всего: {usage.total // (2**30)} GB\n"
                    text += f"Занято: {usage.used // (2**30)} GB ({usage.percent}%)\n\n"
                except:
                    pass
                    
            await update.message.reply_text(text)
            
        elif text == '📁 Файлы':
            files = os.listdir()
            text = "📁 Файлы в текущей директории:\n\n"
            
            for file in files:
                try:
                    size = os.path.getsize(file) / 1024
                    modified = datetime.fromtimestamp(os.path.getmtime(file))
                    text += f"{file}\n"
                    text += f"Размер: {size:.1f} KB\n"
                    text += f"Изменен: {modified.strftime('%d.%m.%Y %H:%M')}\n\n"
                except:
                    pass
            
            await update.message.reply_text(text)
            
        elif text == '⚡ Админ':
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if is_admin:
                    await update.message.reply_text("✅ У бота уже есть права администратора")
                else:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    await update.message.reply_text("🔄 Перезапуск с правами администратора...")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
                
        elif text == '⚙️ Настройки':
            keyboard = [
                [InlineKeyboardButton("🔊 Звук", callback_data='settings_sound'),
                 InlineKeyboardButton("🖥️ Экран", callback_data='settings_display')],
                [InlineKeyboardButton("🌐 Сеть", callback_data='settings_network'),
                 InlineKeyboardButton("⌨️ Ввод", callback_data='settings_input')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("⚙️ Настройки:", reply_markup=reply_markup)
            
        elif text == '❌ Выключить':
            keyboard = [
                [InlineKeyboardButton("✅ Да", callback_data='shutdown_yes'),
                 InlineKeyboardButton("❌ Нет", callback_data='shutdown_no')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "❗ Вы уверены, что хотите выключить компьютер?",
                reply_markup=reply_markup
            )
            
        elif text == '🔄️ Монитор':
            try:
                import win32api
                monitors = win32api.EnumDisplayMonitors()
                text = "🖥️ Мониторы:\n\n"
                for i, monitor in enumerate(monitors, 1):
                    info = win32api.GetMonitorInfo(monitor[0])
                    text += f"Монитор {i}:\n"
                    text += f"Разрешение: {info['Monitor'][2]-info['Monitor'][0]}x{info['Monitor'][3]-info['Monitor'][1]}\n"
                await update.message.reply_text(text)
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔊 Громкость':
            try:
                import winsound
                winsound.Beep(1000, 500)
                await update.message.reply_text("🔊 Проверка звука")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🌡️ CPU':
            try:
                cpu_temp = psutil.cpu_percent(interval=1, percpu=True)
                text = "🌡️ Загрузка ядер CPU:\n\n"
                for i, temp in enumerate(cpu_temp):
                    text += f"Ядро {i+1}: {temp}%\n"
                await update.message.reply_text(text)
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📶 Wi-Fi':
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📶 Wi-Fi статус:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔒 Блокировка':
            try:
                import ctypes
                ctypes.windll.user32.LockWorkStation()
                await update.message.reply_text("🔒 Компьютер заблокирован")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📱 USB':
            try:
                result = subprocess.run(['powershell', 'Get-PnpDevice | Where-Object {$_.Class -eq "USB"}'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📱 USB устройства:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🎮 Игры':
            games_dir = os.path.join(os.environ['ProgramFiles(x86)'], 'Steam', 'steamapps', 'common')
            if os.path.exists(games_dir):
                games = os.listdir(games_dir)
                text = "🎮 Установленные игры:\n\n"
                for game in games[:10]:
                    text += f"• {game}\n"
                await update.message.reply_text(text)
            else:
                await update.message.reply_text("❌ Steam не найден")

        elif text == '🖨️ Принтер':
            try:
                import win32print
                printer = win32print.GetDefaultPrinter()
                await update.message.reply_text(f"🖨️ Принтер по умолчанию:\n{printer}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '⌨️ Клавиатура':
            try:
                result = subprocess.run(['powershell', 'Get-WinUserLanguageList'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"⌨️ Раскладка клавиатуры:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔍 Поиск':
            try:
                result = subprocess.run(['where', '*.*'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔍 Найденные файлы:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '���� Загрузки':
            downloads = os.path.expanduser('~\\Downloads')
            if os.path.exists(downloads):
                files = os.listdir(downloads)
                text = "📥 Последние загрузки:\n\n"
                for file in sorted(files, key=lambda x: os.path.getmtime(os.path.join(downloads, x)), reverse=True)[:10]:
                    size = os.path.getsize(os.path.join(downloads, file)) / (1024*1024)
                    text += f"• {file} ({size:.1f} MB)\n"
                await update.message.reply_text(text)
            else:
                await update.message.reply_text("❌ Папка загрузок не найдена")

        elif text == '📤 Отправить':
            try:
                result = subprocess.run(['powershell', 'Get-SmbShare'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📤 Общие папки:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🎵 Музыка':
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys(chr(0xB3))
                await update.message.reply_text("🎵 Переключение воспроизведения")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🎬 Видео':
            videos = os.path.expanduser('~\\Videos')
            if os.path.exists(videos):
                files = [f for f in os.listdir(videos) if f.endswith(('.mp4', '.avi', '.mkv'))]
                text = "🎬 Видеофайлы:\n\n"
                for file in files[:10]:
                    size = os.path.getsize(os.path.join(videos, file)) / (1024*1024)
                    text += f"• {file} ({size:.1f} MB)\n"
                await update.message.reply_text(text)
            else:
                await update.message.reply_text("❌ Папка видео не найдена")

        elif text == '📺 Стрим':
            try:
                import cv2
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    await update.message.reply_text("❌ Камера не найдена")
                    return
                    
                await update.message.reply_text("📺 Начинаю стрим (10 кадров)...")
                for _ in range(10):
                    ret, frame = cap.read()
                    if ret:
                        cv2.imwrite("stream.jpg", frame)
                        await update.message.reply_photo(open("stream.jpg", "rb"))
                        os.remove("stream.jpg")
                    time.sleep(1)
                cap.release()
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔆 Яркость':
            try:
                result = subprocess.run(['powershell', '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔆 Текущая яркость:\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🕹️ Мышь':
            try:
                x, y = pyautogui.position()
                await update.message.reply_text(f"🕹️ Позиция мыши: X={x}, Y={y}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📋 Буфер':
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                data = win32clipboard.GetClipboardData() if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT) else "Буфер пуст"
                win32clipboard.CloseClipboard()
                await update.message.reply_text(f"📋 Содержимое буфера обмена:\n\n{data[:1000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📱 Телефон':
            try:
                result = subprocess.run(['powershell', 'Get-PnpDevice | Where-Object {$_.Class -eq "Portable Devices"}'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📱 Подключенные устройства:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🌐 Браузер':
            try:
                import webbrowser
                webbrowser.open('https://www.google.com')
                await update.message.reply_text("🌐 Браузер открыт")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📧 Почта':
            try:
                import webbrowser
                webbrowser.open('mailto:')
                await update.message.reply_text("📧 Почтовый клиент открыт")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '⏰ Таймер':
            try:
                await update.message.reply_text("⏰ Таймер на 5 секунд...")
                time.sleep(5)
                await update.message.reply_text("⏰ Время вышло!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📅 Календарь':
            try:
                from datetime import date
                today = date.today()
                await update.message.reply_text(f"📅 Сегодня: {today.strftime('%d.%m.%Y')}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔔 Напоминания':
            try:
                result = subprocess.run(['schtasks', '/query'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔔 Запланированные задачи:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🎨 Цвета':
            try:
                color = pyautogui.pixel(*pyautogui.position())
                await update.message.reply_text(f"🎨 Цвет под курсором: RGB{color}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔧 Службы':
            try:
                result = subprocess.run(['net', 'start'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔧 Запущенные службы:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📈 Графики':
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                text = "📈 Статистика:\n\n"
                text += f"CPU: {'█' * int(cpu_percent/10)}{' ' * (10-int(cpu_percent/10))} {cpu_percent}%\n"
                text += f"RAM: {'█' * int(memory.percent/10)}{' ' * (10-int(memory.percent/10))} {memory.percent}%\n"
                text += f"Диск: {'█' * int(disk.percent/10)}{' ' * (10-int(disk.percent/10))} {disk.percent}%"
                await update.message.reply_text(text)
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🌐 IP':
            try:
                result = subprocess.run(['ipconfig', '/all'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🌐 Сетевые настройки:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔌 Порты':
            try:
                result = subprocess.run(['netstat', '-ano'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔌 Открытые порты:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📡 DNS':
            try:
                result = subprocess.run(['ipconfig', '/displaydns'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📡 DNS кэш:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🛡️ Firewall':
            try:
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🛡️ Состояние брандмауэра:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔒 UAC':
            try:
                result = subprocess.run(['reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', '/v', 'EnableLUA'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔒 Статус UAC:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔑 Права':
            try:
                result = subprocess.run(['whoami', '/all'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔑 Права доступа:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📊 Сеть':
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'all'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📊 Состояние сети:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '💽 SMART':
            try:
                result = subprocess.run(['wmic', 'diskdrive', 'get', 'status,caption,size'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"💽 SMART статус дисков:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔄 BIOS':
            try:
                result = subprocess.run(['wmic', 'bios', 'get', 'manufacturer,version,serialnumber'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔄 Информация о BIOS:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🗄️ Реестр':
            try:
                result = subprocess.run(['reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🗄️ Автозагрузка в реестре:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📦 Пакеты':
            try:
                result = subprocess.run(['wmic', 'product', 'get', 'name,version'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📦 Установленные программы:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔧 Драйверы':
            try:
                result = subprocess.run(['driverquery'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔧 Установленные драйверы:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🚀 Автозагрузка':
            try:
                result = subprocess.run(['wmic', 'startup', 'get', 'caption,command'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🚀 Программы в автозагрузке:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '📝 Логи':
            try:
                result = subprocess.run(['wevtutil', 'qe', 'System', '/c:5', '/f:text'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"📝 Последние системные события:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔍 Ошибки':
            try:
                result = subprocess.run(['wevtutil', 'qe', 'System', '/q:*[System[(Level=2)]]', '/c:5', '/f:text'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔍 Последние ошибки системы:\n\n{result.stdout[:2000]}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '⚡ Питание':
            try:
                result = subprocess.run(['powercfg', '/list'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"⚡ Схемы питания:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🌡️ Сенсоры':
            try:
                result = subprocess.run(['wmic', 'temperature', 'get', 'currentreading,instancename'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🌡️ Показания датчиков:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔊 Аудио':
            try:
                result = subprocess.run(['powershell', 'Get-AudioDevice'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔊 Аудиоустройства:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🔒 Группы':
            try:
                result = subprocess.run(['net', 'localgroup'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🔒 Локальные группы:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '👥 Юзеры':
            try:
                result = subprocess.run(['net', 'user'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"👥 Локальные пользователи:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")

        elif text == '🗃️ Шары':
            try:
                result = subprocess.run(['net', 'share'], 
                                     capture_output=True, text=True, encoding='cp866')
                await update.message.reply_text(f"🗃️ Сетевые ресурсы:\n\n{result.stdout}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик callback-запросов"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'shutdown_yes':
            await query.edit_message_text("🔄 Выключение компьютера...")
            os.system('shutdown /s /t 0')
        elif query.data == 'shutdown_no':
            await query.edit_message_text("❌ Выключение отменено")
        elif query.data.startswith('settings_'):
            setting = query.data.split('_')[1]
            if setting == 'sound':
                await query.edit_message_text("🔊 Настройки звука пока недоступны")
            elif setting == 'display':
                await query.edit_message_text("🖥️ Настройки экрана пока недоступны")
            elif setting == 'network':
                await query.edit_message_text("🌐 Настройки сети пока недоступны")
            elif setting == 'input':
                await query.edit_message_text("⌨️ Настройки ввода пока недоступны")
        
    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота...")
        try:
            self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise

if __name__ == '__main__':
    try:
        bot = PCManagerBot()
        bot.run()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)
