import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.setWindowFlags(
            Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint
        )

        # Connect the downloadRequested signal to a custom slot
        self.browser.page().profile().downloadRequested.connect(self.handle_download)

    def handle_download(self, download):
        # Define custom download behavior
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        download_folder = QFileDialog.getExistingDirectory(
            self, "Select Download Folder", os.path.expanduser("~"), options
        )
        if download_folder:
            download.setPath(download_folder)  # Set download path
            download.accept()  # Start the download
        else:
            download.cancel()  # Cancel the download if no folder is selected
