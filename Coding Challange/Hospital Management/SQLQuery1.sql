use Hospital_Management;

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

INSERT INTO Patient (patientId, firstName, lastName, dateOfBirth, gender, contactNumber, address)
VALUES 
(1, 'Rahul', 'Sharma', '1990-05-15', 'Male', '9876543210', '123 MG Road, Delhi'),
(2, 'Priya', 'Verma', '1985-09-20', 'Female', '9876501234', '45 Park Street, Mumbai');


INSERT INTO Doctor (doctorId, firstName, lastName, specialization, contactNumber)
VALUES 
(1, 'Dr. Anjali', 'Mehra', 'Cardiologist', '9876001122'),
(2, 'Dr. Vikram', 'Sinha', 'Orthopedic', '9876012345');


INSERT INTO Appointment (appointmentId, patientId, doctorId, appointmentDate, description)
VALUES 
(1, 1, 1, '2025-04-10', 'Routine heart check-up'),
(2, 2, 2, '2025-04-11', 'Knee pain consultation');


INSERT INTO Patient (patientId, firstName, lastName, dateOfBirth, gender, contactNumber, address)
VALUES 
(3, 'Amit', 'Kapoor', '1978-12-02', 'Male', '9812345678', '12 Civil Lines, Lucknow'),
(4, 'Sneha', 'Rao', '1992-07-10', 'Female', '9823456789', '89 MG Road, Bangalore'),
(5, 'Karan', 'Joshi', '2000-03-25', 'Male', '9834567890', '55 Nehru Street, Chennai'),
(6, 'Meena', 'Iyer', '1988-11-18', 'Female', '9845678901', '203 Jubilee Hills, Hyderabad');


INSERT INTO Doctor (doctorId, firstName, lastName, specialization, contactNumber)
VALUES 
(3, 'Dr. Raj', 'Patel', 'Dermatologist', '9876023456'),
(4, 'Dr. Neha', 'Khan', 'Pediatrician', '9876034567'),
(5, 'Dr. Sameer', 'Reddy', 'Neurologist', '9876045678');


INSERT INTO Appointment (appointmentId, patientId, doctorId, appointmentDate, description)
VALUES 
(3, 3, 3, '2025-04-12', 'Skin allergy treatment'),
(4, 4, 4, '2025-04-13', 'Child vaccination follow-up'),
(5, 5, 5, '2025-04-14', 'Headache and dizziness check-up'),
(6, 6, 1, '2025-04-15', 'Heart palpitations'),
(7, 1, 2, '2025-04-16', 'Back pain evaluation'),
(8, 2, 3, '2025-04-17', 'Rash on hands and legs');

