class Doctor:
    def __init__(self, doctor_id=None, first_name="", last_name="", specialization="", contact_number=""):
        self.__doctor_id = doctor_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__specialization = specialization
        self.__contact_number = contact_number

    # Getters
    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def specialization(self):
        return self.__specialization

    @property
    def contact_number(self):
        return self.__contact_number

    # Setters
    @doctor_id.setter
    def doctor_id(self, value):
        self.__doctor_id = value

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @specialization.setter
    def specialization(self, value):
        self.__specialization = value

    @contact_number.setter
    def contact_number(self, value):
        self.__contact_number = value

    def __str__(self):
        return f"Doctor(ID: {self.__doctor_id}, Name: {self.__first_name} {self.__last_name}, " \
               f"Specialization: {self.__specialization}, Contact: {self.__contact_number})" 