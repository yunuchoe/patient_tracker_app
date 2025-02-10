from clinic.patient import *
from clinic.dao.patient_dao import *
import json
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.patients = {}

        # check autosave
        if self.autosave:

            # try to open file and load objects
            try:
                with open("clinic/patients.json", "r") as f:
                    for line in f:
                        patient = json.loads(line, cls=PatientDecoder)
                        self.patients[patient.phn] = patient
            except:
                pass

    def search_patient(self, key):
        """ returns the patient with the key or None """
        return self.patients.get(key)

    def create_patient(self, patient):
        """ create a patient and add the patient to the collection """
        self.patients[patient.phn] = patient

        # if autosave is True, then save the patient in the file
        if self.autosave:
            with open("clinic/patients.json", "a") as f:
                res = json.dumps(patient, cls=PatientEncoder)
                f.write(res + "\n")
        return patient

    def retrieve_patients(self, search_string):
        """ retrieve a list of patients with the given search string in their name """
        retrieved_patients = []
        for phn in self.patients:
            if search_string in self.patients[phn].name:
                retrieved_patients.append(self.patients[phn])
        return retrieved_patients

    def update_patient(self, key, patient):
        """ update a patient's information """
        if key == patient.phn:
            self.patients[key] = patient
        else:
            self.patients.pop(key)
            self.patients[patient.phn] = patient

        # if autosave is True, then save the patient's updated info in the file
        if self.autosave:
            with open("clinic/patients.json", "w") as f:
                for cur_patient in self.patients:
                    res = json.dumps(self.patients[cur_patient], cls=PatientEncoder)
                    f.write(res + "\n")

    def delete_patient(self, key):
        """ delete the patient with the given key """
        self.patients.pop(key)

        # if autosave is True, then remove the patient from the file
        if self.autosave:
            with open("clinic/patients.json", "w") as f:
                for cur_patient in self.patients:
                    res = json.dumps(self.patients[cur_patient], cls=PatientEncoder)
                    f.write(res + "\n")

    def list_patients(self):
        """ return a list of all the patients in the collection """
        list_of_patients = []
        for phn in self.patients:
            list_of_patients.append(self.patients[phn])
        return list_of_patients


