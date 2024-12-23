import dearpygui.dearpygui as dpg
import json
import os
import subprocess
import sys
import requests
from utils import load_config, save_config

VERSION = "1.0.0"
GITHUB_REPO = "your_github_repo"  # Change this to your repo

class BotGUI:
    def __init__(self):
        self.current_lang = "English"
        self.languages = {
            "English": {
                "title": "PC Management Bot Configuration",
                "tabs": {
                    "main": "Main Settings",
                    "users": "User Management",
                    "premium": "Premium Features",
                    "updates": "Updates"
                },
                "profiles_label": "Saved Profiles:",
                "profile_name_label": "Profile Name:",
                "save_profile_button": "Save Profile",
                "delete_profile_button": "Delete Profile",
                "token_label": "Bot Token:",
                "user_id_label": "User ID:",
                "save_button": "Save and Start Bot",
                "check_updates": "Check for Updates",
                "current_version": "Current Version:",
                "premium_features": {
                    "remote_desktop": "Remote Desktop Access",
                    "file_transfer": "File Transfer",
                    "process_manager": "Advanced Process Manager",
                    "system_info": "Detailed System Information",
                    "activate": "Activate Premium"
                },
                "user_management": {
                    "add": "Add User",
                    "remove": "Remove User",
                    "list": "User List",
                    "premium_status": "Premium Status"
                },
                "get_token_help": """How to get Bot Token:
1. Open Telegram and search for @BotFather
2. Send /newbot command
3. Follow instructions to create a new bot
4. Copy the provided token""",
                "get_userid_help": """How to get User ID:
1. Open Telegram and search for @userinfobot
2. Start chat with the bot
3. Send any message
4. Copy the user ID number provided
Note: Only users with authorized IDs can use the bot!"""
            },
            "Russian": {
                "title": "Настройка бота управления ПК",
                "tabs": {
                    "main": "Основные настройки",
                    "users": "Управление пользователями",
                    "premium": "Премиум функции",
                    "updates": "Обновления"
                },
                "profiles_label": "Сохраненные профили:",
                "profile_name_label": "Имя профиля:",
                "save_profile_button": "Сохранить профиль",
                "delete_profile_button": "Удалить профиль",
                "token_label": "Токен бота:",
                "user_id_label": "ID пользователя:",
                "save_button": "Сохранить и запустить",
                "check_updates": "Проверить обновления",
                "current_version": "Текущая версия:",
                "premium_features": {
                    "remote_desktop": "Удаленный рабочий стол",
                    "file_transfer": "Передача файлов",
                    "process_manager": "Расширенный диспетчер процессов",
                    "system_info": "Подробная информация о системе",
                    "activate": "Активировать премиум"
                },
                "user_management": {
                    "add": "Добавить пользователя",
                    "remove": "Удалить пользователя",
                    "list": "Список пользователей",
                    "premium_status": "Премиум статус"
                },
                "get_token_help": """Как получить токен бота:
1. Откройте Telegram и найдите @BotFather
2. Отправьте команду /newbot
3. Следуйте инструкциям для создания бота
4. Скопируйте предоставленный токен""",
                "get_userid_help": """Как получить ID пользователя:
1. Откройте Telegram и найдите @userinfobot
2. Начните чат с ботом
3. Отправьте любое сообщение
4. Скопируйте предоставленный ID
Примечание: Только пользователи с авторизованными ID могут использовать бота!"""
            },
            "Chinese": {
                "title": "PC管理机器人配置",
                "tabs": {
                    "main": "主要设置",
                    "users": "用户管理",
                    "premium": "高级功能",
                    "updates": "更新"
                },
                "profiles_label": "已保存的配置:",
                "profile_name_label": "配置名称:",
                "save_profile_button": "保存配置",
                "delete_profile_button": "删除配置",
                "token_label": "机器人令牌:",
                "user_id_label": "用户ID:",
                "save_button": "保存并启动",
                "check_updates": "检查更新",
                "current_version": "当前版本:",
                "premium_features": {
                    "remote_desktop": "远程桌面访问",
                    "file_transfer": "文件传输",
                    "process_manager": "高级进程管理器",
                    "system_info": "详细系统信息",
                    "activate": "激活高级功能"
                },
                "user_management": {
                    "add": "添加用户",
                    "remove": "删除用户",
                    "list": "用户列表",
                    "premium_status": "高级状态"
                },
                "get_token_help": """如何获取机器人令牌：
1. 打开Telegram并搜索 @BotFather
2. 发送 /newbot 命令
3. 按照说明创建新机器人
4. 复制提供的令牌""",
                "get_userid_help": """如何获取用户ID：
1. 打开Telegram并搜索 @userinfobot
2. 与机器人开始对话
3. 发送任何消息
4. 复制提供的用户ID
注意：只有经过授权的用户ID才能使用机器人！"""
            }
        }
        self.profiles = load_config() or {}
        self.current_profile = None
        self.premium_features = {
            "remote_desktop": False,
            "file_transfer": False,
            "process_manager": False,
            "system_info": False
        }

    def check_for_updates(self):
        try:
            response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
            latest_version = response.json()["tag_name"]
            if latest_version > VERSION:
                dpg.configure_item("update_text", default_value=f"New version {latest_version} available!")
                return True
            dpg.configure_item("update_text", default_value="You have the latest version")
            return False
        except:
            dpg.configure_item("update_text", default_value="Failed to check for updates")
            return False

    def save_profile_callback(self):
        profile_name = dpg.get_value("profile_name_input").strip()
        token = dpg.get_value("token_input").strip()
        user_id = dpg.get_value("userid_input").strip()

        if not all([profile_name, token, user_id]):
            dpg.configure_item("error_text", show=True)
            return

        try:
            user_id = int(user_id)
        except ValueError:
            dpg.configure_item("error_text", show=True)
            return

        self.profiles[profile_name] = {
            "token": token,
            "user_ids": str(user_id),
            "premium": True,
            "premium_features": self.premium_features
        }
        save_config(self.profiles)
        
        dpg.configure_item("profiles_combo", items=list(self.profiles.keys()))
        dpg.set_value("profiles_combo", profile_name)
        dpg.configure_item("success_text", show=True, default_value="Profile saved successfully!")

    def delete_profile_callback(self):
        profile_name = dpg.get_value("profiles_combo")
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            save_config(self.profiles)
            dpg.configure_item("profiles_combo", items=list(self.profiles.keys()))
            dpg.configure_item("success_text", show=True, default_value="Profile deleted successfully!")
            dpg.set_value("token_input", "")
            dpg.set_value("userid_input", "")
            dpg.set_value("profile_name_input", "")

    def load_profile_callback(self, sender, app_data):
        if app_data in self.profiles:
            profile = self.profiles[app_data]
            dpg.set_value("token_input", profile.get("token", ""))
            dpg.set_value("userid_input", profile.get("user_ids", ""))
            dpg.set_value("profile_name_input", app_data)
            self.current_profile = app_data
            
            # Load premium features
            self.premium_features = profile.get("premium_features", {
                "remote_desktop": False,
                "file_transfer": False,
                "process_manager": False,
                "system_info": False
            })
            
            # Update premium checkboxes
            for feature in self.premium_features:
                dpg.set_value(f"premium_{feature}", self.premium_features[feature])

    def toggle_premium_feature(self, sender, app_data, user_data):
        feature_name = user_data
        self.premium_features[feature_name] = app_data
        if self.current_profile:
            self.profiles[self.current_profile]["premium_features"] = self.premium_features
            save_config(self.profiles)

    def save_callback(self):
        token = dpg.get_value("token_input").strip()
        user_id = dpg.get_value("userid_input").strip()
        
        if not token or not user_id:
            dpg.configure_item("error_text", show=True)
            return
        
        try:
            user_id = int(user_id)
        except ValueError:
            dpg.configure_item("error_text", show=True)
            return
        
        # Save configuration
        profile_name = dpg.get_value("profile_name_input").strip() or "default"
        self.profiles[profile_name] = {
            "token": token,
            "user_ids": str(user_id),
            "premium": True,
            "premium_features": self.premium_features
        }
        save_config(self.profiles)
        
        dpg.configure_item("success_text", show=True, default_value="Configuration saved successfully!")
        
        # Start the bot in a new process
        python = sys.executable
        subprocess.Popen([python, "bot.py"])
        
        # Close the GUI
        dpg.stop_dearpygui()

    def language_callback(self, sender, app_data):
        self.current_lang = app_data
        lang_data = self.languages[self.current_lang]
        
        # Update all text elements
        dpg.set_value("title_text", lang_data["title"])
        dpg.configure_item("tab_main", label=lang_data["tabs"]["main"])
        dpg.configure_item("tab_users", label=lang_data["tabs"]["users"])
        dpg.configure_item("tab_premium", label=lang_data["tabs"]["premium"])
        dpg.configure_item("tab_updates", label=lang_data["tabs"]["updates"])
        
        dpg.set_value("profiles_text", lang_data["profiles_label"])
        dpg.set_value("profile_name_text", lang_data["profile_name_label"])
        dpg.configure_item("save_profile_button", label=lang_data["save_profile_button"])
        dpg.configure_item("delete_profile_button", label=lang_data["delete_profile_button"])
        dpg.set_value("token_text", lang_data["token_label"])
        dpg.set_value("userid_text", lang_data["user_id_label"])
        dpg.set_value("token_help", lang_data["get_token_help"])
        dpg.set_value("userid_help", lang_data["get_userid_help"])
        dpg.configure_item("save_button", label=lang_data["save_button"])

    def create_gui(self):
        dpg.create_context()
        dpg.create_viewport(title="PC Management Bot", width=800, height=800)
        dpg.setup_dearpygui()

        # Fonts
        with dpg.font_registry():
            with dpg.font("c:\\windows\\fonts\\msyh.ttc", 20) as default_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font(default_font)

        # Premium activation popup
        with dpg.window(label="Premium Activation", show=False, tag="premium_window", modal=True, width=400, height=200):
            dpg.add_text("Enter activation key:")
            dpg.add_input_text(tag="activation_key", width=-1)
            dpg.add_button(label="Activate", callback=self.activate_premium)
            dpg.add_button(label="Close", callback=lambda: dpg.configure_item("premium_window", show=False))

        # Main window with tabs
        with dpg.window(label="Configuration", tag="main_window"):
            dpg.add_text(self.languages[self.current_lang]["title"], tag="title_text")
            
            # Language selector
            dpg.add_combo(
                items=list(self.languages.keys()),
                default_value=self.current_lang,
                callback=self.language_callback,
                width=200
            )
            
            with dpg.tab_bar():
                # Main Settings Tab
                with dpg.tab(label=self.languages[self.current_lang]["tabs"]["main"], tag="tab_main"):
                    # Profiles section
                    dpg.add_text(self.languages[self.current_lang]["profiles_label"], tag="profiles_text")
                    dpg.add_combo(
                        items=list(self.profiles.keys()),
                        callback=self.load_profile_callback,
                        tag="profiles_combo",
                        width=300
                    )
                    
                    dpg.add_text(self.languages[self.current_lang]["profile_name_label"], tag="profile_name_text")
                    dpg.add_input_text(tag="profile_name_input", width=300)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label=self.languages[self.current_lang]["save_profile_button"],
                            callback=self.save_profile_callback,
                            tag="save_profile_button",
                            width=150
                        )
                        dpg.add_button(
                            label=self.languages[self.current_lang]["delete_profile_button"],
                            callback=self.delete_profile_callback,
                            tag="delete_profile_button",
                            width=150
                        )
                    
                    dpg.add_separator()
                    
                    # Bot Token
                    dpg.add_text(self.languages[self.current_lang]["token_label"], tag="token_text")
                    dpg.add_input_text(tag="token_input", width=-1)
                    dpg.add_text(self.languages[self.current_lang]["get_token_help"], 
                                tag="token_help", wrap=800)
                    
                    dpg.add_spacer(height=10)
                    
                    # User ID
                    dpg.add_text(self.languages[self.current_lang]["user_id_label"], tag="userid_text")
                    dpg.add_input_text(tag="userid_input", width=-1)
                    dpg.add_text(self.languages[self.current_lang]["get_userid_help"], 
                                tag="userid_help", wrap=800)
                
                # User Management Tab
                with dpg.tab(label=self.languages[self.current_lang]["tabs"]["users"], tag="tab_users"):
                    dpg.add_text("User Management coming soon...")
                
                # Premium Features Tab
                with dpg.tab(label=self.languages[self.current_lang]["tabs"]["premium"], tag="tab_premium"):
                    for feature, text in self.languages[self.current_lang]["premium_features"].items():
                        if feature != "activate":
                            dpg.add_checkbox(
                                label=text,
                                tag=f"premium_{feature}",
                                callback=self.toggle_premium_feature,
                                user_data=feature,
                                default_value=self.premium_features.get(feature, False)
                            )
                    
                    dpg.add_button(
                        label=self.languages[self.current_lang]["premium_features"]["activate"],
                        tag="activate_premium_button",
                        callback=lambda: dpg.configure_item("premium_window", show=True)
                    )
                
                # Updates Tab
                with dpg.tab(label=self.languages[self.current_lang]["tabs"]["updates"], tag="tab_updates"):
                    dpg.add_text(f"{self.languages[self.current_lang]['current_version']} {VERSION}")
                    dpg.add_button(
                        label=self.languages[self.current_lang]["check_updates"],
                        callback=self.check_for_updates
                    )
                    dpg.add_text("", tag="update_text")
            
            # Error and success messages
            dpg.add_text("Please fill in all fields correctly", tag="error_text", 
                        color=(255, 0, 0), show=False)
            dpg.add_text("", tag="success_text", 
                        color=(0, 255, 0), show=False)
            
            # Save button
            dpg.add_button(
                label=self.languages[self.current_lang]["save_button"],
                callback=self.save_callback,
                tag="save_button",
                width=-1
            )

        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def activate_premium(self, sender, app_data):
        key = dpg.get_value("activation_key")
        if key == "PREMIUM-2024":  # Simple example key
            if self.current_profile:
                self.profiles[self.current_profile]["premium"] = True
                for feature in self.premium_features:
                    self.premium_features[feature] = True
                    dpg.set_value(f"premium_{feature}", True)
                save_config(self.profiles)
                dpg.configure_item("success_text", show=True, default_value="Premium features activated!")
            dpg.configure_item("premium_window", show=False)
        else:
            dpg.configure_item("error_text", show=True, default_value="Invalid activation key!")

def main():
    gui = BotGUI()
    gui.create_gui()

if __name__ == "__main__":
    main()
