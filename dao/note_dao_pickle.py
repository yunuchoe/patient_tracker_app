from clinic.note import *
from clinic.dao.note_dao import *
import datetime
from pickle import dump, load

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn, autosave=False):
        self.notes = []
        self.autocounter = 0
        self.phn = phn
        self.autosave = autosave
        self.filename = "clinic/records/%d.dat" % (self.phn)

        # if autosave is True, try to open the file and load the collection
        if self.autosave:
            try:
                with open("clinic/records/%d.dat" % (self.phn), "rb") as f:
                    self.notes = load(f)
                    self.autocounter = self.notes[-1].code
            except:
                pass

    def search_note(self, key):
        """ return the note with the given key or None """
        for note in self.notes:
            if note.code == key:
                return note
        return None

    def create_note(self, text):
        """ create a note and add it to the collection """
        self.autocounter += 1
        cur_time = datetime.datetime.now()
        note = Note(self.autocounter, text, cur_time)
        self.notes.append(note)

        # if autosave is True, save the new collection in the file
        if self.autosave:
            with open(self.filename, "wb") as f:
                dump(self.notes, f)
        return note

    def retrieve_notes(self, search_string):
        """ return a list of notes that contain the given search string """
        retrieved_notes = []
        for note in self.notes:
            if search_string in note.text:
                retrieved_notes.append(note)
        return retrieved_notes

    def update_note(self, key, text):
        """ update a note in the collection """
        updated_note = None

        for note in self.notes:
            if note.code == key:
                updated_note = note
                break

        updated_note.text = text
        updated_note.timestamp = datetime.datetime.now()

        # if autosave is True, save the new collection in the file
        if self.autosave:
            with open(self.filename, "wb") as f:
                dump(self.notes, f)
        return True

    def delete_note(self, key):
        """ delete a note in the collection """
        note_to_delete_index = -1

        for i in range(len(self.notes)):
            if self.notes[i].code == key:
                note_to_delete_index = i
                break

        self.notes.pop(note_to_delete_index)

        # if autosave is Ture, save the new collection in the file
        if self.autosave:
            with open(self.filename, "wb") as f:
                dump(self.notes, f)
        return True

    def list_notes(self):
        """ return a list of all the notes """
        list_of_notes = []
        for note in self.notes:
            list_of_notes.append(note)
        list_of_notes.reverse()
        return list_of_notes


