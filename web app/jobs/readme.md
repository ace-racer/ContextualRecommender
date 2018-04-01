### This folder contains the scheduled jobs to update the models on a regular basis
#### Dependencies
1. Schedule - pip install schedule

#### How to execute the application

### Update the path to the database
1. Navigate to configurations.py file in this folder
2. Update the value in the variable *OPERATIONS_DATBASE_LOCATION* to the location where the database (.db) file is present in the database folder
3. Update the value of the variable *log_file_folder_location* to the location where the Log file for the scheduled jobs need to be created
4. Update the value of the variable *CONTENT_DATABASE_LOCATION* to the location where the database with the content is present

### Run the jobs 

1. python scheduler.py
2. Check the log file and the operations database to understand the progress of the jobs
