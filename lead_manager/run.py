import subprocess
import sys
import time
import threading
import webbrowser
import os

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    threading.Thread(target=open_browser, daemon=True).start()
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
