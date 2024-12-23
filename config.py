import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Configuration file path
CONFIG_FILE = "bot_profiles.json"

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Management Bot Configuration")
        self.root.geometry("600x800")
        
        # Load languages
        self.languages = {
            "English": {
                "title": "Bot Configuration",
                "token_label": "Bot Token:",
                "user_id_label": "User ID:",
                "save_button": "Save Configuration",
                "get_token_help": """How to get Bot Token:
1. Open Telegram and search for @BotFather
2. Send /newbot command
3. Follow instructions to create a new bot
4. Copy the provided token""",
                "get_userid_help": """How to get User ID:
1. Open Telegram and search for @userinfobot
2. Start chat with the bot
3. Send any message
4. Copy the user ID number provided""",
            },
            "Russian": {
                "title": "Настройка бота",
                "token_label": "Токен бота:",
                "user_id_label": "ID пользователя:",
                "save_button": "Сохранить настройки",
                "get_token_help": """Как получить токен бота:
1. Откройте Telegram и найдите @BotFather
2. Отправьте команду /newbot
3. Следуйте инструкциям для создания бота
4. Скопируйте предоставленный токен""",
                "get_userid_help": """Как получить ID пользователя:
1. Откройте Telegram и найдите @userinfobot
2. Начните чат с ботом
3. Отправьте любое сообщение
4. Скопируйте предоставленный ID""",
            },
            "Chinese": {
                "title": "机器人配置",
                "token_label": "机器人令牌：",
                "user_id_label": "用户ID：",
                "save_button": "保存配置",
                "get_token_help": """如何获取机器人令牌：
1. 打开Telegram并搜索 @BotFather
2. 发送 /newbot 命令
3. 按照说明创建新机器人
4. 复制提供的令牌""",
                "get_userid_help": """如何获取用户ID：
1. 打开Telegram并搜索 @userinfobot
2. 与机器人开始对话
3. 发送任何消息
4. 复制提供的用户ID""",
            }
        }
        
        self.current_lang = "English"
        self.create_widgets()
        
    def create_widgets(self):
        # Language selector
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(lang_frame, text="Language:").pack(side="left")
        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 values=list(self.languages.keys()), state="readonly")
        lang_combo.pack(side="left", padx=5)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Bot Token
        ttk.Label(self.main_frame, text=self.languages[self.current_lang]["token_label"], 
                 font=('Arial', 10, 'bold')).pack(anchor="w")
        self.token_entry = ttk.Entry(self.main_frame, width=50)
        self.token_entry.pack(fill="x", pady=(0, 10))
        
        # Token Help Text
        token_help = tk.Text(self.main_frame, height=6, wrap="word")
        token_help.pack(fill="x", pady=(0, 20))
        token_help.insert("1.0", self.languages[self.current_lang]["get_token_help"])
        token_help.config(state="disabled")
        
        # User ID
        ttk.Label(self.main_frame, text=self.languages[self.current_lang]["user_id_label"], 
                 font=('Arial', 10, 'bold')).pack(anchor="w")
        self.userid_entry = ttk.Entry(self.main_frame, width=50)
        self.userid_entry.pack(fill="x", pady=(0, 10))
        
        # User ID Help Text
        userid_help = tk.Text(self.main_frame, height=6, wrap="word")
        userid_help.pack(fill="x", pady=(0, 20))
        userid_help.insert("1.0", self.languages[self.current_lang]["get_userid_help"])
        userid_help.config(state="disabled")
        
        # Save Button
        ttk.Button(self.main_frame, text=self.languages[self.current_lang]["save_button"],
                  command=self.save_config).pack(pady=20)
        
        # Load existing config
        self.load_config()
    
    def change_language(self, event=None):
        self.current_lang = self.lang_var.get()
        self.root.title(self.languages[self.current_lang]["title"])
        self.create_widgets()
    
    def save_config(self):
        token = self.token_entry.get().strip()
        user_id = self.userid_entry.get().strip()
        
        if not token or not user_id:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "User ID must be a number")
            return
        
        config = {
            "TOKEN": token,
            "ALLOWED_USERS": [user_id]
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        messagebox.showinfo("Success", "Configuration saved successfully!")
    
    def load_config(self):
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.token_entry.insert(0, config.get('TOKEN', ''))
                    if config.get('ALLOWED_USERS'):
                        self.userid_entry.insert(0, str(config['ALLOWED_USERS'][0]))
            except:
                pass

def load_config():
    """Load bot configuration from file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Get first profile's user IDs
                first_profile = next(iter(config.values()))
                PREMIUM_USERS = [int(uid) for uid in first_profile.get('user_ids', '').split(',') if uid]
                return PREMIUM_USERS
        return []
    except Exception as e:
        print(f"Error loading config: {e}")
        return []

# Load premium users on module import
PREMIUM_USERS = load_config()

def main():
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
