# Bitcoin Network Fee Checker + Telegram Alerts

Простой чекер комиссий Bitcoin (sat/vB) с мгновенными уведомлениями в Telegram, когда сеть становится дешёвой.

Идеально подходит для OTC-трейдеров, консолидации UTXO, снайпа ординалов, рун и просто крупных переводов BTC.

## 🚀 Особенности
- Проверка каждые **30 секунд** через API mempool.space  
- Уведомления приходят только если комиссия **≤ твоего порога**
- Сообщение, когда комиссия снова выросла
- Работает **24/7** на любом сервере, VPS или домашнем ПК

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/edotoday/Bitcoin-Network-Fee-Checker.git
cd Bitcoin-Network-Fee-Checker
```

---

### 2. Установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Настройка `.env`

```bash
cp .env.example .env
nano .env
```

Пример содержимого:

```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=-1001234567890
FEE_THRESHOLD_SAT_VB=15      # алерт при 15 sat/vB и ниже (меняй под себя)
CHECK_INTERVAL=30
```

---

## 🤖 Создание Telegram-бота

1. Написать **@BotFather**  
2. Команда `/newbot` → получить токен  
3. Написать своему боту любое сообщение  
4. Узнать `chat_id`:  

```
https://api.telegram.org/bot<ТОКЕН>/getUpdates
```

---

## ▶️ Запуск

```bash
python checker.py
```

---

## 🟢 Запуск 24/7

### 1) Через `screen` (самый простой способ)

```bash
screen -S btcfee
python checker.py
```

Отсоединиться: **Ctrl + A**, затем **D**  
Вернуться:

```bash
screen -r btcfee
```

---

### 2) Через `systemd` (VPS)

Создать сервис:

```bash
sudo nano /etc/systemd/system/btcfee.service
```

Содержимое файла:

```ini
[Unit]
Description=Bitcoin Network Fee Checker
After=network.target

[Service]
WorkingDirectory=/home/user/btc-fee-checker
ExecStart=/home/user/Bitcoin-Network-Fee-Checker/venv/bin/python /home/user/btc-fee-checker/checker.py
Restart=always
RestartSec=10
User=user

[Install]
WantedBy=multi-user.target
```

Активировать сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now btcfee.service
```

---

## 🎉 Готово!

Теперь ты никогда не пропустишь момент, когда **Bitcoin-сеть дешёвая**.

Автор: **[@edotoday_eth](https://x.com/edotoday_eth)**




