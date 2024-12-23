import os
import shutil
import subprocess
from create_icon import create_icon

def build_installer():
    print("Создание установщика PC Manager Bot...")
    
    # Создаем иконку
    print("Создание иконки...")
    create_icon()
    
    # Создаем пример конфига
    print("Создание примера конфига...")
    config_example = {
        "TELEGRAM_TOKEN": "YOUR_BOT_TOKEN_HERE",
        "AUTHORIZED_USERS": [123456789]
    }
    import json
    with open('config.json.example', 'w') as f:
        json.dump(config_example, f, indent=4)
    
    # Проверяем наличие NSIS
    nsis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
    if not os.path.exists(nsis_path):
        print("ОШИБКА: NSIS не найден!")
        print("Скачайте NSIS с https://nsis.sourceforge.io/Download")
        return False
    
    # Собираем установщик
    print("Сборка установщика...")
    try:
        subprocess.run([nsis_path, "installer.nsi"], check=True)
        print("Установщик успешно создан: PC_Manager_Bot_Setup.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ОШИБКА при сборке установщика: {e}")
        return False

if __name__ == '__main__':
    build_installer() 