import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException

class AddPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        # sets up the window to add new patients
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Add Patient")

        layout1 = QGridLayout()

        label_phn = QLabel("Patient Health Number")
        self.text_phn = QLineEdit()
        self.text_phn.setInputMask("00000000")
        label_name = QLabel("Name")
        self.text_name = QLineEdit()
        label_birth_date = QLabel("Birthdate")
        self.text_birth_date = QLineEdit()
        label_phone = QLabel("Phone Number")
        self.text_phone = QLineEdit()
        label_email = QLabel("Email")
        self.text_email = QLineEdit()
        label_address = QLabel("Address")
        self.text_address = QLineEdit()

        self.text_phn.textChanged.connect(self.patient_text_changed)
        self.text_name.textChanged.connect(self.patient_text_changed)
        self.text_birth_date.textChanged.connect(self.patient_text_changed)
        self.text_phone.textChanged.connect(self.patient_text_changed)
        self.text_email.textChanged.connect(self.patient_text_changed)
        self.text_address.textChanged.connect(self.patient_text_changed)

        layout1.addWidget(label_phn, 0, 0)
        layout1.addWidget(self.text_phn, 0, 1)
        layout1.addWidget(label_name, 1, 0)
        layout1.addWidget(self.text_name, 1, 1)
        layout1.addWidget(label_birth_date, 2, 0)
        layout1.addWidget(self.text_birth_date, 2, 1)
        layout1.addWidget(label_phone, 3, 0)
        layout1.addWidget(self.text_phone, 3, 1)
        layout1.addWidget(label_email, 4, 0)
        layout1.addWidget(self.text_email, 4, 1)
        layout1.addWidget(label_address, 5, 0)
        layout1.addWidget(self.text_address, 5, 1)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        self.button_add = QPushButton("Add")
        self.button_close = QPushButton("Close")
        layout2.addWidget(self.button_clear)
        layout2.addWidget(self.button_add)
        layout2.addWidget(self.button_close)
        self.button_add.setEnabled(False)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)
        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)
        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(layout3)
        self.setCentralWidget(widget)

        self.button_add.clicked.connect(self.add_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)

        self.text_phn.setEnabled(True)
        self.text_name.setEnabled(True)
        self.text_birth_date.setEnabled(True)
        self.text_phone.setEnabled(True)
        self.text_email.setEnabled(True)
        self.text_address.setEnabled(True)
    
    # checks if any of the patient fields have been changed
    def patient_text_changed(self):
        if self.text_phn.text() and self.text_name.text() and self.text_birth_date.text() \
            and self.text_phone.text() and self.text_email.text() and self.text_address.text():
            self.button_add.setEnabled(True)
        else:
            self.button_add.setEnabled(False)

    # clears all the patient fields
    def clear_button_clicked(self):
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")

    # adds a new patient with the inputted fields
    def add_button_clicked(self):
        try:
            phn = int(self.text_phn.text())
            name = self.text_name.text()
            birth_date = self.text_birth_date.text()
            phone = self.text_phone.text()
            email = self.text_email.text()
            address = self.text_address.text()
            self.controller.create_patient(phn, name, birth_date, phone, email, address)

            self.parent.refresh_table()
            self.close_button_clicked()
        except ValueError:
            message = QMessageBox.warning(self, "Invliad PHN", "Please enter a numerical patient health number.")
        except IllegalOperationException:
            message = QMessageBox.warning(self, "Invalid Operation", "A patient with this patient health number already exists in the system.")
    
    # closes this window
    def close_button_clicked(self):
        self.clear_button_clicked()
        self.hide()

    # closes everything
    def closeEvent(self, event):
        self.close_button_clicked()
