import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.__init__ import create_app
from app.sqlite_process import auto_process_db

SOCKET_IO = None

if __name__ == "__main__":
    auto_process_db()
    app, SOCKET_IO = create_app()
    SOCKET_IO.run(app, debug=True, host="0.0.0.0", port=5002)

    @SOCKET_IO.on("connect")
    def handle_connect():
        print("\033[92mClient connected\033[0m")

    @SOCKET_IO.on("disconnect")
    def handle_disconnect():
        print("\033[91mClient disconnected during processing\033[0m")
        # socketio.emit("log", {"message": "Client disconnected during processing"})
