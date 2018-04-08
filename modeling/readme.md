### Recommender system models

#### Dependencies:
1. Surprise library: http://surpriselib.com/
   Install using Anaconda in windows systems:
   ```conda install -c conda-forge scikit-surprise```
   Details for other OS in the same link as above.

#### How to run
1. Update the values of the below parameters in the configurations.py file:
    1. STREAM_DETAILS_FILE_LOCATION - contains the stream details - stream, tag, cards info
	2. STREAM_VIEWS_FILE_LOCATION - contains the stream view information with the timestamps
	3. OUTPUT_FILES_DIRECTORY - where all the generated files will be stored - the files follow a sequential numbering scheme

2. Keep the operational parameters as all True so all files are generated

3. Execute client.py as below
    ```python client.py ```