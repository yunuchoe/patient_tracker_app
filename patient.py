from clinic.note import *
from clinic.patient_record import *

class Patient():
    def __init__(self, phn: int, name: str, birthdate: str, phone: str, email: str, address: str, autosave=False):
        self.phn = phn
        self.name = name
        self.birth_date = birthdate
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave
        self.patientrecord = PatientRecord(self.phn, autosave)

    def __repr__(self):
        return "Patient(%r, %r, %r, %r, %r, %r)" % (self.phn, self.name, self.birth_date, self.phone, self.email, self.address)

    def __eq__(self, other):
        return self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date \
               and self.phone == other.phone and self.email == other.email and self.address == other.address

    def __str__(self):
        return "Patient Health Number: %d, Name: %s, Birthdate: %s, Phone Number: %s, Email: %s, Address: %s" % \
               (self.phn, self.name, self.birthdate, self.phone, self.email, self.address)

    def create_note(self, message: str) -> Note:
        # delegate task to patient record
        return self.patientrecord.create_note(message)

    def search_note(self, code: str) -> Note:
        # delegate task to patient record
        return self.patientrecord.search_note(code)

    def retrieve_notes(self, word: str) -> list[Note]:
        # delegate task to patient record
        return self.patientrecord.retrieve_notes(word)

    def update_note(self, code: int, new_sentence: str) -> bool:
        # delegate task to patient record
        return self.patientrecord.update_note(code, new_sentence)

    def delete_note(self, code: str) -> bool:
        # delegate task to patient record
        return self.patientrecord.delete_note(code)

    def list_notes(self) -> list:
        # delegate task to patient record
        return self.patientrecord.list_notes()
