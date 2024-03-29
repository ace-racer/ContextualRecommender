### Tag generation and recommender system modeling

#### Dependencies:
1. Surprise library: http://surpriselib.com/
   Install using Anaconda in windows systems:
   ```conda install -c conda-forge scikit-surprise```
   Details for other OS in the same link as above.
2. NLTK : https://www.nltk.org/install.html
3. Download NLTK supporting files by following the instructions [here](https://www.nltk.org/data.html) 
4. Generate Wordcloud: `pip install wordcloud`

#### How to run
1. Update the values of the below parameters in the configurations.py file:
    1. STREAM_DETAILS_FILE_LOCATION - contains the stream details - stream, tag, cards info
	2. STREAM_VIEWS_FILE_LOCATION - contains the stream view information with the timestamps
	3. STREAM_TAG_MAPPING_FILE_LOCATION - contains the stream tag mappings
	4. OUTPUT_FILES_DIRECTORY - where all the generated files will be stored - the files follow a sequential numbering scheme
	5. log_file_folder_location - where the log files will be generated
	6. CHOSEN_COLLABORATIVE_ALGORITHM - the algorithm to use to perform the collaborative filtering - values from knn_algo_wrapper, svd_algo_wrapper and svdpp_algo_wrapper. 
	   The best parameters as defined in model_params.py for the algorithm will be used to generate the ratings for the test data set.
    7. COMPLETE_STREAM_DETAILS_LOCATION - contains the complete stream details from where the tags will be generated.


2. Update the following values (if required):
    1. NUM_STREAMS_PER_USER to set the number of streams that a user will be recommended via the collaborative recommender and 
    2. NUM_SIMILAR_STREAMS to set the number of streams that are the output of the similar stream filtering

3. client.py taken in multiple options.
   To see the options that are provided by client.py issue the below command:
   ```python client.py -h```
   
   The output of the above is the below and based on the values provided different output files will be generated.   
	
	```usage: client.py [-h] [-tags tags] [-sg SG] [-d D] [-g G] [-e E] [-all All]

     optional arguments:
     -h, --help  show this help message and exit
     -tags tags  Whether to generate the tags from the complete stream details
     -sg SG      Whether to generate the tag frequencies for the streams. Enter a value of 1, if you want files to be generated and 0 otherwise.
     -d D        The distance metric to use to compute the similar streams.
                 Accepted values = jaccard,custom and cosine
     -g G        Whether to generate the ratings files. Enter a value of 1, if you want files to be generated and 0 otherwise.
     -e E        Evaluate all recommender models. Enter a value of 1, if you want all recommender systems to be evaluated and 0 otherwise.
	 -gp GP      Generate predictions for a user using the best collaborative filtering algorithm. Enter a value of 1, if you want the file to be generated and 0 otherwise.
	 -all ALL    Whether all options should be executed. If set to 1 will override all other values.
    ```