@echo off
title PC Manager Bot
cd /d "%~dp0"
"C:\Users\mrjek\AppData\Local\Programs\Python\Python311\python.exe" -u "J:\Telegram bot for PC management\bot.py"
if errorlevel 1 (
    echo.
    echo Press Enter to exit...
    pause >nul
)
