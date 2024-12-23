; Определяем имя программы и версию
!define APPNAME "PC Manager Bot"
!define APPVERSION "1.0"
!define DEFAULTDIR "$PROGRAMFILES\${APPNAME}"

; Включаем современный интерфейс
!include "MUI2.nsh"

; Настройки установщика
Name "${APPNAME}"
OutFile "PC_Manager_Bot_Setup.exe"
InstallDir "${DEFAULTDIR}"
RequestExecutionLevel admin

; Страницы установщика
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Языки
!insertmacro MUI_LANGUAGE "Russian"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    
    ; Копируем файлы
    File "bot.py"
    File "setup.py"
    File "requirements.txt"
    File "config.json.example"
    
    ; Создаем ярлыки
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "pythonw.exe" "setup.py" "$INSTDIR\icon.ico"
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "pythonw.exe" "setup.py" "$INSTDIR\icon.ico"
    
    ; Устанавливаем Python и зависимости
    nsExec::ExecToLog 'python -m pip install -r "$INSTDIR\requirements.txt"'
    
    ; Записываем информацию о деинсталляции
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${APPVERSION}"
SectionEnd

Section "Uninstall"
    ; Удаляем файлы
    Delete "$INSTDIR\bot.py"
    Delete "$INSTDIR\setup.py"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\config.json"
    Delete "$INSTDIR\config.json.example"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Удаляем ярлыки
    Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${APPNAME}"
    
    ; Удаляем папку установки
    RMDir "$INSTDIR"
    
    ; Удаляем информацию из реестра
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd 