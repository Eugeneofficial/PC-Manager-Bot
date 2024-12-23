# PC Manager Bot | Бот для управления ПК

[English](#english) | [Русский](#russian)

# English

Telegram bot for remote Windows PC management with extensive system administration capabilities.

## 🆕 Latest Updates (v2.0)

### New Features
- Added 40+ new functions for system administrators
- Improved error handling and encoding support
- Added new keyboard layout with categorized buttons
- Enhanced plugin system for extensibility
- Improved camera and audio capture

### System Administration Features
1. **System Information**
   - 💻 System stats and hardware info
   - 📊 Process monitoring and management
   - 🌡️ CPU load and temperature monitoring
   - 💾 Disk space and SMART status
   - 📁 File system management

2. **Hardware Control**
   - 📸 Screenshot capture
   - 🎥 Camera access and photo capture
   - 🎤 Microphone recording (10 sec)
   - 🖥️ Monitor information
   - 🔊 Audio device control

3. **Network Tools**
   - 🌐 IP configuration and network status
   - 🔌 Open ports scanning
   - 📡 DNS cache management
   - 📶 Wi-Fi connection info
   - 🛡️ Firewall settings

4. **Security Features**
   - ⚡ Admin rights management
   - 🔒 UAC settings control
   - 🔑 Access rights management
   - 🗄️ Registry operations
   - 📦 Package management

5. **Monitoring Tools**
   - 💽 Storage health monitoring
   - 🔄 System information
   - 🌡️ Temperature sensors
   - 📝 System logs access
   - 🔍 Error tracking

6. **User Management**
   - 🔒 Local groups control
   - 👥 User accounts management
   - 🗃️ Network shares
   - 🔐 System lock control
   - 🛡️ Security policies

## Installation

### Method 1: Using Installer
1. Download latest release from [Releases](https://github.com/Eugeneofficial/PC-Manager-Bot/releases)
2. Run PC-Manager-Bot-Setup.exe
3. Follow installation wizard
4. Configure bot token and user ID
5. Start using!

### Method 2: Manual Installation
1. Clone repository:
```bash
git clone https://github.com/Eugeneofficial/PC-Manager-Bot.git
cd PC-Manager-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure:
- Create config.json with your Telegram bot token and user ID
- Enable desired plugins

4. Run:
```bash
python bot.py
```

## Requirements
- Windows 10/11
- Python 3.8+
- Internet access
- Admin rights (for some features)

## Development
- Written in Python
- Uses python-telegram-bot
- Plugin-based architecture
- MIT License

# Russian

Telegram бот для удаленного управления компьютером с Windows с расширенными возможностями системного администрирования.

## 🆕 Последние обновления (v2.0)

### Новые возможности
- Добавлено более 40 новых функций для системных администраторов
- Улучшена обработка ошибок и поддержка кодировок
- Добавлена новая раскладка клавиатуры с категориями
- Улучшена система плагинов для расширяемости
- Улучшена работа с камерой и звуком

### Функции системного администрирования
1. **Системная информация**
   - 💻 Статистика системы и оборудования
   - 📊 Мониторинг и управление процессами
   - 🌡️ Мониторинг загрузки и температуры CPU
   - 💾 Информация о дисках и SMART-статус
   - 📁 Управление файловой системой

2. **Управление оборудованием**
   - 📸 Создание скриншотов
   - 🎥 Доступ к камере и фото
   - 🎤 Запись с микрофона (10 сек)
   - 🖥️ Информация о мониторах
   - 🔊 Управление аудио

3. **Сетевые инструменты**
   - 🌐 Конфигурация IP и статус сети
   - 🔌 Сканирование открытых портов
   - 📡 Управление DNS-кэшем
   - 📶 Информация о Wi-Fi
   - 🛡️ Настройки брандмауэра

4. **Функции безопасности**
   - ⚡ Управление правами администратора
   - 🔒 Управление настройками UAC
   - 🔑 Управление правами доступа
   - 🗄️ Операции с реестром
   - 📦 Управление пакетами

5. **Инструменты мониторинга**
   - 💽 Мониторинг здоровья дисков
   - 🔄 Системная информация
   - 🌡️ Датчики температуры
   - 📝 Доступ к системным логам
   - 🔍 Отслеживание ошибок

6. **Управление пользователями**
   - 🔒 Управление локальными группами
   - 👥 Управление учетными записями
   - 🗃️ Сетевые ресурсы
   - 🔐 Управление блокировкой
   - 🛡️ Политики безопасности

## Установка

### Способ 1: Через установщик
1. Скачайте последний релиз из [Releases](https://github.com/Eugeneofficial/PC-Manager-Bot/releases)
2. Запустите PC-Manager-Bot-Setup.exe
3. Следуйте инструкциям установщика
4. Настройте токен бота и ID пользователя
5. Начните использование!

### Способ 2: Ручная установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/Eugeneofficial/PC-Manager-Bot.git
cd PC-Manager-Bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройка:
- Создайте config.json с вашим токеном Telegram бота и ID пользователя
- Включите нужные плагины

4. Запуск:
```bash
python bot.py
```

## Требования
- Windows 10/11
- Python 3.8+
- Доступ в интернет
- Права администратора (для некоторых функций)

## Разработка
- Написан на Python
- Использует python-telegram-bot
- Архитектура на основе плагинов
- Лицензия MIT

## License | Лицензия
MIT License

