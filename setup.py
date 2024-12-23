import os
import json
import psutil
import webbrowser
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

def load_config():
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
    return {'TELEGRAM_TOKEN': '', 'AUTHORIZED_USERS': []}

def save_config(data):
    try:
        # Проверяем данные
        if not data.get('token'):
            return False, "Введите токен бота"
        if not data.get('user_ids'):
            return False, "Введите ID пользователей"
            
        # Преобразуем ID пользователей
        try:
            user_ids = [int(id.strip()) for id in data['user_ids'].split(',')]
        except:
            return False, "Неверный формат ID пользователей"
            
        # Сохраняем конфигурацию
        config = {
            'TELEGRAM_TOKEN': data['token'],
            'AUTHORIZED_USERS': user_ids
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
        # Перезапускаем бота
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower() and 'bot.py' in str(proc.info['cmdline']):
                    proc.kill()
            except:
                pass
                
        os.system('start cmd /k python bot.py')
        return True, "Настройки сохранены! Бот запущен."
        
    except Exception as e:
        return False, f"Ошибка: {str(e)}"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PC Manager Bot</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial;
            margin: 0;
            padding: 20px;
            background: #f0f2f5;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a73e8;
            margin-bottom: 30px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #666;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 14px;
        }
        .btn {
            background: #1a73e8;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .btn:hover {
            background: #1557b0;
        }
        .error {
            color: #d32f2f;
            margin-top: 5px;
            font-size: 14px;
        }
        .success {
            color: #388e3c;
            margin-top: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PC Manager Bot</h1>
        <form id="configForm">
            <div class="form-group">
                <label>Telegram Bot Token:</label>
                <input type="text" id="token" placeholder="Введите токен бота" required>
            </div>
            
            <div class="form-group">
                <label>ID пользователей (через запятую):</label>
                <input type="text" id="user_ids" placeholder="Например: 123456789, 987654321" required>
            </div>
            
            <button type="submit" class="btn">Сохранить и запустить</button>
            <div id="message"></div>
        </form>
    </div>

    <script>
        // Загрузка настроек
        fetch('/config')
            .then(response => response.json())
            .then(config => {
                document.getElementById('token').value = config.TELEGRAM_TOKEN || '';
                document.getElementById('user_ids').value = config.AUTHORIZED_USERS ? config.AUTHORIZED_USERS.join(', ') : '';
            })
            .catch(error => {
                showMessage('Ошибка загрузки настроек', false);
            });

        // Сохранение настроек
        document.getElementById('configForm').onsubmit = function(e) {
            e.preventDefault();
            
            const data = {
                token: document.getElementById('token').value,
                user_ids: document.getElementById('user_ids').value
            };
            
            fetch('/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                showMessage(result.message, result.success);
            })
            .catch(error => {
                showMessage('Ошибка сохранения настроек', false);
            });
        };

        function showMessage(text, isSuccess) {
            const messageDiv = document.getElementById('message');
            messageDiv.className = isSuccess ? 'success' : 'error';
            messageDiv.textContent = text;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/config')
def get_config():
    return jsonify(load_config())

@app.route('/save', methods=['POST'])
def save():
    success, message = save_config(request.json)
    return jsonify({'success': success, 'message': message})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(port=5000) 