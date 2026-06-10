import os
import threading
import time
import urllib.request
import webbrowser

from sigma_app import create_app


app = create_app()


def get_run_options():
    return {
        "host": os.environ.get("HOST", "127.0.0.1"),
        "port": int(os.environ.get("PORT", "5000")),
        "debug": os.environ.get("FLASK_DEBUG", "0") == "1",
    }


def open_browser_when_ready(host, port):
    url = f"http://{host}:{port}"
    for _ in range(50):
        try:
            with urllib.request.urlopen(url):
                break
        except Exception:
            time.sleep(0.2)
    webbrowser.open(url)


if __name__ == "__main__":
    run_options = get_run_options()
    threading.Thread(
        target=open_browser_when_ready,
        args=(run_options["host"], run_options["port"]),
        daemon=True,
    ).start()
    app.run(**run_options)