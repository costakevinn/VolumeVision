import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2

import config

TITLE = "VolumeVision"
HEADER = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
PAGE = (
    b"<title>VolumeVision</title>"
    b'<body style="margin:0;background:#000"><img src="/stream" style="max-width:100%">'
)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/stream":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(PAGE)
            return
        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.end_headers()
        try:
            while True:
                jpeg = self.server.window.jpeg
                if jpeg:
                    self.wfile.write(HEADER + jpeg + b"\r\n")
                time.sleep(1 / 30)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *args):
        pass


class Window:
    def __init__(self):
        self.web = config.WINDOW == "web"
        self.jpeg = None
        if self.web:
            self.server = ThreadingHTTPServer(("0.0.0.0", config.WINDOW_PORT), Handler)
            self.server.daemon_threads = True
            self.server.window = self
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
            print(f"Window: http://localhost:{config.WINDOW_PORT}", flush=True)

    def show(self, frame):
        if self.web:
            self.jpeg = cv2.imencode(".jpg", frame)[1].tobytes()
            return True
        cv2.imshow(TITLE, frame)
        if cv2.waitKey(1) == ord("q"):
            return False
        try:
            return cv2.getWindowProperty(TITLE, cv2.WND_PROP_VISIBLE) >= 1
        except cv2.error:
            return False

    def close(self):
        if self.web:
            self.server.shutdown()
        else:
            cv2.destroyAllWindows()