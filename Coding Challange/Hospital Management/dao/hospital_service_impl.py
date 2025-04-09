from typing import List
from dao.ihospital_service import IHospitalService
from entity.appointment import Appointment
from util.db_connection import DBConnection
from myexceptions.hospital_exceptions import PatientNumberNotFoundException

class HospitalServiceImpl(IHospitalService):
    def get_appointment_by_id(self, appointment_id: int) -> Appointment:
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT appointmentId, patientId, doctorId, appointmentDate, description 
            FROM Appointment 
            WHERE appointmentId = ?
        """, (appointment_id,))
        
        row = cursor.fetchone()
        if row:
            return Appointment(
                appointment_id=row[0],
                patient_id=row[1],
                doctor_id=row[2],
                appointment_date=row[3],
                description=row[4]
            )
        return None

    def get_appointments_for_patient(self, patient_id: int) -> List[Appointment]:
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        
        # First check if patient exists
        cursor.execute("SELECT COUNT(*) FROM Patient WHERE patientId = ?", (patient_id,))
        if cursor.fetchone()[0] == 0:
            raise PatientNumberNotFoundException(patient_id)
        
        cursor.execute("""
            SELECT appointmentId, patientId, doctorId, appointmentDate, description 
            FROM Appointment 
            WHERE patientId = ?
        """, (patient_id,))
        
        appointments = []
        for row in cursor.fetchall():
            appointments.append(Appointment(
                appointment_id=row[0],
                patient_id=row[1],
                doctor_id=row[2],
                appointment_date=row[3],
                description=row[4]
            ))
        return appointments

    def get_appointments_for_doctor(self, doctor_id: int) -> List[Appointment]:
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT appointmentId, patientId, doctorId, appointmentDate, description 
            FROM Appointment 
            WHERE doctorId = ?
        """, (doctor_id,))
        
        appointments = []
        for row in cursor.fetchall():
            appointments.append(Appointment(
                appointment_id=row[0],
                patient_id=row[1],
                doctor_id=row[2],
                appointment_date=row[3],
                description=row[4]
            ))
        return appointments

    def schedule_appointment(self, appointment: Appointment) -> bool:
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Appointment (appointmentId, patientId, doctorId, appointmentDate, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                appointment.appointment_id,
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.description
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error scheduling appointment: {str(e)}")
            conn.rollback()
            return False

    def update_appointment(self, appointment: Appointment) -> bool:
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE Appointment 
                SET patientId = ?, doctorId = ?, appointmentDate = ?, description = ?
                WHERE appointmentId = ?
            """, (
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.description,
                appointment.appointment_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating appointment: {str(e)}")
            conn.rollback()
            return False

    def cancel_appointment(self, appointment_id: int) -> bool:
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Appointment WHERE appointmentId = ?", (appointment_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error canceling appointment: {str(e)}")
            conn.rollback()
            return False 