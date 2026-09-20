import pytesseract
import time
import threading
import os
from PIL import ImageGrab
import winsound

# Caminho do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Timer do Dota 2 (ajuste conforme sua resolução)
TIMER_BOX = (932, 20, 986, 37)

# Sons dos eventos
AUDIO_PATHS = {
    "stack": "sounds/stack.wav",
    "bounty_rune": "sounds/bounty_rune.wav",
    "power_rune": "sounds/power_rune.wav",
    "xp_rune": "sounds/xp_rune.wav",
    "lotus": "sounds/lotus.wav"
}

# Últimos tempos notificados (para evitar spam)
last_notified = {}

# Delay mínimo entre alertas (segundos)
NOTIFY_COOLDOWN = 10

def get_event_times():
    return {
        "stack": [i * 60 + 42 for i in range(60)],
        "bounty_rune": [i * 60 - 12 for i in range(0, 60, 4)],
        "power_rune": [i * 60 - 13 for i in range(6, 120, 2) if i * 60 - 13 > 0],
        "xp_rune": [i * 60 - 18 for i in range(7, 120, 7) if i * 60 - 18 > 0],
        "lotus": [i * 60 - 10 for i in range(3, 120, 3) if i * 60 - 10 > 0]
    }

def read_timer():
    img = ImageGrab.grab(bbox=TIMER_BOX)
    text = pytesseract.image_to_string(img, config='--psm 7')
    return text.strip().replace('\n', '').replace(' ', '')

def time_to_seconds(timer_text):
    try:
        minutes, seconds = map(int, timer_text.split(":"))
        return minutes * 60 + seconds
    except:
        return None

def play_sound(event_name):
    path = AUDIO_PATHS.get(event_name)
    if path and os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

def notifier(event_name):
    now = time.time()
    last_time = last_notified.get(event_name, 0)
    if now - last_time < NOTIFY_COOLDOWN:
        return  # Ignora alertas muito próximos

    last_notified[event_name] = now

    if event_name == "stack":
        print("[ALERTA] Hora de stackar!")
    elif event_name == "bounty_rune":
        print("[ALERTA] Runa: Bounty rune")
    elif event_name == "power_rune":
        print("[ALERTA] Runa: Power rune")
    elif event_name == "xp_rune":
        print("[ALERTA] Tempo de XP Rune!")
    elif event_name == "lotus":
        print("[ALERTA] Lotus em breve!")

    play_sound(event_name)

def monitor():
    last_time = -1
    events = get_event_times()
    print("Monitorando o tempo de jogo...")

    while True:
        timer_text = read_timer()
        current_time = time_to_seconds(timer_text)

        if current_time is not None and current_time != last_time:
            last_time = current_time

            for event_name, times in events.items():
                for event_time in times:
                    if event_time - 1 <= current_time <= event_time:
                        threading.Thread(target=notifier, args=(event_name,), daemon=True).start()

        time.sleep(1)

if __name__ == "__main__":
    monitor()
