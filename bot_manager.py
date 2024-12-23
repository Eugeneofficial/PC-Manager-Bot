import dearpygui.dearpygui as dpg
import json
import os
import webbrowser
import locale
import sys
import requests
from datetime import datetime
from packaging import version

VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/your_username/your_repo/main/version.json"  # Замените на вашу ссылку

def fix_text(text):
    """Исправление кодировки текста"""
    try:
        if isinstance(text, bytes):
            return text.decode('utf-8')
        return text
    except:
        return text

class BotManager:
    def __init__(self):
        if sys.platform.startswith('win'):
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleCP(65001)
            kernel32.SetConsoleOutputCP(65001)
            if sys.stdout.encoding != 'utf-8':
                sys.stdout.reconfigure(encoding='utf-8')

        self.version = VERSION
        self.bot_process = None
        dpg.create_context()
        
        # Определение текущего языка системы
        try:
            system_lang = locale.getdefaultlocale()[0][:2]
            self.current_lang = 'ru' if system_lang == 'ru' else 'en'
        except:
            self.current_lang = 'en'
        
        # Базовые тексты
        self.texts = {
            'ru': {
                'title': u'Управление ботом',
                'setup': u'Настройка',
                'stats': u'Статистика',
                'admin': u'Админ панель',
                'bot_token': u'Токен бота:',
                'user_id': u'ID пользователей:',
                'get_token': u'Получить токен',
                'get_id': u'Получить ID',
                'save': u'Сохранить',
                'clear': u'Очистить',
                'stats_title': u'Статистика использования:',
                'total_cmds': u'Всего команд:',
                'last_active': u'Последняя активность:',
                'popular_cmds': u'Популярные команды:',
                'admin_actions': u'Действия:',
                'restart': u'Перезапустить бота',
                'stop': u'Остановить бота',
                'clear_logs': u'Очистить логи',
                'logs': u'Логи:',
                'refresh': u'Обновить',
                'token_required': u'Требуется токен бота!',
                'id_required': u'Требуется ID пользователя!',
                'invalid_id': u'Неверный формат ID!',
                'save_success': u'Настройки сохранены!\nЗапуск бота...',
                'error': u'Ошибка',
                'success': u'Успешно',
                'no_stats': u'Статистика недоступна'
            },
            'en': {
                'title': 'Bot Manager',
                'setup': 'Setup',
                'stats': 'Statistics',
                'admin': 'Admin Panel',
                'bot_token': 'Bot Token:',
                'user_id': 'User IDs:',
                'get_token': 'Get Token',
                'get_id': 'Get ID',
                'save': 'Save',
                'clear': 'Clear',
                'stats_title': 'Usage Statistics:',
                'total_cmds': 'Total Commands:',
                'last_active': 'Last Activity:',
                'popular_cmds': 'Popular Commands:',
                'admin_actions': 'Actions:',
                'restart': 'Restart Bot',
                'stop': 'Stop Bot',
                'clear_logs': 'Clear Logs',
                'logs': 'Logs:',
                'refresh': 'Refresh',
                'token_required': 'Bot token is required!',
                'id_required': 'User ID is required!',
                'invalid_id': 'Invalid ID format!',
                'save_success': 'Settings saved!\nStarting bot...',
                'error': 'Error',
                'success': 'Success',
                'no_stats': 'Statistics not available'
            }
        }
        
        # Добавляем новые строки для обновлений
        self.texts['ru'].update({
            'version': u'Версия:',
            'checking_updates': u'Проверка обновлений...',
            'update_available': u'Доступно обновление {}! Скачать?',
            'no_updates': u'Обновлений нет',
            'update_error': u'Ошибка проверки обновлений',
            'download': u'Скачать',
            'bot_status': u'Статус бота:',
            'bot_running': u'Работает',
            'bot_stopped': u'Остановлен'
        })
        
        self.texts['en'].update({
            'version': 'Version:',
            'checking_updates': 'Checking for updates...',
            'update_available': 'Update {} available! Download?',
            'no_updates': 'No updates available',
            'update_error': 'Update check failed',
            'download': 'Download',
            'bot_status': 'Bot status:',
            'bot_running': 'Running',
            'bot_stopped': 'Stopped'
        })
        
        # Загрузка конфигурации
        self.config = self.load_config()
        
        # Создание интерфейса
        self.setup_gui()
        
        # Запускаем проверку обновлений
        self.check_updates()
        
    def check_updates(self):
        """Проверка обновлений"""
        try:
            dpg.set_value("update_status", self.get_text('checking_updates'))
            response = requests.get(UPDATE_URL)
            if response.status_code == 200:
                latest = response.json()
                if version.parse(latest['version']) > version.parse(self.version):
                    self.show_update_dialog(latest['version'], latest['download_url'])
                else:
                    dpg.set_value("update_status", f"{self.get_text('version')} {self.version} ({self.get_text('no_updates')})")
        except Exception as e:
            dpg.set_value("update_status", f"{self.get_text('update_error')}: {str(e)}")
    
    def show_update_dialog(self, new_version, download_url):
        """Показ диалога обновления"""
        with dpg.window(
            label=self.get_text('update_available').format(new_version),
            modal=True,
            no_close=True,
            width=300,
            height=100,
            pos=(350, 250)
        ) as modal_id:
            dpg.add_button(
                label=self.get_text('download'),
                width=-1,
                callback=lambda: [webbrowser.open(download_url), dpg.delete_item(modal_id)]
            )
            dpg.add_button(
                label="OK",
                width=-1,
                callback=lambda: dpg.delete_item(modal_id)
            )
    
    def setup_gui(self):
        # Создаем шрифт для поддержки кириллицы
        with dpg.font_registry():
            # Основной шрифт
            with dpg.font("C:\\Windows\\Fonts\\segoeuib.ttf", 16) as default_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            
            # Шрифт для заголовка
            with dpg.font("C:\\Windows\\Fonts\\segoeuib.ttf", 20) as title_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            
        # Создаем viewport
        dpg.create_viewport(
            title="PC Manager Bot",  # Используем английское название для заголовка окна
            width=1000,
            height=600,
            resizable=False
        )
        
        # Применяем основной шрифт
        dpg.bind_font(default_font)
        
        # Настройка темы
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Цвета
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (45, 45, 45))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (45, 45, 45))
                dpg.add_theme_color(dpg.mvThemeCol_Tab, (35, 35, 35))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (45, 45, 45))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (40, 40, 40))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 45, 45))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (55, 55, 55))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (65, 65, 65))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 35))
                dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (55, 55, 55))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (45, 45, 45))
                
                # Стили
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 15)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 6)
        
        dpg.bind_theme(global_theme)
        
        # Основное окно
        with dpg.window(
            label=self.get_text('title'),
            tag="main_window",
            width=1000,
            height=600,
            pos=(0, 0),
            no_move=True,
            no_resize=True,
            no_collapse=True,
            no_close=True
        ):
            # Добавляем статус обновлений и бота в верхней части
            with dpg.group(horizontal=True):
                dpg.add_text(tag="update_status", default_value=f"{self.get_text('version')} {self.version}")
                dpg.add_button(
                    label=self.get_text('refresh'),
                    callback=self.check_updates,
                    width=100,
                    height=25
                )
                dpg.add_spacer(width=20)
                dpg.add_text(self.get_text('bot_status'))
                dpg.add_text(tag="bot_status", default_value=self.get_text('bot_stopped'))
            
            dpg.add_separator()
            
            with dpg.tab_bar():
                # Вкладка настроек
                with dpg.tab(label=self.get_text('setup')):
                    with dpg.group(horizontal=True):
                        # Левая колонка
                        with dpg.child_window(width=450, height=500):
                            dpg.add_text(self.get_text('bot_token'))
                            dpg.add_input_text(
                                tag="token_input",
                                width=-1,
                                default_value=self.config.get('TELEGRAM_TOKEN', '')
                            )
                            dpg.add_button(
                                label=self.get_text('get_token'),
                                callback=lambda: webbrowser.open('https://t.me/botfather'),
                                width=-1,
                                height=25
                            )
                            
                            dpg.add_spacer(height=20)
                            
                            dpg.add_text(self.get_text('user_id'))
                            dpg.add_input_text(
                                tag="user_id_input",
                                width=-1,
                                default_value=','.join(map(str, self.config.get('AUTHORIZED_USERS', [])))
                            )
                            dpg.add_button(
                                label=self.get_text('get_id'),
                                callback=lambda: webbrowser.open('https://t.me/userinfobot'),
                                width=-1,
                                height=25
                            )
                            
                            dpg.add_spacer(height=20)
                            
                            with dpg.group(horizontal=True):
                                dpg.add_button(
                                    label=self.get_text('save'),
                                    callback=self.save_and_exit,
                                    width=200,
                                    height=30
                                )
                                dpg.add_button(
                                    label=self.get_text('clear'),
                                    callback=self.clear_settings,
                                    width=200,
                                    height=30
                                )
                
                # Вкладка статистики
                with dpg.tab(label=self.get_text('stats')):
                    with dpg.child_window(width=-1, height=500):
                        dpg.add_text(self.get_text('stats_title'), color=(200, 200, 200))
                        dpg.add_text(tag="stats_text", wrap=900)
                        dpg.add_button(
                            label=self.get_text('refresh'),
                            callback=self.update_statistics,
                            width=150,
                            height=25
                        )
                
                # Вкладка админ-панели
                with dpg.tab(label=self.get_text('admin')):
                    with dpg.group(horizontal=True):
                        # Левая колонка (действия)
                        with dpg.child_window(width=200, height=500):
                            dpg.add_text(self.get_text('admin_actions'), color=(200, 200, 200))
                            dpg.add_button(
                                label=self.get_text('restart'),
                                callback=self.restart_bot,
                                width=-1,
                                height=30
                            )
                            dpg.add_button(
                                label=self.get_text('stop'),
                                callback=self.stop_bot,
                                width=-1,
                                height=30
                            )
                            dpg.add_button(
                                label=self.get_text('clear_logs'),
                                callback=self.clear_logs,
                                width=-1,
                                height=30
                            )
                        
                        # Правая колонка (логи)
                        with dpg.child_window(width=-1, height=500):
                            dpg.add_text(self.get_text('logs'), color=(200, 200, 200))
                            dpg.add_input_text(
                                tag="log_viewer",
                                multiline=True,
                                readonly=True,
                                width=-1,
                                height=400
                            )
                            dpg.add_button(
                                label=self.get_text('refresh'),
                                callback=self.update_logs,
                                width=150,
                                height=25
                            )
        
        # Инициализация данных
        self.update_statistics()
        self.update_logs()
        
        # Настройка и отображение viewport
        dpg.setup_dearpygui()
        dpg.show_viewport()
        
        # Центрирование окна
        dpg.set_primary_window("main_window", True)
    
    def update_statistics(self, sender=None, app_data=None):
        """Обновление статистики"""
        try:
            stats = self.load_statistics()
            if stats:
                text = (
                    f"{self.get_text('total_cmds')} {stats['total_commands']}\n"
                    f"{self.get_text('last_active')} {stats['last_active']}\n\n"
                    f"{self.get_text('popular_cmds')}\n"
                )
                for cmd, count in sorted(stats['commands'].items(), key=lambda x: x[1], reverse=True):
                    text += f"{cmd}: {count}\n"
            else:
                text = self.get_text('no_stats')
            
            dpg.set_value("stats_text", text)
        except Exception as e:
            dpg.set_value("stats_text", f"Error: {str(e)}")
    
    def update_logs(self, sender=None, app_data=None):
        """Обновление логов"""
        try:
            if os.path.exists('bot.log'):
                with open('bot.log', 'r', encoding='utf-8') as f:
                    logs = f.read().strip()
                    dpg.set_value("log_viewer", logs if logs else "No logs available")
            else:
                dpg.set_value("log_viewer", "Log file does not exist")
        except Exception as e:
            dpg.set_value("log_viewer", f"Error loading logs: {str(e)}")
    
    def load_statistics(self):
        """Загрузка статистики"""
        try:
            if not os.path.exists('bot.log'):
                return None
                
            stats = {
                'total_commands': 0,
                'last_active': '',
                'commands': {}
            }
            
            with open('bot.log', 'r', encoding='utf-8') as f:
                for line in f:
                    if 'command:' in line.lower():
                        stats['total_commands'] += 1
                        stats['last_active'] = line.split('[')[0].strip()
                        
                        cmd = line.split('command:')[1].split()[0]
                        stats['commands'][cmd] = stats['commands'].get(cmd, 0) + 1
            
            return stats
        except Exception as e:
            print(f"Error loading statistics: {str(e)}")
            return None
    
    def restart_bot(self):
        """Перезапуск бота"""
        try:
            self.stop_bot()
            # Запускаем бота в фоновом режиме
            if sys.platform.startswith('win'):
                os.system('start /min cmd /c "python bot.py"')
            else:
                os.system('python bot.py &')
            dpg.set_value("bot_status", self.get_text('bot_running'))
        except Exception as e:
            self.show_error(str(e))
    
    def stop_bot(self):
        """Остановка бота"""
        try:
            if sys.platform.startswith('win'):
                os.system('taskkill /f /im python.exe /fi "windowtitle eq bot.py"')
            else:
                os.system('pkill -f "python bot.py"')
            dpg.set_value("bot_status", self.get_text('bot_stopped'))
        except Exception as e:
            self.show_error(str(e))
    
    def clear_logs(self):
        """Очистка логов"""
        try:
            if os.path.exists('bot.log'):
                with open('bot.log', 'w', encoding='utf-8') as f:
                    f.write(f"Logs cleared at {datetime.now()}\n")
                self.update_logs()
        except Exception as e:
            self.show_error(str(e))
    
    def clear_settings(self):
        """Очистка настроек"""
        dpg.set_value("token_input", "")
        dpg.set_value("user_id_input", "")
    
    def load_config(self):
        """Загрузка конфигурации"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
        return {}
    
    def save_and_exit(self):
        """Сохранение настроек"""
        try:
            # Проверка токена
            token = dpg.get_value("token_input").strip()
            if not token:
                self.show_error(self.get_text('token_required'))
                return
            
            # Проверка ID
            user_ids = dpg.get_value("user_id_input").strip()
            if not user_ids:
                self.show_error(self.get_text('id_required'))
                return
            
            try:
                user_id_list = [int(uid.strip()) for uid in user_ids.split(',') if uid.strip()]
                if not user_id_list:
                    raise ValueError()
            except ValueError:
                self.show_error(self.get_text('invalid_id'))
                return
            
            # Сохранение
            config = {
                'TELEGRAM_TOKEN': token,
                'AUTHORIZED_USERS': user_id_list
            }
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.show_success(self.get_text('save_success'))
            # Запускаем бота без закрытия интерфейса
            self.restart_bot()
        except Exception as e:
            self.show_error(str(e))
    
    def show_error(self, message):
        """Показ ошибки"""
        with dpg.window(
            label=self.get_text('error'),
            modal=True,
            no_close=True,
            width=300,
            height=100,
            pos=(350, 250)
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
            label=self.get_text('success'),
            modal=True,
            no_close=True,
            width=300,
            height=100,
            pos=(350, 250)
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

    def get_text(self, key):
        """Получение текста на текущем языке"""
        text = self.texts[self.current_lang].get(key, key)
        return fix_text(text)

if __name__ == '__main__':
    try:
        app = BotManager()
        app.run()
    except Exception as e:
        print(f"Application error: {str(e)}") 