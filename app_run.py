import os
import sys
import logging
import time
import requests
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
from PyQt5.QtCore import QUrl, Qt, QTimer
from threading import Thread
import logging
import traceback
import requests
import multiprocessing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from waitress_server.server import run_flask, stop_waitress

def run_flask_and_connect(msg, window):
    def flask_wrapper():
        try:
            run_flask()
        except Exception as e:
            logging.error(f"Flask error: {str(e)}")
            logging.error(traceback.format_exc())

    flask_thread = Thread(target=flask_wrapper)
    flask_thread.daemon = True
    flask_thread.start()

    # Wait for Flask to start (with timeout)
    start_time = time.time()
    while time.time() - start_time < 30:  # 30 second timeout
        try:
            response = requests.get("http://127.0.0.1:5002", timeout=1)
            if response.status_code == 200:
                window.browser.setUrl(QUrl("http://127.0.0.1:5002"))
                window.showMaximized()
                msg.close()
                return
        except requests.RequestException:
            time.sleep(0.5)

    logging.error("Flask server failed to start within 30 seconds")
    QMessageBox.critical(
        None, "Error", "Failed to start the application. Please check the logs."
    )

if __name__ == "__main__":
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    # log_file_path = os.path.join(download_folder, "app.log")
    # logging.basicConfig(filename=log_file_path, level=logging.DEBUG)

    # os.environ["VALIDATE_DOWNLOAD_SAVE_FOLDER"] = (
    #     os.path.expanduser("~") + "/downloads/"
    # )
    # os.makedirs(os.environ.get("VALIDATE_DOWNLOAD_SAVE_FOLDER"), exist_ok=True)
    multiprocessing.freeze_support()

    def show_startup_message():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The application is starting. Please wait...")
        msg.setWindowTitle("Startup")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        return msg

    # Start the PyQt5 application
    app = QApplication(sys.argv)
    logging.info("Check")
    msg = show_startup_message()
    window = MainWindow()
    # Run the flask server and connect to the URL
    run_flask_and_connect(msg, window)

    def cleanup():
        stop_waitress()  # No action needed for Waitress
        app.quit()

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec_())