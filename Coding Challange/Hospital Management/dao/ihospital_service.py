from abc import ABC, abstractmethod
from typing import List
from entity.appointment import Appointment

class IHospitalService(ABC):
    @abstractmethod
    def get_appointment_by_id(self, appointment_id: int) -> Appointment:
        """Get appointment by ID"""
        pass

    @abstractmethod
    def get_appointments_for_patient(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        pass

    @abstractmethod
    def get_appointments_for_doctor(self, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a doctor"""
        pass

    @abstractmethod
    def schedule_appointment(self, appointment: Appointment) -> bool:
        """Schedule a new appointment"""
        pass

    @abstractmethod
    def update_appointment(self, appointment: Appointment) -> bool:
        """Update an existing appointment"""
        pass

    @abstractmethod
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment"""
        pass 