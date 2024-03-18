import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic, QtCore

class RDPLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        uic.loadUi("LogIn.ui", self)
        self.Password.returnPressed.connect(self.on_login_button_clicked)
        self.Entrar.clicked.connect(self.on_login_button_clicked)

    def connect_to_rdp(self, username, password):
        # Replace placeholders with your RDP server address and username
        rdp_server = os.environ.get('RdpServer','')
        rdp_username = username

        # Construct xfreerdp command with provided username and password
        command = [
            "xfreerdp",
            "/v:" + rdp_server,
            "/u:" + rdp_username,
            "/p:" + password,
	    "/dynamic-resolution",
            "/printer",
            "/cert-ignore",  # Ignore certificate errors (optional)
	    "+aero",
            "+clipboard"
        ]

        # Launch xfreerdp process
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            # Handle any errors occurred during the connection
            QMessageBox.critical(None, "Error", f"Failed to connect: {e}")

    def on_login_button_clicked(self):
        username = self.User.text()
        password = self.Password.text()

        if username and password:
            self.connect_to_rdp(username, password)
            self.User.clear()
            self.Password.clear()
        else:
            QMessageBox.warning(None, "Warning", "Please enter both username and password.")

def main():
    app = QApplication(sys.argv)
    window = RDPLoginWindow()
#    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
