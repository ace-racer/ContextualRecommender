import logging

STREAM_DETAILS_FILE_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\stream_details.csv"
STREAM_VIEWS_FILE_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\stream_views\\0907to0908.csv"

OUTPUT_FILES_DIRECTORY = "H:\\TeamStreamz_IW\\code\\data\\generated\\ratings"

CONTENT_VIEWS_BY_USER_BY_CARD_GENERATED_FILE_NAME = "content_views_by_user_by_card"
CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME = "content_views_user_rating"
RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME = "ratings_file_required_format"

# configurations for binning to get the ratings
RATINGS_LOWER = 1
RATINGS_UPPER = 5
SAME_INTERVALS = True

# logging parameters
LOG_LEVEL = logging.INFO
log_file_folder_location = "H:\\TeamStreamz_IW\\code\\modeling\\logs"
log_pattern = "%(asctime)s %(levelname)s %(message)s"

# other params
GENERATE_RATINGS_FILES = False
EVALUATE_ALL_MODELS = True
RUN_BEST_MODEL = True