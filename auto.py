import keyboard
import time
import random
import threading
import numpy as np
from mss import mss
from PIL import Image

# ================== CONFIG ==================
WALK_SPEED = 0.22
WALK_DURATION = 15        # Changed to 15 seconds as requested
BATTLE_SPAM_DURATION = 60

running = True
auto_cycle = False
in_battle = False

sct = mss()
# ===========================================

def stop_movement():
    for key in ['w', 'a', 's', 'd']:
        keyboard.release(key)

def walk_phase():
    print(f"🚶 Walking for {WALK_DURATION} seconds...")
    directions = ['w', 'a', 's', 'd']
    start = time.time()
    while time.time() - start < WALK_DURATION and not in_battle and running:
        direction = random.choice(directions)
        keyboard.press(direction)
        time.sleep(WALK_SPEED)
        keyboard.release(direction)
        if random.random() < 0.22:
            time.sleep(random.uniform(0.15, 0.4))
    stop_movement()

def battle_phase():
    global in_battle
    print(f"⚔️ Spamming Enter for {BATTLE_SPAM_DURATION} seconds...")
    end = time.time() + BATTLE_SPAM_DURATION
    while time.time() < end and in_battle and running:
        keyboard.press_and_release('enter')
        time.sleep(0.23)
    print("Battle phase finished")
    in_battle = False
    stop_movement()

def auto_cycle_loop():
    global auto_cycle, in_battle
    while running and auto_cycle:
        if in_battle:
            time.sleep(1)
            continue
        walk_phase()
        time.sleep(0.5)
        in_battle = True
        battle_phase()
        time.sleep(0.5)

def battle_detector():
    global in_battle
    while running:
        try:
            screenshot = sct.grab((0, 0, 1920, 1080))
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            pixels = np.array(img)
            dark = np.all(pixels < 30, axis=2)
            if np.sum(dark) / dark.size > 0.82 and not in_battle:
                in_battle = True
                stop_movement()
                print("⚔️ BLACK SCREEN DETECTED")
                threading.Thread(target=battle_phase, daemon=True).start()
        except:
            pass
        time.sleep(0.18)

def toggle_auto_cycle():
    global auto_cycle
    auto_cycle = not auto_cycle
    if auto_cycle:
        print("🔄 FULL AUTO CYCLE STARTED (Walk 7s → Enter Spam 60s → Repeat)")
        threading.Thread(target=auto_cycle_loop, daemon=True).start()
    else:
        print("Auto Cycle STOPPED")
        stop_movement()

def manual_battle():
    global in_battle
    in_battle = not in_battle
    if in_battle:
        stop_movement()
        print("⚔️ MANUAL BATTLE MODE ON")
        threading.Thread(target=battle_phase, daemon=True).start()
    else:
        print("Manual Battle OFF")
        stop_movement()

def main():
    print("="*90)
    print("FF9 Auto Script - Walk 7s → Battle 60s")
    print("="*90)
    print("Controls:")
    print("   2     → Toggle Full Auto Cycle (Walk 15s → Spam Enter 60s)")
    print("   3     → Manual Battle Mode")
    print("   ESC   → Quit")
    print("="*90)

    keyboard.add_hotkey('2', toggle_auto_cycle)
    keyboard.add_hotkey('3', manual_battle)

    threading.Thread(target=battle_detector, daemon=True).start()

    while running:
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        print("Script ready! Press 2 to start auto cycle")
        main()
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        stop_movement()
        print("Script stopped.")