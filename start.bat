@echo off
chcp 65001 > nul

echo =====================================
echo       PC Management Bot Launcher    
echo =====================================
echo.

REM Проверка Python
echo [*] Checking Python installation...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
) else (
    echo [OK] Python is installed
)

REM Проверка и создание виртуального окружения
echo [*] Checking virtual environment...
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo [OK] Virtual environment exists

REM Активация виртуального окружения
echo [*] Activating virtual environment...
call venv\Scripts\activate
echo [OK] Virtual environment activated

REM Установка зависимостей
echo [*] Checking dependencies...
echo [*] Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Создание необходимых директорий
echo [*] Creating directories...
if not exist "logs" mkdir logs
if not exist "downloads" mkdir downloads
if not exist "screenshots" mkdir screenshots
echo [OK] Directories created/checked

REM Бэкап лог файла если он существует
echo [*] Backing up log file...
if exist "bot.log" (
    copy "bot.log" "logs\bot_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log" > nul
    del "bot.log" > nul
)
echo [OK] Log file backed up

REM Проверка конфигурации и запуск GUI если нужно
if not exist "config.json" (
    echo [*] Configuration not found. Starting GUI...
    start /wait python bot_manager.py
) else (
    echo [*] Configuration found
    choice /C YN /M "Do you want to open settings"
    if errorlevel 2 (
        echo [*] Skipping settings
    ) else (
        start /wait python bot_manager.py
    )
)

echo.
echo =====================================
echo Starting the bot...
echo Press Ctrl+C to stop
echo =====================================
echo.

REM Запуск бота
python bot.py

REM Если бот завершился с ошибкой
if errorlevel 1 (
    echo.
    echo [ERROR] Bot stopped with error
    echo Check bot.log for details
    pause
) 