import speech_recognition as sr
from pynput import mouse
import pyautogui

# Global variable to track the program's state
is_running = False

# Function to handle mouse click events
def on_click(x, y, button, pressed):
    global is_running
    if pressed and not is_running:
        is_running = True
        print("Program started.")
        listen_to_speech()
    elif pressed and is_running:
        is_running = False
        print("Program stopped.")

# Function to listen to user's speech
def listen_to_speech():
    global is_running
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        while is_running:
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio).lower()
                print("You said:", command)
                if command == "start":
                    is_running = True
                    print("Game already started.")
                elif command == "stop":
                    is_running = False
                    print("Program stopped.")
                elif command == "up":
                    pyautogui.press('up')
                elif command == "down":
                    pyautogui.press('down')
                elif command == "restart":
                    print("Program restarting...")
                    is_running = False
                    pyautogui.press('r')
                    break
                elif command == "quit":
                    print("Quitting program...")
                    is_running = False
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

# Function to start mouse listener
def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    print("Click the mouse to start the program.")
    start_mouse_listener()
 