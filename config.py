from decouple import config

TELEGRAM_BOT_TOKEN   = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID     = config('TELEGRAM_CHAT_ID')
FEE_THRESHOLD_SAT_VB = config('FEE_THRESHOLD_SAT_VB', default=15, cast=int)  # алерт ниже 15 sat/vB
CHECK_INTERVAL       = config('CHECK_INTERVAL', default=30, cast=int)       # секунд
