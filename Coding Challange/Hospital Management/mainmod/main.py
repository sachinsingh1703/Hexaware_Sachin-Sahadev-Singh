from dao.hospital_service_impl import HospitalServiceImpl
from entity.appointment import Appointment
from myexceptions.hospital_exceptions import PatientNumberNotFoundException
import datetime

def display_menu():
    print("\nHospital Management System")
    print("=" * 25)
    print("1. Get Appointment by ID")
    print("2. Get Appointments for Patient")
    print("3. Get Appointments for Doctor")
    print("4. Schedule New Appointment")
    print("5. Update Appointment")
    print("6. Cancel Appointment")
    print("0. Exit")
    return input("Enter your choice (0-6): ")

def get_date_input():
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD")

def main():
    hospital_service = HospitalServiceImpl()

    while True:
        choice = display_menu()
        
        try:
            if choice == "1":
                # Get Appointment by ID
                appointment_id = int(input("Enter Appointment ID: "))
                appointment = hospital_service.get_appointment_by_id(appointment_id)
                if appointment:
                    print(f"\nFound appointment: {appointment}")
                else:
                    print("\nAppointment not found")

            elif choice == "2":
                # Get Appointments for Patient
                patient_id = int(input("Enter Patient ID: "))
                try:
                    appointments = hospital_service.get_appointments_for_patient(patient_id)
                    if appointments:
                        print("\nPatient appointments:")
                        for apt in appointments:
                            print(f"- {apt}")
                    else:
                        print("\nNo appointments found for this patient")
                except PatientNumberNotFoundException as e:
                    print(f"\nError: {e}")

            elif choice == "3":
                # Get Appointments for Doctor
                doctor_id = int(input("Enter Doctor ID: "))
                appointments = hospital_service.get_appointments_for_doctor(doctor_id)
                if appointments:
                    print("\nDoctor appointments:")
                    for apt in appointments:
                        print(f"- {apt}")
                else:
                    print("\nNo appointments found for this doctor")

            elif choice == "4":
                # Schedule New Appointment
                print("\nSchedule New Appointment")
                appointment_id = int(input("Enter Appointment ID: "))
                patient_id = int(input("Enter Patient ID: "))
                doctor_id = int(input("Enter Doctor ID: "))
                appointment_date = get_date_input()
                description = input("Enter appointment description: ")

                new_appointment = Appointment(
                    appointment_id=appointment_id,
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    appointment_date=appointment_date,
                    description=description
                )

                if hospital_service.schedule_appointment(new_appointment):
                    print("\nAppointment scheduled successfully!")
                else:
                    print("\nFailed to schedule appointment")

            elif choice == "5":
                # Update Appointment
                print("\nUpdate Appointment")
                appointment_id = int(input("Enter Appointment ID to update: "))
                
                # First get the existing appointment
                existing_appointment = hospital_service.get_appointment_by_id(appointment_id)
                if not existing_appointment:
                    print("\nAppointment not found")
                    continue

                print("\nEnter new details (press Enter to keep existing value):")
                
                # Get new values, use existing ones if no input
                patient_id_str = input(f"Enter Patient ID [{existing_appointment.patient_id}]: ")
                patient_id = int(patient_id_str) if patient_id_str else existing_appointment.patient_id

                doctor_id_str = input(f"Enter Doctor ID [{existing_appointment.doctor_id}]: ")
                doctor_id = int(doctor_id_str) if doctor_id_str else existing_appointment.doctor_id

                date_str = input(f"Enter date [{existing_appointment.appointment_date}] (YYYY-MM-DD): ")
                appointment_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else existing_appointment.appointment_date

                description = input(f"Enter description [{existing_appointment.description}]: ")
                if not description:
                    description = existing_appointment.description

                updated_appointment = Appointment(
                    appointment_id=appointment_id,
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    appointment_date=appointment_date,
                    description=description
                )

                if hospital_service.update_appointment(updated_appointment):
                    print("\nAppointment updated successfully!")
                else:
                    print("\nFailed to update appointment")

            elif choice == "6":
                # Cancel Appointment
                appointment_id = int(input("Enter Appointment ID to cancel: "))
                if hospital_service.cancel_appointment(appointment_id):
                    print("\nAppointment cancelled successfully!")
                else:
                    print("\nFailed to cancel appointment")

            elif choice == "0":
                print("\nThank you for using Hospital Management System!")
                break

            else:
                print("\nInvalid choice! Please try again.")

        except ValueError as e:
            print(f"\nError: Please enter valid numeric values where required. ({str(e)})")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 