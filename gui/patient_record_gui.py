import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QPlainTextEdit
from PyQt6.QtCore import Qt

from clinic.controller import Controller, IllegalOperationException
from clinic.patient_record import PatientRecord
from clinic.note import Note


class PatientRecordGUI(QMainWindow):
    def __init__(self, controller):
        # set up the patient record window
        super().__init__()
        self.controller = controller
        patient = self.controller.get_current_patient()
        self.setWindowTitle("%s's Record" % (patient.name))
        self.resize(800, 700)
        
        self.text_box = QPlainTextEdit()
        self.text_box.setReadOnly(True)

        refresh_button = QPushButton("Clear Search")
        refresh_button.clicked.connect(self.refresh_button_clicked)
        
        self.label_create = QLabel()
        self.label_create.setText("Text:")
        self.text_create = QLineEdit()
        self.text_create.setPlaceholderText("Enter the text of the note")
        self.text_create.textChanged.connect(self.text_create_changed)
        self.create_button = QPushButton("Create Note")
        self.create_button.clicked.connect(self.create_button_clicked)
        self.create_button.setEnabled(False)

        create_layout = QHBoxLayout()
        create_layout.addWidget(self.label_create)
        create_layout.addWidget(self.text_create)
        create_layout.addWidget(self.create_button)

        self.label_update_code = QLabel()
        self.label_update_code.setText("Code:")
        self.text_update_code = QLineEdit()
        self.text_update_code.setPlaceholderText("Enter the code here")
        self.text_update_code.setInputMask("00000000")
        self.text_update_code.textChanged.connect(self.text_update_changed)
        self.label_update_text = QLabel()
        self.label_update_text.setText("New Text:")
        self.text_update = QLineEdit()
        self.text_update.setPlaceholderText("Enter the new text here")
        self.text_update.textChanged.connect(self.text_update_changed)
        self.update_button = QPushButton("Update Note")
        self.update_button.clicked.connect(self.update_button_clicked)
        self.update_button.setEnabled(False)

        update_layout = QHBoxLayout()
        update_layout.addWidget(self.label_update_code)
        update_layout.addWidget(self.text_update_code)
        update_layout.addWidget(self.label_update_text)
        update_layout.addWidget(self.text_update)
        update_layout.addWidget(self.update_button)

        self.label_delete_code = QLabel()
        self.label_delete_code.setText("Code:")
        self.text_delete = QLineEdit()
        self.text_delete.setInputMask("00000000")
        self.text_delete.setPlaceholderText("Enter the code here")
        self.text_delete.textChanged.connect(self.text_delete_changed)
        self.delete_button = QPushButton("Delete Note")
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.delete_button.setEnabled(False)
        self.text_retrieve_notes = QLineEdit()
        self.text_retrieve_notes.setPlaceholderText("Enter the keyword in the notes to retrieve")
        self.text_retrieve_notes.textChanged.connect(self.text_retrieve_notes_changed)

        delete_layout = QHBoxLayout()
        delete_layout.addWidget(self.label_delete_code)
        delete_layout.addWidget(self.text_delete)
        delete_layout.addWidget(self.delete_button)

        self.label_retrieve = QLabel()
        self.label_retrieve.setText("Search:")

        retrieve_layout = QHBoxLayout()
        retrieve_layout.addWidget(self.label_retrieve)
        retrieve_layout.addWidget(self.text_retrieve_notes)

        create_widget = QWidget()
        create_widget.setLayout(create_layout)

        update_widget = QWidget()
        update_widget.setLayout(update_layout)

        delete_widget = QWidget()
        delete_widget.setLayout(delete_layout)

        retrieve_widget = QWidget()
        retrieve_widget.setLayout(retrieve_layout)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.text_box)
        layout1.addWidget(create_widget)
        layout1.addWidget(update_widget)
        layout1.addWidget(delete_widget)
        layout1.addWidget(retrieve_widget)
        layout1.addWidget(refresh_button)


        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        self.refresh_button_clicked()

    # clears the search text bar        
    def refresh_button_clicked(self):
        self.text_box.setPlainText("")
        lo_notes = self.controller.list_notes()
        for note in lo_notes:
            note_code = note.code
            note_text = note.text
            note_timestamp = note.timestamp

            self.text_box.appendPlainText("Code: %d, Note: %s, Time: %s" % (note_code, note_text, note_timestamp))

        self.text_retrieve_notes.setText("")

    # creates a new note with assigned code counting up from 1
    def create_button_clicked(self):
        text = self.text_create.text()
        self.controller.create_note(text)
        message = QMessageBox.warning(self, "Note Created!", "The note has been successfully added to the system.")
        self.text_create.setText("")
        self.refresh_button_clicked()

    # updates the note matching the given code
    def update_button_clicked(self):
        key = int(self.text_update_code.text())
        text = self.text_update.text()
        if self.controller.update_note(key, text):
            message = QMessageBox.information(self, "Update Success!", "Note %d has been successfully updated." % (key))
            self.text_update_code.setText("")
            self.text_update.setText("")
            self.refresh_button_clicked()
        else:
            message = QMessageBox.warning(self, "Invalid Operation", "A note with this code was not found in the system.")

    # checks if delete text bar has changed
    def text_delete_changed(self):
        if self.text_delete.text():
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)

    # checks if create text bar has changed
    def text_create_changed(self):
        if self.text_create.text():
            self.create_button.setEnabled(True)
        else:
            self.create_button.setEnabled(False)

    # checks if update text bar has changed
    def text_update_changed(self):
        if self.text_update.text() and self.text_update_code.text():
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    # deletes the note matching the given code
    def delete_button_clicked(self):
        key = int(self.text_delete.text())
        if self.controller.delete_note(key):
            message = QMessageBox.information(self, "Deletion Success!", "Note %d has been successfully deleted." % (key))
            self.text_delete.setText("")
            self.refresh_button_clicked()
        else:
            message = QMessageBox.warning(self, "Invalid Code", "A note with this code was not found in the system.")
            self.text_delete.setText("")

    # searchs for the notes with the matching key word
    def text_retrieve_notes_changed(self):
        text = self.text_retrieve_notes.text().rstrip()
        if text:
            self.clear_button_clicked()
            lo_notes = self.controller.retrieve_notes(text)
            for note in lo_notes:
                note_code = note.code
                note_text = note.text
                note_timestamp = note.timestamp

                self.text_box.appendPlainText("Code: %d, Note: %s, Time: %s" % (note_code, note_text, note_timestamp))
        else:
            self.refresh_button_clicked()
