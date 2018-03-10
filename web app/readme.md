#### Dependencies
1. Flask - pip install flask



#### How to execute the application

### Set up the data base and load the data - Note this DB needs to be dropped on completion of the project
1. Install SQLite and add it to path. Please follow this: https://www.tutorialspoint.com/sqlite/sqlite_installation.htm
2. Run the below set of commands to import data from CSV to a .db file for SQLite 3

Navigate to the folder with the data CSVs and then type the below one by one in a sqlite3 prompt
a. .mode csv
b. .open <db_name>.db
c. .import <file>.csv <file>
d. .schema <file>

### Run the service 

1. python /path_to_app.py_in_service_folder/app.py
2. Navigate to the URL in your browser that is shown in the console when executing 1