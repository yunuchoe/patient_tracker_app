import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton, QTableView, QWidget, QLabel, QLineEdit

from clinic.controller import Controller
from clinic.patient import Patient
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.list_patient_gui import ListPatientGUI
from clinic.gui.add_patient_gui import AddPatientGUI

class PatientTableGUI(QMainWindow):
    def __init__(self, controller):
        # set upt the patient table window
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Patients")
        self.resize(900, 400)

        self.add_patient_gui = AddPatientGUI(self.controller, self)
        self.list_patient_gui = ListPatientGUI(self.controller, self)

        add_button = QPushButton("Add Patient")
        add_button.clicked.connect(self.add_button_clicked)

        self.patient_table = QTableView()

        self.patient_model = PatientTableModel(self.controller)
        self.patient_table.setModel(self.patient_model)

        self.current_patient_phn = None
        self.patient_table.doubleClicked.connect(self.list_patient_requested)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_button_clicked)
        self.text_filter = QLineEdit()
        self.text_filter.setPlaceholderText("Enter the name of the patients to retrieve")
        self.text_filter.textChanged.connect(self.filter_text_changed)
        # self.retrieve_button = QPushButton("Retrieve Patients")
        # self.retrieve_button.clicked.connect(self.retrieve_button_clicked)

        layout1 = QHBoxLayout()
        layout1.addWidget(add_button)
        layout1.addWidget(reset_button)
        layout1.addWidget(self.text_filter)
        # layout1.addWidget(self.retrieve_button)

        bottom_widget = QWidget()
        bottom_widget.setLayout(layout1)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.patient_table)
        layout2.addWidget(bottom_widget)
        
        widget = QWidget()
        widget.setLayout(layout2)
        self.setCentralWidget(widget)
        self.refresh_table()


    # opens a new window to add patients
    def add_button_clicked(self):
        self.add_patient_gui.show()

    # resets table
    def reset_button_clicked(self):
        self.patient_model.refresh_data()
        self.text_filter.setText("")
        self.patient_table.setColumnWidth(5, 200)
        self.patient_table.setColumnWidth(4, 200)
        self.patient_table.setColumnWidth(3, 140)
        self.patient_table.setColumnWidth(1, 100)
        self.patient_table.setColumnWidth(0, 100)
        self.patient_table.setEnabled(True)

    # refreshes table
    def refresh_table(self):
        self.patient_model.refresh_data()
        self.patient_table.setColumnWidth(5, 200)
        self.patient_table.setColumnWidth(4, 200)
        self.patient_table.setColumnWidth(3, 140)
        self.patient_table.setColumnWidth(1, 100)
        self.patient_table.setColumnWidth(0, 100)
        self.patient_table.setEnabled(True)

    # opens a new window to show the list of patients
    def list_patient_requested(self):
        index = self.patient_table.selectionModel().currentIndex()
        self.current_patient_phn = int(index.sibling(index.row(), 0).data())

        self.list_patient_gui.list_patient(self.current_patient_phn)
        self.list_patient_gui.show()

    # checks if the filter text bar has been changed
    def filter_text_changed(self):
        if self.text_filter.text().rstrip():
            keyword = self.text_filter.text().rstrip()
            self.patient_model.filter_patients(keyword)
            self.patient_table.setColumnWidth(5, 200)
            self.patient_table.setColumnWidth(4, 200)
            self.patient_table.setColumnWidth(3, 140)
            self.patient_table.setColumnWidth(1, 100)
            self.patient_table.setColumnWidth(0, 100)
            self.patient_table.setEnabled(True)
        else:
            self.refresh_table()

    # closes the window
    def closeEvent(self, event):
        self.list_patient_gui.close()
        self.close()
