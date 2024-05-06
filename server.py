import os
import openai
import requests
from flask import Flask, request, jsonify

# Загрузка API-ключей из переменных окружения
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Создание экземпляра Flask-приложения
app = Flask(__name__)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    if 'message' not in data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    # Извлечение текста сообщения и идентификатора чата
    message = data['message']['text']
    chat_id = data['message']['chat']['id']

    # Получение ответа от OpenAI GPT
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=100
    )
    reply_text = response.choices[0].text.strip()

    # Отправка ответа обратно в Telegram
    payload = {'chat_id': chat_id, 'text': reply_text}
    response = requests.post(TELEGRAM_API_URL, json=payload)

    return jsonify({"status": "success"})

# Запуск сервера Flask на заданном порте
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
