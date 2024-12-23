import os
import json
import psutil
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import subprocess
from threading import Thread
import time

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC Manager Bot")
        self.root.geometry("800x600")
        
        # Создаем главный контейнер
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Создаем вкладки
        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка плагинов
        self.plugins_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.plugins_frame, text="Плагины")
        
        # Вкладка статуса
        self.status_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.status_frame, text="Статус")
        
        # Вкладка логов
        self.logs_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.logs_frame, text="Логи")
        
        # Инициализация компонентов
        self.setup_plugins_tab()
        self.setup_status_tab()
        self.setup_logs_tab()
        
        # Запускаем обновление статуса и логов
        self.update_thread = Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
    def setup_plugins_tab(self):
        # Фрейм для списка плагинов
        plugins_list_frame = ttk.LabelFrame(self.plugins_frame, text="Доступные плагины", padding="5")
        plugins_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Создаем и размещаем чекбоксы для плагинов
        self.plugin_vars = {}
        for i, plugin in enumerate(self.get_available_plugins()):
            var = tk.BooleanVar(value=plugin['enabled'])
            self.plugin_vars[plugin['name']] = var
            ttk.Checkbutton(plugins_list_frame, text=plugin['name'], 
                          variable=var).grid(row=i, column=0, sticky=tk.W)
        
        # Кнопки управления
        buttons_frame = ttk.Frame(self.plugins_frame)
        buttons_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(buttons_frame, text="Сохранить", 
                  command=self.save_plugins).grid(row=0, column=0, padx=5)
        
        self.start_stop_btn = ttk.Button(buttons_frame, text="Запустить бота", 
                                       command=self.toggle_bot)
        self.start_stop_btn.grid(row=0, column=1, padx=5)
        
    def setup_status_tab(self):
        # Создаем виджеты для отображения статуса
        self.status_text = scrolledtext.ScrolledText(self.status_frame, height=10, width=50)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.status_text.config(state='disabled')
        
    def setup_logs_tab(self):
        # Создаем виджет для отображения логов
        self.log_text = scrolledtext.ScrolledText(self.logs_frame, height=20, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.log_text.config(state='disabled')
        
    def get_available_plugins(self):
        plugins = []
        plugins_dir = 'plugins'
        
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)
            
        config = self.load_config()
        enabled_plugins = config.get('ENABLED_PLUGINS', [])
        
        for file in os.listdir(plugins_dir):
            if file.endswith('.py') and not file.startswith('__'):
                plugin_name = file[:-3]
                plugins.append({
                    'name': plugin_name,
                    'enabled': plugin_name in enabled_plugins
                })
        
        return plugins
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки конфига: {e}")
            return {
                'TELEGRAM_TOKEN': '',
                'AUTHORIZED_USERS': [0],
                'ENABLED_PLUGINS': []
            }
            
    def save_config(self, data):
        try:
            config = self.load_config()
            config['ENABLED_PLUGINS'] = data.get('plugins', [])
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфига: {e}")
            return False
            
    def save_plugins(self):
        enabled_plugins = [name for name, var in self.plugin_vars.items() if var.get()]
        self.save_config({'plugins': enabled_plugins})
        
    def get_bot_status(self):
        status = {
            'running': False,
            'pid': None,
            'cpu': 0,
            'memory': 0,
            'uptime': ''
        }
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                if 'python' in proc.info['name'].lower() and 'bot.py' in ' '.join(proc.cmdline()):
                    status['running'] = True
                    status['pid'] = proc.info['pid']
                    p = psutil.Process(proc.info['pid'])
                    status['cpu'] = p.cpu_percent()
                    status['memory'] = p.memory_percent()
                    uptime = datetime.now() - datetime.fromtimestamp(proc.info['create_time'])
                    hours, remainder = divmod(uptime.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    status['uptime'] = f"{uptime.days}д {hours}ч {minutes}м {seconds}с"
                    break
        except:
            pass
            
        return status
        
    def get_logs(self, lines=50):
        try:
            with open('bot.log', 'r', encoding='utf-8') as f:
                return f.readlines()[-lines:]
        except:
            return []
            
    def kill_bot(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'python' in proc.info['name'].lower() and 'bot.py' in ' '.join(proc.cmdline()):
                    proc.kill()
        except Exception as e:
            print(f"Ошибка при остановке бота: {e}")
            
    def start_bot(self):
        try:
            self.kill_bot()  # На всякий случай убиваем старый процесс
            subprocess.Popen(['python', 'bot.py'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            print(f"Ошибка запуска бота: {e}")
            
    def toggle_bot(self):
        status = self.get_bot_status()
        if status['running']:
            self.kill_bot()
            self.start_stop_btn.config(text="Запустить бота")
        else:
            self.start_bot()
            self.start_stop_btn.config(text="Остановить бота")
            
    def update_status_text(self):
        status = self.get_bot_status()
        
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        
        status_str = f"Состояние: {'Работает' if status['running'] else 'Остановлен'}\n"
        if status['running']:
            status_str += f"PID: {status['pid']}\n"
            status_str += f"CPU: {status['cpu']:.1f}%\n"
            status_str += f"RAM: {status['memory']:.1f}%\n"
            status_str += f"Время работы: {status['uptime']}"
            
        self.status_text.insert(tk.END, status_str)
        self.status_text.config(state='disabled')
        
        # Обновляем текст кнопки
        self.start_stop_btn.config(
            text="Остановить бота" if status['running'] else "Запустить бота"
        )
            
    def update_logs_text(self):
        logs = self.get_logs()
        
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, ''.join(logs))
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)  # Прокрутка к последней строке
            
    def update_loop(self):
        while True:
            self.update_status_text()
            self.update_logs_text()
            time.sleep(1)  # Обновляем каждую секунду
            
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    gui = BotGUI()
    gui.run() 