# custom imports
import constants
import configurations
from base_operations import base_operations
from svd_algo_wrapper import svd_algo_wrapper
from svdpp_algo_wrapper import svdpp_algo_wrapper
import model_params

class best_model_output_generator(base_operations):
    """Generates the outputs from the best model that has been obtained"""
    def __init__(self):
        super(best_model_output_generator, self).__init__(constants.COLLABORATIVE_FILTERING_MODELER_NAME)

    def perform_operation(self):
        self.LOG_HANDLE.info("Running the best collaborative filtering algorithm...")
        latest_ratings_file_name = self.get_latest_output_file_name(configurations.RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME, next=False)[1]
        latest_ratings_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_ratings_file_name)
        self.LOG_HANDLE.info("Training best recommender model on the file here: " + latest_ratings_file_location)
        print("Training best recommender model")

        # Params from here: http://surprise.readthedocs.io/en/stable/reader.html
        reader = Reader(sep=constants.COMMA_STR)

        # Params from here: http://surprise.readthedocs.io/en/stable/dataset.html
        ratings_dataset = Dataset.load_from_file(latest_ratings_file_location, reader)

        # Get the users and streams that are of interest