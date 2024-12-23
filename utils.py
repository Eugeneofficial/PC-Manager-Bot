import os
import psutil
import platform
import logging
from datetime import datetime
import asyncio
from typing import Dict, List, Any, Optional
import mss
import mss.tools
import ctypes
from PIL import Image

from translations import TRANSLATIONS

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    try:
        import json
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
    return {}

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to config.json"""
    try:
        import json
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving config: {e}")

def get_user_language(user_id: str) -> str:
    """Get user's preferred language."""
    try:
        config = load_config()
        if config and user_id in config:
            return config[user_id].get('language', 'ru')
    except Exception as e:
        logger.error(f"Error getting user language: {e}")
    return 'ru'

def get_text(key: str, lang: str) -> str:
    """Get translated text."""
    try:
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]
        return TRANSLATIONS['ru'][key]
    except Exception as e:
        logger.error(f"Error getting translation: {e}")
        return key

async def get_system_info() -> str:
    """Get system information."""
    try:
        # CPU Info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        # Memory Info
        memory = psutil.virtual_memory()
        
        # Disk Info
        disk = psutil.disk_usage('/')
        
        # System Info
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        info = (
            "💻 *Системная информация:*\n\n"
            f"🖥 *Процессор:*\n"
            f"├ Загрузка: {cpu_percent}%\n"
            f"├ Частота: {cpu_freq.current:.1f} МГц\n"
            f"└ Ядра: {cpu_count}\n\n"
            f"🧠 *Память:*\n"
            f"├ Всего: {memory.total / (1024**3):.1f} ГБ\n"
            f"├ Использовано: {memory.used / (1024**3):.1f} ГБ\n"
            f"└ Свободно: {memory.available / (1024**3):.1f} ГБ\n\n"
            f"💾 *Диск:*\n"
            f"├ Всего: {disk.total / (1024**3):.1f} ГБ\n"
            f"├ Использовано: {disk.used / (1024**3):.1f} ГБ\n"
            f"└ Свободно: {disk.free / (1024**3):.1f} ГБ\n\n"
            f"⏰ *Время работы:* {str(uptime).split('.')[0]}\n"
            f"🔄 *Загружен:* {boot_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        return info
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        raise

async def take_screenshot() -> str:
    """Take a screenshot and return the path to the saved image."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'screenshot_{timestamp}.png'
        
        with mss.mss() as sct:
            # Get the first monitor
            monitor = sct.monitors[1]
            
            # Take the screenshot
            screenshot = sct.grab(monitor)
            
            # Save it
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
        
        return filename
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise

def get_processes() -> List[Dict[str, Any]]:
    """Get list of running processes."""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'memory_mb': pinfo['memory_info'].rss / (1024 * 1024)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by memory usage
        return sorted(processes, key=lambda x: x['memory_mb'], reverse=True)
    except Exception as e:
        logger.error(f"Error getting processes: {e}")
        raise

def kill_process(pid: int) -> bool:
    """Kill a process by PID."""
    try:
        process = psutil.Process(pid)
        process.kill()
        return True
    except Exception as e:
        logger.error(f"Error killing process {pid}: {e}")
        return False

def get_drives_info() -> List[Dict[str, Any]]:
    """Get information about all drives."""
    try:
        drives = []
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            if os.name == 'nt':
                if 'cdrom' in partition.opts or partition.fstype == '':
                    continue
            
            usage = psutil.disk_usage(partition.mountpoint)
            drives.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'used_percent': usage.percent
            })
        
        return drives
    except Exception as e:
        logger.error(f"Error getting drives info: {e}")
        raise

async def shutdown_pc(update: Any, context: Any) -> None:
    """Shutdown the computer."""
    try:
        await update.callback_query.message.reply_text("💤 Выключение компьютера...")
        if os.name == 'nt':
            os.system('shutdown /s /t 1')
        else:
            os.system('shutdown -h now')
    except Exception as e:
        logger.error(f"Error shutting down: {e}")
        await update.callback_query.message.reply_text("❌ Ошибка при выключении.")

async def restart_pc(update: Any, context: Any) -> None:
    """Restart the computer."""
    try:
        await update.callback_query.message.reply_text("🔄 Перезагрузка компьютера...")
        if os.name == 'nt':
            os.system('shutdown /r /t 1')
        else:
            os.system('shutdown -r now')
    except Exception as e:
        logger.error(f"Error restarting: {e}")
        await update.callback_query.message.reply_text("❌ Ошибка при перезагрузке.")

async def sleep_pc(update: Any, context: Any) -> None:
    """Put the computer to sleep."""
    try:
        await update.callback_query.message.reply_text("😴 Перевод компьютера в спящий режим...")
        if os.name == 'nt':
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        else:
            os.system('systemctl suspend')
    except Exception as e:
        logger.error(f"Error sleeping: {e}")
        await update.callback_query.message.reply_text("❌ Ошибка при переходе в спящий режим.")

async def lock_pc(update: Any, context: Any) -> None:
    """Lock the computer."""
    try:
        await update.callback_query.message.reply_text("🔒 Блокировка компьютера...")
        if os.name == 'nt':
            ctypes.windll.user32.LockWorkStation()
        else:
            os.system('loginctl lock-session')
    except Exception as e:
        logger.error(f"Error locking: {e}")
        await update.callback_query.message.reply_text("❌ Ошибка при блокировке.")
