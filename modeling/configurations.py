import logging

from collaborative_filtering.knn_algo_wrapper import knn_algo_wrapper
from collaborative_filtering.svd_algo_wrapper import svd_algo_wrapper
from collaborative_filtering.svdpp_algo_wrapper import svdpp_algo_wrapper

# configs to be updated as required

# contains the stream details - stream, tag, cards info
STREAM_DETAILS_FILE_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\stream_details.csv"

# contains the stream view information with the timestamps
STREAM_VIEWS_FILE_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\stream_views\\0907to0908.csv"

# contains the stream tag mapping filr
STREAM_TAG_MAPPING_FILE_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\stream_tag_mapping_original.csv"

# where all the generated files will be stored - the files follow a sequential numbering scheme
OUTPUT_FILES_DIRECTORY = "H:\\TeamStreamz_IW\\code\\data\\generated\\ratings"

# where all the log files will be created
log_file_folder_location = "H:\\TeamStreamz_IW\\code\\modeling\\logs"

# The collaborative filtering algorithm to choose - currently set to KNN with item similarity
CHOSEN_COLLABORATIVE_ALGORITHM = knn_algo_wrapper

# ******************** Below parameters to be updated only if really required ********************

# operational params - update as required
GENERATE_RATINGS_FILES = False
EVALUATE_ALL_MODELS = True
RUN_BEST_MODEL = True
NUM_STREAMS_PER_USER = 5
NUM_SIMILAR_STREAMS = 5
NUM_MOST_COMMON_STREAMS = 10

# configs to be updated only if required

CONTENT_VIEWS_BY_USER_BY_CARD_GENERATED_FILE_NAME = "content_views_by_user_by_card"
CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME = "content_views_user_rating"
RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME = "ratings_file_required_format"
PREDICTED_RATINGS_FILE_NAME = "predicted_ratings"
PREDICTED_STREAMS_FOR_USER = "predicted_streams_for_user"
TAG_FREQUENCY_STREAMS = "tag_frequency_streams"
SIMILAR_STREAMS_GENRATED_FILE_NAME = "similar_streams"
TF_IDF_FILE_NAME = "tf_idf_streams"

# configurations for binning to get the ratings
RATINGS_LOWER = 1
RATINGS_UPPER = 5
SAME_INTERVALS = True

# logging parameters
LOG_LEVEL = logging.INFO
log_pattern = "%(asctime)s %(levelname)s %(message)s"

# Stream-stream similarity
COLUMNS_TO_SELECT = ["StreamID"]
