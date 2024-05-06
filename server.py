import os
import openai
import requests
from flask import Flask, request, jsonify

# Настройте API-ключи OpenAI и Telegram, используя переменные окружения
openai.api_key = os.getenv("sk-proj-Df38V7kUQFf4KYnFCZXgT3BlbkFJMDoU0sjT2LDiF9nDTuqe")
TELEGRAM_BOT_TOKEN = os.getenv("6732894258:AAEk1Kwmel9p7HRe24PfMb0rZSwvoaGasJU")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Создайте экземпляр Flask-приложения
app = Flask(__name__)

@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    data = request.json
    # Извлеките текст сообщения и идентификатор чата
    message = data['message']['text']
    chat_id = data['message']['chat']['id']

    # Получите ответ от OpenAI GPT
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=100
    )
    reply_text = response.choices[0].text.strip()

    # Отправьте ответ обратно в Telegram
    payload = {'chat_id': chat_id, 'text': reply_text}
    response = requests.post(TELEGRAM_API_URL, json=payload)

    return jsonify({"status": "success"})

# Запустите сервер Flask на заданном порте
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
