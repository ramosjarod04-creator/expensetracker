import os
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://127.0.0.1:8000/")

if __name__ == "__main__":
    # open the browser after a short delay
    threading.Timer(1.5, open_browser).start()
    os.system("python manage.py runserver")
