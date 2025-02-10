import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException
from clinic.gui.patient_record_gui import PatientRecordGUI

class ListPatientGUI(QMainWindow):
    def __init__(self, controller, parent):
        # set up list of patients window
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.patient_record_gui = None
        self.setWindowTitle("")
        self.phn = 0
        self.name = ""
        self.birth_date = ""
        self.phone = ""
        self.email = ""
        self.address = ""

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

        self.button_update = QPushButton("Update")
        self.button_delete = QPushButton("Delete")
        self.button_set = QPushButton("Set Appointment")
        self.button_unset = QPushButton("Unset Appointment")
        self.button_close = QPushButton("Close")
        self.button_patient_record = QPushButton("Patient Record")
        layout2.addWidget(self.button_update)
        layout2.addWidget(self.button_delete)
        layout2.addWidget(self.button_set)
        layout2.addWidget(self.button_unset)
        layout2.addWidget(self.button_patient_record)
        layout2.addWidget(self.button_close)

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

        self.text_phn.textChanged.connect(self.patient_text_changed)
        self.text_name.textChanged.connect(self.patient_text_changed)
        self.text_birth_date.textChanged.connect(self.patient_text_changed)
        self.text_phone.textChanged.connect(self.patient_text_changed)
        self.text_email.textChanged.connect(self.patient_text_changed)
        self.text_address.textChanged.connect(self.patient_text_changed)

        self.text_phn.setEnabled(True)
        self.text_name.setEnabled(True)
        self.text_birth_date.setEnabled(True)
        self.text_phone.setEnabled(True)
        self.text_email.setEnabled(True)
        self.text_address.setEnabled(True)

        self.button_update.setEnabled(False)
        self.button_delete.setEnabled(True)
        self.button_set.setEnabled(True)
        self.button_unset.setEnabled(False)

        self.button_update.clicked.connect(self.update_button_clicked)
        self.button_delete.clicked.connect(self.delete_button_clicked)
        self.button_close.clicked.connect(self.close_button_clicked)
        self.button_set.clicked.connect(self.set_button_clicked)
        self.button_unset.clicked.connect(self.unset_button_clicked)
        self.button_patient_record.clicked.connect(self.patient_record_button_clicked)

    def list_patient(self, key):
        """ Search and list a patient """
        patient = self.controller.search_patient(key)
        self.setWindowTitle("%s" % (patient.name))
        cur_patient = self.controller.get_current_patient()
        self.phn = patient.phn
        self.name = patient.name
        self.birth_date = patient.birth_date
        self.phone = patient.phone
        self.email = patient.email
        self.address = patient.address
        
        # checks current patient 
        if cur_patient and cur_patient == patient:
            self.text_phn.setText(str(self.phn))
            self.text_name.setText(self.name)
            self.text_birth_date.setText(self.birth_date)
            self.text_phone.setText(self.phone)
            self.text_email.setText(self.email)
            self.text_address.setText(self.address)
            self.text_phn.setEnabled(False)
            self.text_name.setEnabled(False)
            self.text_birth_date.setEnabled(False)
            self.text_phone.setEnabled(False)
            self.text_email.setEnabled(False)
            self.text_address.setEnabled(False)
            self.button_update.setEnabled(False)
            self.button_delete.setEnabled(False)
            self.button_unset.setEnabled(True)
            self.button_set.setEnabled(False)
            self.button_patient_record.setEnabled(True)
            self.patient_record_gui = PatientRecordGUI(self.controller)
        else:
            self.text_phn.setText("%d" % (patient.phn))
            self.text_name.setText(patient.name)
            self.text_birth_date.setText(patient.birth_date)
            self.text_phone.setText(patient.phone)
            self.text_email.setText(patient.email)
            self.text_address.setText(patient.address)
            self.text_phn.setEnabled(True)
            self.text_name.setEnabled(True)
            self.text_birth_date.setEnabled(True)
            self.text_phone.setEnabled(True)
            self.text_email.setEnabled(True)
            self.text_address.setEnabled(True)
            self.button_delete.setEnabled(True)
            self.button_unset.setEnabled(False)
            self.button_set.setEnabled(True)
            self.button_patient_record.setEnabled(False)
            self.patient_record_gui = None

    # checks if the text fields changed in order for an update to occur
    def patient_text_changed(self):
        if self.text_phn.text() and self.text_name.text() and self.text_birth_date.text() \
            and self.text_phone.text() and self.text_email.text() and self.text_address.text() \
            and (int(self.text_phn.text()) != self.phn or self.text_name.text() != self.name \
            or self.text_phone.text() != self.phone or self.text_email.text() != self.email \
            or self.text_address.text() != self.address):
            self.button_update.setEnabled(True)
        else:
            self.button_update.setEnabled(False)

    # updates patient information with inputted info
    def update_button_clicked(self):
        try:
            phn = int(self.text_phn.text())
            name = self.text_name.text()
            birth_date = self.text_birth_date.text()
            phone = self.text_phone.text()
            email = self.text_email.text()
            address = self.text_address.text()
            self.controller.update_patient(self.phn, phn, name, birth_date, phone, email, address)
            self.parent.refresh_table()
            if self.phn != phn:
                self.phn = phn
            message = QMessageBox.information(self, "Update Success!", "This patient's information has successfully been updated.")
            
            self.name = name
            self.birth_date = birth_date
            self.phone = phone
            self.email = email
            self.address = address

            self.setWindowTitle("%s" % (self.name))
            
            self.button_update.setEnabled(False)

        except ValueError:
            message = QMessageBox.warning(self, "Update Failure!", "Please enter a valid numerical patient health number.")
        except IllegalOperationException:
            message = QMessageBox.warning(self, "Update Failure!", "A patient with this PHN already exists in the system.")

    # deletes the patient
    def delete_button_clicked(self):
        try:
            self.controller.delete_patient(self.phn)
            self.parent.refresh_table()
            message = QMessageBox.information(self, "Deletion Success!", "This patient has successfully been deleted from the system.")
            self.close_button_clicked()
        except IllegalOperationException:
            message = QMessageBox.warning(self, "Deletion Failure", "Please end the appointment with this patient before deleting.")

    # closes this window
    def close_button_clicked(self):
        self.text_phn.setText("")
        self.text_name.setText("")
        self.text_birth_date.setText("")
        self.text_phone.setText("")
        self.text_email.setText("")
        self.text_address.setText("")
        if self.patient_record_gui:
            self.patient_record_gui.hide()
        self.hide()
        
    # sets current patient
    def set_button_clicked(self):
        self.controller.set_current_patient(self.phn)
        self.text_phn.setText(str(self.phn))
        self.text_name.setText(self.name)
        self.text_birth_date.setText(self.birth_date)
        self.text_phone.setText(self.phone)
        self.text_email.setText(self.email)
        self.text_address.setText(self.address)
        self.text_phn.setEnabled(False)
        self.text_name.setEnabled(False)
        self.text_birth_date.setEnabled(False)
        self.text_phone.setEnabled(False)
        self.text_email.setEnabled(False)
        self.text_address.setEnabled(False)
        self.button_update.setEnabled(False)
        self.button_delete.setEnabled(False)
        self.button_unset.setEnabled(True)
        self.button_set.setEnabled(False)
        self.button_patient_record.setEnabled(True)
        self.patient_record_gui = PatientRecordGUI(self.controller)
    
    # unsets current patient - only avaliable if set
    def unset_button_clicked(self):
        self.controller.unset_current_patient()
        self.text_phn.setEnabled(True)
        self.text_name.setEnabled(True)
        self.text_birth_date.setEnabled(True)
        self.text_phone.setEnabled(True)
        self.text_email.setEnabled(True)
        self.text_address.setEnabled(True)
        self.button_delete.setEnabled(True)
        self.button_unset.setEnabled(False)
        self.button_set.setEnabled(True)
        self.button_patient_record.setEnabled(False)
        self.patient_record_gui = None

    # opens patient record in a new window
    def patient_record_button_clicked(self):
        self.patient_record_gui.show()

    # closes the window
    def closeEvent(self, event):
        if self.patient_record_gui:
            self.patient_record_gui.close()
        self.close_button_clicked()    
