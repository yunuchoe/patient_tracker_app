from clinic.patient import *
from clinic.note import *
from clinic.patient_record import *
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_dao_json import *
from clinic.dao.note_dao_pickle import *

import hashlib
from pickle import load, dump
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder
# from patient import *
# from note import *
# from patient_record import *

class Controller:
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.login_info = {}

        if not self.autosave:
            self.login_info = {"user": "123456", "ali": "@G00dPassw0rd"}
        else:
            with open("clinic/users.txt", "r") as file:
                for line in file:
                    line = line.rstrip()
                    line = line.split(",")
                    self.login_info[line[0]] = line[1]

        self.login_status = False
        self.cur_patient = None
        self.patient_dao_json = PatientDAOJSON(self.autosave)

    def get_password_hash(self, password):
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig


    def login(self, username: str, password: str) -> bool:
        """ Purpose: The user logins to the system.
                     The user must provide the correct username and password
                     and the user must not already be logged in.

            Parameters: username - the username as a string
                        password - the password as a string

            Returns: bool - the success or failure of the login
        """
        # check if the username exists in the collection
        if username in self.login_info:

            # check if autosave is on
            if not self.autosave:

                # check if the password is correct and if the user is not currently logged in
                if self.login_info[username] == password and not self.login_status:

                    # set the user login to True
                    self.login_status = True

                    # return True to indicate a successful login
                    return True

                elif self.login_info[username] != password:

                    # cannot log in with incorrect password
                    raise InvalidLoginException("Incorrect password. Please try again.")

                else:

                    # cannot log in when already logged in
                    raise DuplicateLoginException("You are already logged in")

            else:

                # set the user's password to a hashcode
                password_hash = self.get_password_hash(password)

                # check if the password is correct and the user is not already logged in
                if self.login_info[username] == password_hash and not self.login_status:

                    # set the user login to True
                    self.login_status = True

                    # return True to indicate a successful login
                    return True

                elif self.login_info[username] != password_hash:

                    # cannot log in with incorrect password
                    raise InvalidLoginException("Incorrect password. Please try again.")

                else:

                    # cannot log in when already logged in
                    raise DuplicateLoginException("You are already logged in")

        else:

            # the username is incorrect
            raise InvalidLoginException("Invalid username. Please try again.")

    def logout(self) -> bool:
        """ Purpose: The user logouts of the system.
                     The user must be logged in to logout.

            Parameters: None

            Returns: bool - the success or failure of the logout
        """

        # check if the user is logged in
        if self.login_status == True:

            # change the login status to false
            self.login_status = False

            # return True to indicate a successful logout
            return True

        else:

            # the user is not logged in
            # throw exception to indicate not logged in
            raise InvalidLogoutException("User is not logged in. Please log in to log out.")

    def search_patient(self, phn: int) -> Patient:
        """ Purpose: Searches through the patients collection to find a patient with the given patient health number.
	             User must be logged in to perform this action.

            Parameters: phn - the patient's health number

	    Returns: The patient instance if the patient was successfully found, otherwise None
        """
        # check if the user is logged in
        if self.login_status:

            # delegate the task to patient dao
            return self.patient_dao_json.search_patient(phn)

        else:

            # the user is not logged in
            raise IllegalAccessException("User is not logged in. Please log in to log out.")

    def create_patient(self, phn: int, name: str, birthdate: str, phone: str, email: str, address: str) -> Patient:
        """ Purpose: Create a patient and add it to the patients collection.
	             The patient must not already be in the collection and the user must be logged in.

	    Parameters: phn - the patient's health number
                        name - the patient's name
                        birthdate - the patient's birthdate
                        phone - the patient's phone number
                        email - the patient's email address
                        address - the patient's home address

            Returns - The patient instance if the patient was successfully added, otherwise None
	"""
	# check if the user is logged in
        if self.login_status:

            # check if the patient is in the collection
            if not self.search_patient(phn):

	        # create the patient instance and delegate task to patient dao
                patient = Patient(phn, name, birthdate, phone, email, address)
                return self.patient_dao_json.create_patient(patient)

            else:

                # cannot create patient whose phn already exists in the collection
                # throw illegal operation exception
                raise IllegalOperationException("This phn is already in use")

        # the user is not logged in
        # throw illegal access exception
        else:
            raise IllegalAccessException("User is not logged in")

    def retrieve_patients(self, name_to_retrieve: str) -> list[Patient]:
        """ Purpose: Find patients with the given name and add them to a list of patients.
                     The user must be logged in.

            Parameters: name_to_retrieve - the name of the patient(s) to retrieve

            Returns: The list of retrieved patients
        """
        # check if the user is logged in
        if self.login_status:

            # delegate the task to patient dao
            return self.patient_dao_json.retrieve_patients(name_to_retrieve)

        else:
            # the user is not logged in
            # throw illegal access exception
            raise IllegalAccessException("User is not logged in")

    def update_patient(self, target_phn: int, phn: int, name: str, birthdate: str, phone: str, email: str, address: str) -> bool:
        """ Purpose: Update the information for a patient.
                     The user must be logged in and the patient must not be set as the current patient.

            Parameters: target_phn - the phn of the patient to update
                        phn - the phn in the updated info
                        name - the patient's name in the updated info
                        birthdate - the patient's birthdate in the updated info
                        phone - the patient's phone number in the updated info
                        email - the patient's email in the updated info
                        address - the patient's address in the updated info

            Returns: bool - the success or failure of the deletion
        """
        # check if the user is logged in and the patient to update is not set as the current patient
        if self.login_status:

            # search the patient
            patient = self.search_patient(target_phn)

            # check if the patient exists in the collection
            if not patient:
                raise IllegalOperationException("Patient does not exist")

            # check if the patient to update is the cur patient
            if self.cur_patient and patient == self.cur_patient:
                raise IllegalOperationException("Cannot update current patient")

            if self.search_patient(target_phn):

                # check if the updated phn already exists
                if target_phn != phn and self.search_patient(phn):
                    raise IllegalOperationException("Updated phn already exists")

                else:

                    # update the patient
                    updated_patient = Patient(phn, name, birthdate, phone, email, address)

                    # delegate the task to patient dao
                    self.patient_dao_json.update_patient(target_phn, updated_patient)

                    # return True to indicate update success
                    return True
        else:
            # either the user is not logged in or the patient to update is set as the current patient
            # throw illegal access exception
             raise IllegalAccessException("User is not logged in")

    def delete_patient(self, phn: int) -> bool:
        """ Purpose: Delete a patient from the patients collection.
                     The user must be logged in and the patient must not be set as the current patient.

            Parameters: phn - the phn of the patient to delete

            Returns: bool - the success or failure of the deletion
        """
        # check if the user is logged in
        if self.login_status:

            # check if the patient to delete exists in the collection
            patient = self.search_patient(phn)

            if not patient:
                # patient does not exist
                raise IllegalOperationException("Patient does not exist")

            if self.cur_patient and patient == self.cur_patient:
                # the patient to delete is set as the current patient
                raise IllegalOperationException("Cannot delete current patient")

            # delegate the task to patient dao
            self.patient_dao_json.delete_patient(phn)

            # return True to indicate deletion success
            return True

        else:
            # either the user is not logged in or the patient to delete is set as the current patient
            # throw illegal access exception
            raise IllegalAccessException("User is not logged in")


    def list_patients(self) -> list[Patient]:
        """ Purpose: Append all patients in the collection to a list.
                     The user must be logged in.

            Parameters: None

            Returns: The list of patients in the collection
        """
        # check if the user is logged in
        if self.login_status:

            # delegate the task to patient dao
            return self.patient_dao_json.list_patients()

        else:

            # the user is not logged in
            raise IllegalAccessException("User is not logged in")

    def set_current_patient(self, phn: int) -> None:
        """ Purpose: The user sets a patient to be the current patient.

            Parameters: phn - the phn of the patient to set as the current patient

            Returns: None
        """
        # set the current patient's phn to the given phn
        if self.login_status:

            # check if the patient exists
            if self.search_patient(phn):

                # set the current patient
                self.cur_patient = self.search_patient(phn)

            else:
                # the patient does not exist
                raise IllegalOperationException("Not a valid phn")
        else:
            # the user is not logged in
            raise IllegalAccessException("User is not logged in")

    def unset_current_patient(self) -> None:
        """ Purpose: The user unsets the current patient.

            Parameters: None

            Returns: None
        """
        # set the current patient's phn to None
        if self.login_status:

            # set current patient to None
            self.cur_patient = None

        else:
            # the user is not logged in
            raise IllegalAccessException("User is not logged in")

    def get_current_patient(self) -> Patient:
        """ Purpose: Return the current patient.
                     The user must be logged in and the current patient must exist

            Parameters: None

            Returns: The patient that is set as the current patient, otherwise None
        """
        # check if the user is logged in
        if self.login_status:

            # return the current patient
            return self.cur_patient

        else:
            # the user is not logged in
             raise IllegalAccessException("User is not logged in")

    def create_note(self, message: str) -> Note:
        """ Purpose: Returns the created note for the selected patient with the inputted string

            Parameters: message - the message of the note in string format

            Returns: The created note, otherwise None
        """
        # check if the user is logged in
        if self.login_status:

            # check if a current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            # delegate the task to the patient class
            return self.cur_patient.create_note(message)

        else:
            # the user is not logged in
            raise IllegalAccessException("User is not logged in")

    def search_note(self, code: int) -> Note:
        """ Purpose: Searches for a patient note given the note's code

            Parameters: code - the code of the note

            Returns: The note to search for, otherwise None
        """
        # check if the user is logged in
        if self.login_status:

            # check if the current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            # delegate the task to the patient class
            return self.cur_patient.search_note(code)

        else:
            # the user is not logged in
            raise IllegalAccessException("Not logged in")

    def retrieve_notes(self, word: str) -> list[Note]:
        """ Purpose: Creates a list of all notes with the desired word under the current patient

            Parameters: word - word we want to search for and put in list

            Returns: A list of the notes with the key word
        """
        # check if the user is logged in
        if self.login_status:

            # check if the current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            # delegate the task to the patient class
            return self.cur_patient.retrieve_notes(word)

        else:
            # the user is not logged in
            raise IllegalAccessException("Not logged in")

    def update_note(self, code: int, new_sentence: str) -> bool:
        """ Purpose: Updates a note with a new sentence

            Parameters: new_sentence - the new message we want in note

            Returns: bool - true if successful, otherwise false
        """
        # check if the user is logged in
        if self.login_status:

            # check if the current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            # check if the note exists
            if self.search_note(code):

                # delegate the task to the patient class
                return self.cur_patient.update_note(code, new_sentence)

            else:
                # note does not exist
                return False

        else:
            # the user is not logged in
            raise IllegalAccessException("Not logged in")

    def delete_note(self, code: int) -> bool:
        """ Purpose: deletes a note from the current patient

            Parameters: int - the code of the note that we want removed

            Returns: bool - true if successful, otherwise false
        """
        # check if the user is logged in
        if self.login_status:

            # check if the current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            if self.search_note(code):

                # delegate the task to the patient class
                return self.cur_patient.delete_note(code)

            else:
                # note does not exist
                return None
        else:
            # the user is not logged in
            raise IllegalAccessException("Not logged in")

    def list_notes(self) -> list:
        """ Purpose: puts all notes in a list

            Parameters: none

            Returns: returns a list of all notes
        """
        # check if the user is logged in
        if self.login_status:

            # check if the current patient is set
            if not self.cur_patient:

                # no current patient is set
                raise NoCurrentPatientException("No current patient selected")

            # delegate the task to the patient class
            return self.cur_patient.list_notes()

        else:
            # the user is not logged in
            raise IllegalAccessException("Not logged in")


# main function for debugging
def main():
    # check if repr works
    patient = Patient(121212, 'hi', 'a', 'a', 'a', 'a')
    print(str(patient))

if __name__ == "__main__":
    main()

