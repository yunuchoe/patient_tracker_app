import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QAction

from clinic.controller import Controller
from clinic.gui.help_gui import HelpGUI
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.patient_table_gui import PatientTableGUI

class ClinicHomeGUI(QMainWindow):
    def __init__(self, controller, parent):
        # setting up main menu
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Clinic")

        self.help_gui = HelpGUI()
        self.search_patient_gui = SearchPatientGUI(self.controller)
        self.patient_table_gui = PatientTableGUI(self.controller)

        home_layout = QGridLayout()
        home_label = QLabel("Welcome to the clinic. Please navigate using the toolbar.")
        home_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_layout.addWidget(home_label)
        self.home_widget = QWidget()
        self.home_widget.setLayout(home_layout)

        self.toolbar = QToolBar("Clinic Toolbar")
        logout_button_action = QAction("Logout", self)
        logout_button_action.setStatusTip("Log out of the system")
        logout_button_action.triggered.connect(self.logout_button_clicked)
        help_button_action = QAction("Help", self)
        help_button_action.setStatusTip("Open instructions for using interface")
        help_button_action.triggered.connect(self.help_button_clicked)
        search_button_action = QAction("Search", self)
        search_button_action.setStatusTip("Search a patient")
        search_button_action.triggered.connect(self.search_button_clicked)
        patient_table_button_action = QAction("Patients Table", self)
        patient_table_button_action.setStatusTip("Open a table of the patients in the system to perform update and delete actions.")
        patient_table_button_action.triggered.connect(self.patient_table_button_clicked)
        self.toolbar.addAction(logout_button_action)
        self.toolbar.addAction(help_button_action)
        self.toolbar.addAction(search_button_action)
        self.toolbar.addAction(patient_table_button_action)

        self.setStatusBar(QStatusBar(self))
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.home_widget)

    # tab for logout
    def logout_button_clicked(self):
        logout_dlg = QMessageBox(self)
        logout_dlg.setWindowTitle("Logout Confirmation")
        logout_dlg.setText("Are you sure you want to log out?")
        logout_dlg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No)
        button = logout_dlg.exec()

        # logout if desired
        if button == QMessageBox.StandardButton.Ok:
            self.controller.logout()
            for window in QApplication.topLevelWidgets():
                window.close()
            self.parent.show()
            self.close()
        # do nothing
        else:
            pass
    # open help window
    def help_button_clicked(self):
        self.help_gui.show()

    # open search window
    def search_button_clicked(self):
        self.search_patient_gui.show()

    # open table of patients
    def patient_table_button_clicked(self):
        self.patient_table_gui.show()

    #closes all windows - exit program
    def closeEvent(self, event):
        self.help_gui.close()
        self.search_patient_gui.close()
        self.patient_table_gui.close()
        self.close()
