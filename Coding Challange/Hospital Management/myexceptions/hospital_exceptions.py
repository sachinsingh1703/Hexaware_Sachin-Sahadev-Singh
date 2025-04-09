class PatientNumberNotFoundException(Exception):
    """Exception raised when a patient number is not found in the database"""
    def __init__(self, patient_id: int, message: str = "Patient not found"):
        self.patient_id = patient_id
        self.message = f"{message} (ID: {patient_id})"
        super().__init__(self.message) 