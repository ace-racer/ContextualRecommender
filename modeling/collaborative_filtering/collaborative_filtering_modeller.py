"""Run the modelling tasks using SurPRISE library: http://surpriselib.com/"""

# Surprise library imports
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise.reader import Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
from surprise.model_selection import GridSearchCV


# standard imports
import matplotlib.pyplot as plt
import os
import pandas


# custom imports
import constants
import configurations
from base_operations import base_operations
from collaborative_filtering.svd_algo_wrapper import svd_algo_wrapper
from collaborative_filtering.knn_algo_wrapper import knn_algo_wrapper
from collaborative_filtering.normal_algo_wrapper import normal_algo_wrapper
from collaborative_filtering.svdpp_algo_wrapper import svdpp_algo_wrapper
import model_params

# constants


class collaborative_filtering_modeller(base_operations):
    """
    The class containing the collaborative filtering algorithms to choose the best
    """
    def __init__(self):
        super(collaborative_filtering_modeller, self).__init__(constants.COLLABORATIVE_FILTERING_MODELER_NAME)

    def perform_operation(self):
        self.LOG_HANDLE.info("Running the collaborative filtering algorithms...")
        latest_ratings_file_name = self.get_latest_output_file_name(configurations.RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME, next=False)[1]
        latest_ratings_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_ratings_file_name)
        self.LOG_HANDLE.info("Running recommender models on the file here: " + latest_ratings_file_location)
        print("Running all recommender models")

        # Params from here: http://surprise.readthedocs.io/en/stable/reader.html
        reader = Reader(sep=constants.COMMA_STR)

        # Params from here: http://surprise.readthedocs.io/en/stable/dataset.html
        ratings_dataset = Dataset.load_from_file(latest_ratings_file_location, reader)

        # Divide the data set into the training and test sets
        trainset, testset = train_test_split(ratings_dataset, test_size=model_params.test_set_size)

        # Add different algorithms here - Removed SVD PP algorithm
        collaborative_algorithms = [normal_algo_wrapper(), knn_algo_wrapper(), svd_algo_wrapper()]

        rmse_values = {}

        for collaborative_algorithm in collaborative_algorithms:
            print("Started Algorithm: " + collaborative_algorithm.algo_name)
            rmse_values[collaborative_algorithm.algo_name] = collaborative_algorithm.evaluate_on_test(trainset, testset)
            collaborative_algorithm.perform_grid_search_with_cv(ratings_dataset)
            print("Completed Algorithm: " + collaborative_algorithm.algo_name)

        print("All recommender models have been run...")
        plt.scatter(rmse_values.keys(), rmse_values.values())
        plt.xlabel('Collaborative filtering algorithm')
        plt.ylabel('Root mean square error (RMSE) on test predictions')
        plt.show()





