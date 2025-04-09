# Hospital Management System

A Python-based hospital management system that handles patients, doctors, and appointments.

## Features

- Patient management
- Doctor management
- Appointment scheduling and management
- Database integration with SQL Server

## Prerequisites

1. Python 3.7 or higher
2. SQL Server
3. ODBC Driver 17 for SQL Server
4. A SQL Server database named 'Hospital_Management'

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the database connection in `config.ini` (will be created automatically on first run)

## Database Setup

Create the following tables in your SQL Server database:

```sql
USE Hospital_Management;

CREATE TABLE Patient (
    patientId INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    dateOfBirth DATE,
    gender VARCHAR(10),
    contactNumber VARCHAR(15),
    address VARCHAR(255)
);

CREATE TABLE Doctor (
    doctorId INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    specialization VARCHAR(100),
    contactNumber VARCHAR(15)
);

CREATE TABLE Appointment (
    appointmentId INT PRIMARY KEY,
    patientId INT,
    doctorId INT,
    appointmentDate DATE,
    description TEXT,
    FOREIGN KEY (patientId) REFERENCES Patient(patientId),
    FOREIGN KEY (doctorId) REFERENCES Doctor(doctorId)
);
```

## Usage

Run the application from the project root directory:
```
python run.py
```

## Project Structure

- `entity/` - Contains entity classes (Patient, Doctor, Appointment)
- `dao/` - Data Access Objects and service interfaces
- `util/` - Utility classes for database connection
- `myexceptions/` - Custom exception classes
- `mainmod/` - Main application module
- `run.py` - Application entry point 