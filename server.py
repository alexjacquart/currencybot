from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Твой Telegram-бот
BOT_TOKEN = "8064353519:AAGqu6DXLbldnJLJ6OlkxqWH5d4xYbfycI8"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1"

# Базовый курс
current_rate = 100.00  

@app.route("/getrate", methods=["GET"])
def get_rate():
    """Отдаём текущий курс для сайта"""
    return jsonify({"rate": current_rate})

@app.route("/update", methods=["GET"])
def update_rate():
    """Получаем курс из последнего сообщения в Telegram"""
    global current_rate
    try:
        response = requests.get(TELEGRAM_API_URL)
        data = response.json()

        if data.get("ok") and data.get("result"):
            last_message = data["result"][-1]["message"]["text"]
            new_rate = float(last_message) if last_message.replace(".", "", 1).isdigit() else None
            if new_rate:
                current_rate = new_rate
                return jsonify({"status": "success", "rate": current_rate})
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"status": "error", "message": "No valid rate found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
