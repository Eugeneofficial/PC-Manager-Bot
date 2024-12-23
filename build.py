import os
import sys
import shutil
import uuid
from datetime import datetime, timedelta

# Конфигурация сборки
VERSION = "1.0.0"
EXPIRATION_DAYS = 30  # Срок действия в днях
OUTPUT_DIR = "dist"
TEMP_DIR = "build"
ICON_PATH = "icon.ico"

def clean_dirs():
    """Очистка директорий сборки"""
    for dir in [OUTPUT_DIR, TEMP_DIR]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

def get_machine_code():
    """Получение уникального кода машины"""
    try:
        import wmi
        c = wmi.WMI()
        # Получаем серийный номер процессора и материнской платы
        cpu = c.Win32_Processor()[0].ProcessorId.strip()
        board = c.Win32_BaseBoard()[0].SerialNumber.strip()
        return f"{cpu}-{board}"
    except:
        # Если не удалось получить железо, используем UUID
        return str(uuid.uuid4())

def build_protected():
    """Сборка защищенного приложения"""
    # Создаем временную лицензию
    machine_code = get_machine_code()
    expiration_date = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    
    # Создаем файл конфигурации PyArmor
    config_content = f"""
[build]
output = {TEMP_DIR}
platform = windows.x86_64
plugins = check_restrict,check_expiration
cross_protection = 1
restrict_mode = 1
expire_date = {expiration_date.strftime("%Y-%m-%d")}
bind_data = {machine_code}
    """
    
    # Сохраняем конфигурацию
    with open("pyarmor.toml", "w") as f:
        f.write(config_content)
    
    # Создаем команды PyArmor
    print("Generating protected files...")
    result = os.system(f'pyarmor gen bot_manager.py')
    if result != 0:
        print("Error generating protected files")
        sys.exit(1)
    
    # Перемещаем защищенные файлы
    print("Moving protected files...")
    if os.path.exists("dist"):
        # Перемещаем все файлы из dist в build
        for item in os.listdir("dist"):
            src = os.path.join("dist", item)
            dst = os.path.join(TEMP_DIR, item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        # Удаляем временную директорию dist
        shutil.rmtree("dist")
    
    # Копируем дополнительные файлы
    print("Copying additional files...")
    additional_files = [
        "handlers.py",
        "utils.py",
        "logger.py",
        "translations.py",
        "config.json",
        "requirements.txt",
        "README.md"
    ]
    
    for file in additional_files:
        if os.path.exists(file):
            try:
                shutil.copy2(file, TEMP_DIR)
                print(f"Copied {file}")
            except Exception as e:
                print(f"Error copying {file}: {e}")

def create_installer():
    """Создание установщика"""
    # Создаем директорию dist если её нет
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Проверяем наличие всех необходимых файлов
    required_files = [
        "bot_manager.py",
        "handlers.py",
        "utils.py",
        "logger.py",
        "translations.py",
        "config.json",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(TEMP_DIR, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
            print(f"Warning: {file} not found in {TEMP_DIR}")
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        sys.exit(1)
    
    # Проверяем наличие runtime директории
    runtime_dir = os.path.join(TEMP_DIR, "pyarmor_runtime_000000")
    if not os.path.exists(runtime_dir):
        print(f"Error: Runtime directory not found at {runtime_dir}")
        sys.exit(1)
    
    # Создаем установщик с помощью NSIS
    nsis_script = f"""
    Unicode true
    
    !include "MUI2.nsh"
    !include "FileFunc.nsh"
    
    Name "PC Manager Bot v{VERSION}"
    OutFile "{os.path.abspath(os.path.join(OUTPUT_DIR, 'PCManagerBot_Setup_v' + VERSION + '.exe'))}"
    InstallDir "$PROGRAMFILES64\\PCManagerBot"
    RequestExecutionLevel admin
    
    !define MUI_ABORTWARNING
    
    !insertmacro MUI_PAGE_WELCOME
    !insertmacro MUI_PAGE_DIRECTORY
    !insertmacro MUI_PAGE_INSTFILES
    !insertmacro MUI_PAGE_FINISH
    
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_INSTFILES
    
    !insertmacro MUI_LANGUAGE "Russian"
    !insertmacro MUI_LANGUAGE "English"
    
    Section "MainSection" SEC01
        SetOutPath "$INSTDIR"
        
        # Копируем файлы по одному
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'bot_manager.py'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'handlers.py'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'utils.py'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'logger.py'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'translations.py'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'config.json'))}"
        File "{os.path.abspath(os.path.join(TEMP_DIR, 'requirements.txt'))}"
        
        # Копируем директорию с runtime
        SetOutPath "$INSTDIR\\pyarmor_runtime_000000"
        File /r "{os.path.abspath(runtime_dir)}\\*.*"
        
        SetOutPath "$INSTDIR"
        
        # Создаем bat-файл для запуска
        FileOpen $0 "$INSTDIR\\start_bot.bat" w
        FileWrite $0 "@echo off$\\r$\\n"
        FileWrite $0 "cd %~dp0$\\r$\\n"
        FileWrite $0 "python bot_manager.py$\\r$\\n"
        FileWrite $0 "pause$\\r$\\n"
        FileClose $0
        
        # Создаем ярлыки
        CreateDirectory "$SMPROGRAMS\\PCManagerBot"
        CreateShortcut "$SMPROGRAMS\\PCManagerBot\\PC Manager Bot.lnk" "$INSTDIR\\start_bot.bat"
        CreateShortcut "$DESKTOP\\PC Manager Bot.lnk" "$INSTDIR\\start_bot.bat"
        
        # Создаем деинсталлятор
        WriteUninstaller "$INSTDIR\\uninstall.exe"
        
        # Добавляем в список программ
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PCManagerBot" "DisplayName" "PC Manager Bot"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PCManagerBot" "UninstallString" "$INSTDIR\\uninstall.exe"
        WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PCManagerBot" "DisplayVersion" "${VERSION}"
    SectionEnd
    
    Section "Uninstall"
        # Удаляем файлы
        Delete "$INSTDIR\\bot_manager.py"
        Delete "$INSTDIR\\handlers.py"
        Delete "$INSTDIR\\utils.py"
        Delete "$INSTDIR\\logger.py"
        Delete "$INSTDIR\\translations.py"
        Delete "$INSTDIR\\config.json"
        Delete "$INSTDIR\\requirements.txt"
        Delete "$INSTDIR\\start_bot.bat"
        RMDir /r "$INSTDIR\\pyarmor_runtime_000000"
        Delete "$INSTDIR\\uninstall.exe"
        RMDir "$INSTDIR"
        
        # Удаляем ярлыки
        Delete "$SMPROGRAMS\\PCManagerBot\\PC Manager Bot.lnk"
        RMDir "$SMPROGRAMS\\PCManagerBot"
        Delete "$DESKTOP\\PC Manager Bot.lnk"
        
        # Удаляем из списка программ
        DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PCManagerBot"
    SectionEnd
    """
    
    # Сохраняем скрипт NSIS
    nsis_script_path = os.path.join(TEMP_DIR, "installer.nsi")
    with open(nsis_script_path, "w", encoding='utf-8') as f:
        f.write(nsis_script)
    
    # Проверяем, что скрипт создался
    if not os.path.exists(nsis_script_path):
        print(f"Error: Failed to create NSIS script at {nsis_script_path}")
        sys.exit(1)
    else:
        print(f"NSIS script created at {nsis_script_path}")
    
    # Компилируем установщик
    print("Creating installer...")
    result = os.system(f'makensis "{nsis_script_path}"')
    if result != 0:
        print("Error creating installer")
        sys.exit(1)
    print("Installer created successfully")

def main():
    print("Starting build process...")
    
    # Проверяем наличие PyArmor
    if os.system("pyarmor --version") != 0:
        print("Installing PyArmor...")
        os.system("pip install pyarmor")
    
    # Проверяем наличие NSIS
    if os.system("makensis /VERSION") != 0:
        print("Error: NSIS not found! Please install NSIS from https://nsis.sourceforge.io/")
        sys.exit(1)
    
    # Очищаем директории
    clean_dirs()
    
    # Собираем защищенное приложение
    print("Building protected application...")
    build_protected()
    
    # Создаем установщик
    print("Creating installer...")
    create_installer()
    
    print(f"Build completed! Installer is in {OUTPUT_DIR} directory")

if __name__ == "__main__":
    main() 