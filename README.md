# SmartCare Surgery web based system

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