import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton, QTableView, QWidget, QLabel, QLineEdit

class HelpGUI(QMainWindow):
    def __init__(self):
        #lists all of the app instructions
        super().__init__()

        label_search = QLabel()
        label_search.setText("Search Patient: Click on the 'Search' button on the toolbar to open a window to search a patient by PHN.")

        label_add_patient = QLabel()
        label_add_patient.setText("Add Patient: Click on the 'Add Patient' button on the bottom left of the patients table window to open a window for adding patients.")

        label_reset_table = QLabel()
        label_reset_table.setText("Reset Table: Click on the 'Reset' button on the bottom of the patients table to reset the table.")

        label_patient_table = QLabel()
        label_patient_table.setText("Patients Table: Click on the 'Patients Table' button to open a table of all of the patients in the system. This table is initially empty until patients have been added to the system.")

        label_patient_window = QLabel()
        label_patient_window.setText("Patient Window: Double click on a patient's information in the patients table to open a window to perform patient actions.")

        label_patient_actions = QLabel()
        label_patient_actions.setText("The patient actions are the following 3 actions:")

        label_update_patient = QLabel()
        label_update_patient.setText("- Update Patient: If no appointment was set with this patient, change the information in the patient window and click 'Update' to update the patient's information.")

        label_delete_patient = QLabel()
        label_delete_patient.setText("- Delete Patient: If no appointment was set with this patient, click 'Delete' to delete this patient from the system.")

        label_set_appointment = QLabel()
        label_set_appointment.setText("- Set Appointment: Click 'Set Appointment' to set an appointment with a patient. This enables viewing and editing of patient records. Click 'Unset Appointment' to finish the appointment.")

        label_patient_record_window = QLabel()
        label_patient_record_window.setText("Patient Record Window: After setting an appointment with the patient, click 'Patient Record' to open a window to view patient records and perform patient record actions.")

        label_patient_record_actions = QLabel()
        label_patient_record_actions.setText("The patient record actions are the following 3 actions:")

        label_create_note = QLabel()
        label_create_note.setText("- Create Note: Enter the text of the note and click 'Create' to create a note.")

        label_update_note = QLabel()
        label_update_note.setText("- Update Note: Enter the code of the note and the new text, then click 'Update' to update the note.")

        label_delete_note = QLabel()
        label_delete_note.setText("- Delete Note: Enter the code of the note and click 'Delete' to delete the note.")

        label_retrieve_patients = QLabel()
        label_retrieve_patients.setText("Retrieve Patients: Use the provided filter text bar on the bottom right of the patients table to filter the patients table by name.")

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label_search)
        layout.addWidget(label_patient_table)
        layout.addWidget(label_add_patient)
        layout.addWidget(label_reset_table)
        layout.addWidget(label_retrieve_patients)
        layout.addWidget(label_patient_window)
        layout.addWidget(label_patient_actions)
        layout.addWidget(label_update_patient)
        layout.addWidget(label_delete_patient)
        layout.addWidget(label_set_appointment)
        layout.addWidget(label_patient_record_window)
        layout.addWidget(label_patient_record_actions)
        layout.addWidget(label_create_note)
        layout.addWidget(label_update_note)
        layout.addWidget(label_delete_note)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def close_button_clicked(self):
        self.close()
