CREATE DATABASE IF NOT EXISTS smartcare;
USE smartcare;

-- Create 'user' table
CREATE TABLE IF NOT EXISTS user (
  userID VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  role ENUM('nurse', 'patient', 'admin', 'doctor'),
  password VARCHAR(255)
);

-- Create 'nurse' table
CREATE TABLE IF NOT EXISTS nurse (
  userID VARCHAR(255),
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Create 'patient' table
CREATE TABLE IF NOT EXISTS patient (
  userID VARCHAR(255),
  address TEXT,
  dateOfBirth DATE,
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Create 'admin' table
CREATE TABLE IF NOT EXISTS admin (
  userID VARCHAR(255),
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Create 'doctor' table
CREATE TABLE IF NOT EXISTS doctor (
  userID VARCHAR(255),
  specialization TEXT,
  PRIMARY KEY (userID),
  FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Create 'security_log' table
CREATE TABLE IF NOT EXISTS security_log (
  logID INT AUTO_INCREMENT PRIMARY KEY,
  userID VARCHAR(255),
  timestamp DATETIME,
  action TEXT,
  FOREIGN KEY (userID) REFERENCES user(userID)
);

-- Create 'appointment' table
CREATE TABLE IF NOT EXISTS appointment (
  appointmentID INT AUTO_INCREMENT PRIMARY KEY,
  patientID VARCHAR(255),
  doctorID VARCHAR(255),
  appointmentTime DATETIME,
  status ENUM('scheduled', 'completed', 'cancelled'),
  FOREIGN KEY (patientID) REFERENCES patient(userID),
  FOREIGN KEY (doctorID) REFERENCES doctor(userID)
);

-- Create 'prescription' table
CREATE TABLE IF NOT EXISTS prescription (
  prescriptionID INT AUTO_INCREMENT PRIMARY KEY,
  appointmentID INT,
  description TEXT,
  FOREIGN KEY (appointmentID) REFERENCES appointment(appointmentID)
);

-- Create 'invoice' table
CREATE TABLE IF NOT EXISTS invoice (
  invoiceID INT AUTO_INCREMENT PRIMARY KEY,
  appointmentID INT,
  amount FLOAT,
  status ENUM('unpaid', 'paid'),
  FOREIGN KEY (appointmentID) REFERENCES appointment(appointmentID)
);
