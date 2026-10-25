import time
import threading
import pytesseract
import pyautogui
from PIL import ImageGrab

# -----------------------------
# TESSERACT PATH
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

running = False

# -----------------------------
# WORDS TO LOOK FOR
# -----------------------------
TARGET_WORDS = [
    "close",
    "skip",
    "skip ad",
    "skip ads",
    "skip advertisement",
    "continue",
    "dismiss",
    "not now",
    "no thanks",
]

BLACKLIST_WORDS = [
    "chrome",
    "firefox",
    "edge",
    "discord",
    "explorer",
]

# -----------------------------
# OCR SCAN
# -----------------------------
def scan_screen():
    img = ImageGrab.grab()

    data = pytesseract.image_to_data(
        img,
        output_type=pytesseract.Output.DICT
    )

    for i in range(len(data["text"])):

        text = data["text"][i].strip().lower()

        if not text:
            continue

        for target in TARGET_WORDS:

            if target in text:

                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                center_x = x + w // 2
                center_y = y + h // 2

                print(
                    f"Found '{text}' -> clicking "
                    f"{center_x}, {center_y}"
                )

                pyautogui.click(center_x, center_y)
                return True

    return False


# -----------------------------
# MAIN OCR LOOP
# -----------------------------
def watcher():

    global running

    print("Watcher thread started")

    while True:

        if running:
            try:
                scan_screen()
            except Exception as e:
                print("OCR Error:", e)

        time.sleep(1)


# -----------------------------
# TOGGLE KEY
# -----------------------------
def toggle_loop():

    global running

    import keyboard

    while True:

        if keyboard.is_pressed("f1"):
            running = not running

            print(
                f"Watcher {'ENABLED' if running else 'DISABLED'}"
            )

            time.sleep(0.3)

        time.sleep(0.05)


# -----------------------------
# START THREADS
# -----------------------------
threading.Thread(
    target=watcher,
    daemon=True
).start()

threading.Thread(
    target=toggle_loop,
    daemon=True
).start()

print("Press F1 to enable/disable")

# -----------------------------
# KEEP ALIVE
# -----------------------------
while True:
    time.sleep(1)