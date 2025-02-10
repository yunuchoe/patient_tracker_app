from clinic.note import *
from clinic.dao.note_dao_pickle import *

class PatientRecord:
    def __init__(self, phn, autosave=False):
        self.phn = phn
        self.autosave = autosave
        self.note_dao_pickle = NoteDAOPickle(phn, autosave)

    def create_note(self, message: str) -> Note:
        # delegate the task to the note dao
        return self.note_dao_pickle.create_note(message)

    def search_note(self, code: int) -> Note:
        return self.note_dao_pickle.search_note(code)

    def retrieve_notes(self, word: str) -> list[Note]:
        return self.note_dao_pickle.retrieve_notes(word)

    def update_note(self, code: int, new_sentence: str):
        return self.note_dao_pickle.update_note(code, new_sentence)

    def delete_note(self, code: str) -> bool:
        return self.note_dao_pickle.delete_note(code)

    def list_notes(self) -> list:
        return self.note_dao_pickle.list_notes()

    def __str__(self):
        patient_record_str = ""
        for code in self.notes:
            if code == self.autocounter - 1:
                patient_record_str += "Patient Record Code: %d, Patient Record Text: %s" % (code, self.notes[code].text)
            else:
                patient_record_str += "Patient Record Code: %d, Patient Record Text: %s\n" % (code, self.notes[code].text)
        return patient_record_str

    def __repr__(self):
        return "PatientRecord(%r, %r)" % (self.autocounter, self.notes)

    def __eq__(self, other):
        return self.autocounter == other.autocounter and self.notes == other.notes


