import hmac
import hashlib
from urllib.parse import parse_qs
from django.conf import settings

def verify_telegram_init_data(init_data: str) -> dict:
    """
    Проверяет подлинность initData от Telegram.
    Возвращает словарь с данными пользователя, если проверка успешна.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN не настроен в настройках.")

    # Парсим initData
    parsed_data = parse_qs(init_data)
    if not parsed_data:
        raise ValueError("Некорректный формат initData.")

    # Извлекаем подпись (hash) и удаляем её из данных
    received_hash = parsed_data.get('hash', [None])[0]
    if not received_hash:
        raise ValueError("Отсутствует hash в initData.")

    # Формируем строку для проверки
    data_check = []
    for key, value in parsed_data.items():
        if key != 'hash':
            data_check.append(f"{key}={value[0]}")
    data_check.sort()
    data_check_string = "\n".join(data_check)

    # Генерируем секретный ключ
    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    # Вычисляем HMAC-SHA256
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Проверяем подпись
    if computed_hash != received_hash:
        raise ValueError("Неверная подпись initData.")

    # Извлекаем данные пользователя
    user_data = parsed_data.get('user', [None])[0]
    if not user_data:
        raise ValueError("Отсутствуют данные пользователя в initData.")

    import json
    return json.loads(user_data)