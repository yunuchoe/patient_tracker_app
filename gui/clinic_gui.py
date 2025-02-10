import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout

from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.gui.clinic_home_gui import ClinicHomeGUI

class ClinicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # setting up for login screen
        self.controller = Controller(False)
        self.clinic_home = None
        self.setWindowTitle("Login")

        self.login_layout = QGridLayout()

        self.label_username = QLabel("Username")
        self.text_username = QLineEdit()
        self.text_username.setPlaceholderText("Username")

        self.label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.text_password.setPlaceholderText("Password")

        self.login_button = QPushButton("Login")
        self.quit_button = QPushButton("Quit")

        # formatting login screen
        self.login_layout.addWidget(self.label_username, 0, 0)
        self.login_layout.addWidget(self.text_username, 0, 1)

        self.login_layout.addWidget(self.label_password, 1, 0)
        self.login_layout.addWidget(self.text_password, 1, 1)

        self.login_layout.addWidget(self.login_button, 2, 0)
        self.login_layout.addWidget(self.quit_button, 2, 1)

        # connect the buttons clicked signals to the slots below
        self.login_button.clicked.connect(self.login_button_clicked)
        self.quit_button.clicked.connect(self.quit_button_clicked)

        self.login_widget = QWidget()
        self.login_widget.setLayout(self.login_layout)
        self.setCentralWidget(self.login_widget)

        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        print(center_point)
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def login_button_clicked(self):
        """ Handles controller login """

        username = self.text_username.text()
        password = self.text_password.text()

        try:
            self.controller.login(username, password)

            auto_dlg = QMessageBox(self)
            auto_dlg.setWindowTitle("Autosave Set")
            auto_dlg.setText("You are now logged in. Would you like to turn on autosave?")
            auto_dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No)
            button = auto_dlg.exec()

            # turn autosave on
            if button == QMessageBox.StandardButton.Ok:
                self.controller = Controller(True)       
                self.controller.login(username, password)
            #turn autosave off - default option
            else:
                self.controller = Controller(False)
                self.controller.login(username, password)

            self.text_username.setText("")
            self.text_password.setText("")
            self.hide()
            self.clinic_home = ClinicHomeGUI(self.controller, self)
            self.clinic_home.show()

        # login failed
        except InvalidLoginException:
            message = QMessageBox.warning(self, "Login Failure", "Your username or password is incorrect. Please try again.")
            self.text_password.setText("")

    def quit_button_clicked(self):
        """ Quit the program """
        sys.exit()



def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
