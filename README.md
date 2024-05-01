# SmartCare Surgery Web-based System

## Introduction
SmartCare Surgery is a web-based application designed to replace the paper-based system at a GP business, facilitating interactions among doctors, nurses, patients, and administrators. It is developed by Toby Warn, Ben Phillips, and Filip Orczynski as part of their Distributed & Enterprise Software Development course. The system aims to streamline operations, manage patient information securely, and integrate with external services for enhanced functionality.

## Features
- Multiple user roles with secure login (Doctor, Nurse, Patient, Admin)
- Appointment booking via integrated calendar services
- Automatic address lookup through web services
- Invoice generation and management
- Periodic turnover calculations (daily, weekly, monthly)
- Advanced collaboration features for future expansions

## Prerequisites
- Docker
- MySQL
- Python 3.8+
- Django
- HTML/CSS

## Installation

1. Clone the repository:
   ```
   https://github.com/benphillips1997/DESD.git
   ```
2. Set django-web-app-entrypoint.sh to LF

3. Set up the Docker environment:
   ```
   docker-compose up --build
   ```

## Usage

1. Access the application through your web browser at `http://localhost:8000`.
2. Log in using one of the default user accounts.

## Default User Accounts

## Users

Superuser account:
    -userID: super1
    -email: superuser@smartcare.com
    -password: pw1

Admin account:
    -userID: admin1
    -email: admin@smartcare.com
    -password: pw1

Patient account:
    -userID: patient1
    -email: patient@smartcare.com
    -password: pw1

Doctor account - verified:
    -userID: DrFirst01
    -email: dr_first@smartcare.com
    -password: pw1

Nurse account - verified:
    -userID: MsBest01
    -email: ms_best@smartcare.com
    -password: pw1


## Unit Testing

Ensure all privileges to the test database:
   ```
   docker exec -it mysql_container mysql -u root -p
   GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%';
   FLUSH PRIVILEGES;
   ```

## Acknowledgments
- Thanks to Dilshan, Cameron & Mehmet for their guidance.
