import time
import requests

# === INSERISCI QUI I TUOI DATI ===
TELEGRAM_TOKEN = "8782623879:AAFqgQc5utGotjQNYhJtmhNnx6rF4oyQzn8"
CHAT_ID = "5138499845"

# Configurazione
CHECK_INTERVAL = 15  # Controlla ogni 15 secondi
SPAM_COUNT = 50      # Numero di messaggi per tempestarti di notifiche

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Errore Telegram: {e}")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    }
    try:
        # Verifica la pagina del prodotto Wooting 80HE
        res = requests.get("https://wooting.io/wooting-80he", headers=headers, timeout=10)
        if res.status_code == 200:
            content = res.text.lower()
            # Se trova diciture di acquisto immediato (non in pre-ordine esaurito)
            if "add to cart" in content or "in stock" in content:
                return True
    except Exception as e:
        print(f"Errore controllo: {e}")
    return False

def main():
    print("Bot avviato...")
    send_telegram("🤖 **Bot Wooting 80HE attivato dal telefono!**")
    already_notified = False

    while True:
        if check_stock():
            if not already_notified:
                print("WOOTING DISPONIBILE!")
                for i in range(SPAM_COUNT):
                    send_telegram(
                        f"🚨 **WOOTING 80HE È IN STOCK!** 🚨\n\n"
                        f"🏃‍♂️ Corri a comprarla ora!\n"
                        f"🔗 https://wooting.io/wooting-80he\n\n"
                        f"*(Notifica {i+1}/{SPAM_COUNT})*"
                    )
                    time.sleep(0.3)
                already_notified = True
        else:
            already_notified = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

