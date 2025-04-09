class Patient:
    def __init__(self, patient_id=None, first_name="", last_name="", date_of_birth="", gender="", contact_number="", address=""):
        self.__patient_id = patient_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__date_of_birth = date_of_birth
        self.__gender = gender
        self.__contact_number = contact_number
        self.__address = address

    # Getters
    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def gender(self):
        return self.__gender

    @property
    def contact_number(self):
        return self.__contact_number

    @property
    def address(self):
        return self.__address

    # Setters
    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @date_of_birth.setter
    def date_of_birth(self, value):
        self.__date_of_birth = value

    @gender.setter
    def gender(self, value):
        self.__gender = value

    @contact_number.setter
    def contact_number(self, value):
        self.__contact_number = value

    @address.setter
    def address(self, value):
        self.__address = value

    def __str__(self):
        return f"Patient(ID: {self.__patient_id}, Name: {self.__first_name} {self.__last_name}, " \
               f"DOB: {self.__date_of_birth}, Gender: {self.__gender}, " \
               f"Contact: {self.__contact_number}, Address: {self.__address})" 