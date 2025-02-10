import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller
from clinic.exception.illegal_operation_exception import IllegalOperationException

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller):
        # initalize the search patient window
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Search Patient")

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
        label_search_phn = QLabel("PHN:")
        self.text_search_phn = QLineEdit()
        self.text_search_phn.setInputMask('00000000')
        self.button_search = QPushButton("Search")
        self.button_search.setEnabled(False)

        layout2.addWidget(self.button_clear)
        layout2.addWidget(label_search_phn)
        layout2.addWidget(self.text_search_phn)
        layout2.addWidget(self.button_search)

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

        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)

        self.text_search_phn.textChanged.connect(self.search_text_changed)

        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)
    
    # checks if the search text bar has been changed
    def search_text_changed(self):
        """ Enable the search button """
        if self.text_search_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    # clears all the text fields
    def clear_button_clicked(self):
        """ Clear the text from all of the fields """
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")

    # searches for the patient given the phn
    def search_button_clicked(self):
        """ Search a patient in the system """
        phn = int(self.text_search_phn.text())
        patient = self.controller.search_patient(phn)

        if patient:
            self.text_phn.setText("%d" % (patient.phn))
            self.text_name.setText(patient.name)
            self.text_birth_date.setText(patient.birth_date)
            self.text_phone.setText(patient.phone)
            self.text_email.setText(patient.email)
            self.text_address.setText(patient.address)
        else:
            message = QMessageBox.warning(self, "Patient Not Found", "The patient you were searching for was not found in the system.")
            self.clear_button_clicked()
