
    Unicode true
    
    !include "MUI2.nsh"
    !include "FileFunc.nsh"
    
    Name "PC Manager Bot v1.0.0"
    OutFile "J:\Telegram bot for PC management\dist\PCManagerBot_Setup_v1.0.0.exe"
    InstallDir "$PROGRAMFILES64\PCManagerBot"
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
        File "J:\Telegram bot for PC management\build\bot_manager.py"
        File "J:\Telegram bot for PC management\build\handlers.py"
        File "J:\Telegram bot for PC management\build\utils.py"
        File "J:\Telegram bot for PC management\build\logger.py"
        File "J:\Telegram bot for PC management\build\translations.py"
        File "J:\Telegram bot for PC management\build\config.json"
        File "J:\Telegram bot for PC management\build\requirements.txt"
        
        # Копируем директорию с runtime
        SetOutPath "$INSTDIR\pyarmor_runtime_000000"
        File /r "J:\Telegram bot for PC management\build\pyarmor_runtime_000000\*.*"
        
        SetOutPath "$INSTDIR"
        
        # Создаем bat-файл для запуска
        FileOpen $0 "$INSTDIR\start_bot.bat" w
        FileWrite $0 "@echo off$\r$\n"
        FileWrite $0 "cd %~dp0$\r$\n"
        FileWrite $0 "python bot_manager.py$\r$\n"
        FileWrite $0 "pause$\r$\n"
        FileClose $0
        
        # Создаем ярлыки
        CreateDirectory "$SMPROGRAMS\PCManagerBot"
        CreateShortcut "$SMPROGRAMS\PCManagerBot\PC Manager Bot.lnk" "$INSTDIR\start_bot.bat"
        CreateShortcut "$DESKTOP\PC Manager Bot.lnk" "$INSTDIR\start_bot.bat"
        
        # Создаем деинсталлятор
        WriteUninstaller "$INSTDIR\uninstall.exe"
        
        # Добавляем в список программ
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PCManagerBot" "DisplayName" "PC Manager Bot"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PCManagerBot" "UninstallString" "$INSTDIR\uninstall.exe"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PCManagerBot" "DisplayVersion" "$1.0.0"
    SectionEnd
    
    Section "Uninstall"
        # Удаляем файлы
        Delete "$INSTDIR\bot_manager.py"
        Delete "$INSTDIR\handlers.py"
        Delete "$INSTDIR\utils.py"
        Delete "$INSTDIR\logger.py"
        Delete "$INSTDIR\translations.py"
        Delete "$INSTDIR\config.json"
        Delete "$INSTDIR\requirements.txt"
        Delete "$INSTDIR\start_bot.bat"
        RMDir /r "$INSTDIR\pyarmor_runtime_000000"
        Delete "$INSTDIR\uninstall.exe"
        RMDir "$INSTDIR"
        
        # Удаляем ярлыки
        Delete "$SMPROGRAMS\PCManagerBot\PC Manager Bot.lnk"
        RMDir "$SMPROGRAMS\PCManagerBot"
        Delete "$DESKTOP\PC Manager Bot.lnk"
        
        # Удаляем из списка программ
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PCManagerBot"
    SectionEnd
    