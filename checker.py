# checker.py
import time
import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, FEE_THRESHOLD_SAT_VB, CHECK_INTERVAL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Бесплатный и надёжный API (можно заменить на mempool.space своего узла)
API_URL = "https://mempool.space/api/v1/fees/recommended"

last_notified_fee = None
notified_low = False

def get_current_fee_sat_vb():
    try:
        r = requests.get(API_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # берём средний приоритет — обычно самый актуальный для обычных транзакций
            return data["fastestFee"]  # можно поменять на "halfHourFee" или "hourFee"
        else:
            logging.error(f"API error: {r.status_code}")
            return None
    except Exception as e:
        logging.error(f"Request failed: {e}")
}        return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

def main():
    global last_notified_fee, notified_low

    logging.info("BTC Fee Checker запущен")
    send_telegram_message("BTC Fee Checker запущен\nЖду низкие комиссии...")

    while True:
        fee = get_current_fee_sat_vb()
        if fee is None:
            time.sleep(CHECK_INTERVAL)
            continue

        message = f"<b>Bitcoin Network Fee</b>\n<code>{fee}</code> sat/vB"

        should_notify = False

        if fee <= FEE_THRESHOLD_SAT_VB and not notified_low:
            should_notify = True
            notified_low = True
            message = f"<b>НИЗКАЯ КОМИССИЯ НА BITCOIN!</b>\n<code>{fee}</code> sat/vB\nСамое время отправлять BTC / ординалы / руны!"
        elif fee > FEE_THRESHOLD_SAT_VB and notified_low:
            should_notify = True
            notified_low = False
            message = f"Комиссия снова выросла: <code>{fee}</code> sat/vB"

        # опционально — уведомление при сильном изменении
        if last_notified_fee is not None and abs(fee - last_notified_fee) >= 30:
            should_notify = True

        if should_notify or last_notified_fee is None:
            logging.info(f"Fee: {fee} sat/vB")
            send_telegram_message(message)
            last_notified_fee = fee

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
