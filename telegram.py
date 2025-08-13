import requests

token = '7595974861:AAHwcITO9a1DMrUvAnKXxM3eM_plmkB-2m4'


def sendMessage(chat_id, message):
    """
    Sends a text message to a specified Telegram chat.
    
    Args:
        chat_id (str): The ID of the target chat.
        message (str): The text message to send.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
