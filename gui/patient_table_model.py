import sys
from PyQt6.QtCore import Qt, QAbstractTableModel

from clinic.controller import Controller
from clinic.patient import Patient

class PatientTableModel(QAbstractTableModel):
    
    # initalize the table fields
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = []
        self.refresh_data()

    # refreshes the table contents
    def refresh_data(self):
        self._data = []
        lo_patients = self.controller.list_patients()
        for patient in lo_patients:
            self._data.append([patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address])
        self.layoutChanged.emit()

    # filter the table with the given keyword
    def filter_patients(self, keyword):
        self._data = []
        retrieved_patients = self.controller.retrieve_patients(keyword)
        for patient in retrieved_patients:
            self._data.append([patient.phn, patient.name, patient.birth_date, patient.phone, patient.email, patient.address])
        self.layoutChanged.emit()

    # resets the data in the table
    def reset(self):
        self._data = []
        self.layoutChanged.emit()

    # setting the display of the table
    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, str):
                return "%s" % (value)
            else:
                return value
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
    # returns the row count
    def rowCount(self, index):
        return len(self._data)
    
    # returns the column count
    def columnCount(self, index):
        if self._data:
            return len(self._data[0])
        else:
            return 0
    
    # header data
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ["PHN", "Name", "Birthdate", "Phone", "Email", "Address"]
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return "%s" % headers[section]
        return super().headerData(section, orientation, role)
