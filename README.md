# PC Manager Bot / Бот для управления ПК

[English](#english) | [Русский](#russian)

## English

A Telegram bot for remote PC management with extensive functionality and plugin support.

### Features

- System monitoring (CPU, RAM, disk usage)
- Screenshot capture
- Camera access
- Audio recording
- Process management
- Power control
- File system access
- Admin rights management
- System settings control
- Hardware monitoring
- Network management
- And many more...

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `config.json` with your Telegram bot token and authorized user ID:
```json
{
    "TELEGRAM_TOKEN": "YOUR_BOT_TOKEN",
    "AUTHORIZED_USERS": [YOUR_USER_ID]
}
```
4. Run the bot:
```bash
python bot.py
```

### Updates in v2.0

- Added plugin system support
- Improved system monitoring capabilities
- Added new administrative functions
- Enhanced security features
- Added extensive logging
- Improved error handling
- Added new UI controls

## Russian

Telegram бот для удаленного управления компьютером с расширенным функционалом и поддержкой плагинов.

### Возможности

- Мониторинг системы (CPU, RAM, диски)
- Создание скриншотов
- Доступ к камере
- Запись аудио
- Управление процессами
- Управление питанием
- Доступ к файловой системе
- Управление правами администратора
- Управление настройками системы
- Мониторинг оборудования
- Управление сетью
- И многое другое...

### Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Создайте файл `config.json` с вашим токеном бота Telegram и ID пользователя:
```json
{
    "TELEGRAM_TOKEN": "ВАШ_ТОКЕН_БОТА",
    "AUTHORIZED_USERS": [ВАШ_ID_ПОЛЬЗОВАТЕЛЯ]
}
```
4. Запустите бота:
```bash
python bot.py
```

### Обновления в версии 2.0

- Добавлена поддержка системы плагинов
- Улучшены возможности мониторинга системы
- Добавлены новые административные функции
- Улучшена система безопасности
- Добавлено расширенное логирование
- Улучшена обработка ошибок
- Добавлены новые элементы управления

