# SmartCare Surgery web based system

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
    -userID: doctor1
    -email: doctor@smartcare.com
    -password: pw1

Doctor account - unverified:
    -userID: doctor2
    -email: doctor2@smartcare.com
    -password: pw1

Nurse account - verified:
    -userID: nurse1
    -email: nurse@smartcare.com
    -password: pw1

Nurse account - unverified:
    -userID: nurse2
    -email: nurse2@smartcare.com
    -password: pw1


## Unit testing

To be able to run unit tests you must first grant privileges to the test database.
You can do this by entering the MYSQL shell as the root user
```
mysql -u root -p
```
and enter your password.


Then grant all privileges
```
GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%';
```