import sys
import json
import os
import subprocess
import hashlib
import zipfile
import tempfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from cryptography.fernet import Fernet

class YanDesksurf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.load_config()
        self.enable_3d_acceleration()
        self.optimize_webgl_settings()

    def enable_3d_acceleration(self):
        self.browser.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)

    def optimize_webgl_settings(self):
        self.browser.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)

    def load_config(self):
        try:
            with open('yansurf.json', 'r') as f:
                config = json.load(f)
                yansurf_file = config.get('yansurf_file')
                encryption_key = config.get('encryption_key')
                window_options = config.get('window_options', {})
                self.apply_window_options(window_options)

                if yansurf_file and encryption_key:
                    self.load_encrypted_app(yansurf_file, encryption_key)
                else:
                    self.configure_new_app()
        except FileNotFoundError:
            self.configure_new_app()

    def apply_window_options(self, options):
        self.resize(options.get('width', 800), options.get('height', 600))
        self.setFixedSize(options.get('width', 800), options.get('height', 600)) if not options.get('resizable', True) else None
        self.showFullScreen() if options.get('fullscreen', False) else None

    def load_encrypted_app(self, yansurf_file, encryption_key):
        fernet = Fernet(encryption_key)
        with open(yansurf_file, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        temp_dir = tempfile.mkdtemp()
        with open(os.path.join(temp_dir, 'temp.zip'), 'wb') as temp_file:
            temp_file.write(decrypted_data)

        with zipfile.ZipFile(os.path.join(temp_dir, 'temp.zip'), 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        index_html_path = os.path.join(temp_dir, 'index.html')
        self.browser.load(QUrl.fromLocalFile(index_html_path))
        self.load_yanprog()

    def load_yanprog(self):
        try:
            with open('yanprog.yanprog', 'r') as file:
                for line in file:
                    if "create_file" in line:
                        filename = line.split()[1]
                        open(filename, 'w').close()
                    elif "delete_file" in line:
                        filename = line.split()[1]
                        os.remove(filename)
                    elif "rename_file" in line:
                        src, dst = line.split()[1:3]
                        os.rename(src, dst)
                    elif "move_file" in line:
                        src, dst = line.split()[1:3]
                        os.rename(src, dst)
                    elif "run_command" in line:
                        command = line.split()[1:]
                        subprocess.run(command, shell=True)
        except FileNotFoundError:
            pass

        self.monitor_dom_changes()

    def monitor_dom_changes(self):
        self.browser.page().titleChanged.connect(self.on_title_changed)
        self.browser.page().contentsSizeChanged.connect(self.on_contents_changed)
        QTimer.singleShot(5000, self.check_page_hash)  

    def on_title_changed(self, title):
        print(f"Title changed to: {title}")
        self.evaluate_yanprog_conditions("title", title)

    def on_contents_changed(self):
        print("Contents of the page have changed.")
        self.evaluate_yanprog_conditions("dom", None)

    def check_page_hash(self):
        self.browser.page().runJavaScript("document.documentElement.outerHTML", self.evaluate_page_hash)

    def evaluate_page_hash(self, html):
        page_hash = hashlib.sha256(html.encode()).hexdigest()
        print(f"Page hash: {page_hash}")
        self.evaluate_yanprog_conditions("hash", page_hash)
        QTimer.singleShot(5000, self.check_page_hash)  

    def evaluate_yanprog_conditions(self, event_type, value):
        pass

    def configure_new_app(self):
        options = QFileDialog.Options()
        zip_file, _ = QFileDialog.getOpenFileName(self, "Select a .zip file to encrypt", "", "Zip Files (*.zip)", options=options)
        if zip_file:
            encryption_key = Fernet.generate_key()
            fernet = Fernet(encryption_key)
            with open(zip_file, 'rb') as file:
                zip_data = file.read()
            encrypted_data = fernet.encrypt(zip_data)
            yansurf_file = zip_file.replace('.zip', '.yansurf')
            with open(yansurf_file, 'wb') as file:
                file.write(encrypted_data)
            with open('yansurf.json', 'w') as f:
                json.dump({'yansurf_file': yansurf_file, 'encryption_key': encryption_key.decode()}, f)
            QMessageBox.information(self, "Configuration", f"Created {yansurf_file} with encryption key: {encryption_key.decode()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YanDesksurf()
    ex.show()
    sys.exit(app.exec_())