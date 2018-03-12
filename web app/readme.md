#### Dependencies
1. Flask - pip install flask



#### How to execute the application

### Set up the data base and load the data - Note this DB needs to be dropped on completion of the project
1. Install SQLite and add it to path. Please follow this: https://www.tutorialspoint.com/sqlite/sqlite_installation.htm
2. Run the below set of commands to import data from CSV to a .db file for SQLite 3

Navigate to the folder with the data CSVs and then type the below one by one in a sqlite3 prompt
   1. .mode csv
   2. .open <db_name>.db
   3. .import <<file>>.csv <<db_name>>
   4. .schema <<file>>

### Run the service 

1. python /path_to_app.py_in_service_folder/app.py
2. Navigate to the URL in your browser that is shown in the console when executing 1

### Service endpoints

1. Get views by user id: 
   GET /views/<userid> 
   
   E.g. http://127.0.0.1:5000/views/1007

2. Add new view of user: 
   
   POST /views/add  
   Request header: Content-Type:application/json  
   Request body:  
   
   ```json
   {
	"userid":"1007",
	"streamid":"561",
	"moduleid":"491",
	"cardid":"8889"
   }
   ```
   
   E.g. http://127.0.0.1:5000/views/add  
     
   Note: A text response is sent which can be checked for errors. A text of "OK" is sent for success, else an error text is returned.