class Appointment:
    def __init__(self, appointment_id=None, patient_id=None, doctor_id=None, appointment_date="", description=""):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__appointment_date = appointment_date
        self.__description = description

    # Getters
    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def appointment_date(self):
        return self.__appointment_date

    @property
    def description(self):
        return self.__description

    # Setters
    @appointment_id.setter
    def appointment_id(self, value):
        self.__appointment_id = value

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @appointment_date.setter
    def appointment_date(self, value):
        self.__appointment_date = value

    @description.setter
    def description(self, value):
        self.__description = value

    def __str__(self):
        return f"Appointment(ID: {self.__appointment_id}, Patient ID: {self.__patient_id}, " \
               f"Doctor ID: {self.__doctor_id}, Date: {self.__appointment_date}, " \
               f"Description: {self.__description})" 