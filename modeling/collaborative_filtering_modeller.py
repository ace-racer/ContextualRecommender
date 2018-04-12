"""Run the modelling tasks using SurPRISE library: http://surpriselib.com/"""

# Surprise library imports
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise.reader import Reader
from surprise.model_selection import train_test_split


# standard imports
import matplotlib.pyplot as plt
import os
import pandas


# custom imports
import constants
import configurations
from base_operations import base_operations
import model_params

# constants


class collaborative_filtering_modeller(base_operations):
    """
    The class containing the data preparer methods
    """
    def __init__(self):
        super(collaborative_filtering_modeller, self).__init__(constants.COLLABORATIVE_FILTERING_MODELER_NAME)

    def perform_operation(self):
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

        # Run the algorithms one by one and get their performance on the training data
        self.perform_SVD(trainset, testset)

        print("All recommender models have been run...")

    def perform_SVD(self, trainset, testset):
        """
        Run SVD on the ratings data set
        :param trainset:
        :param testset:
        :return:
        """
        if ratings_dataset:
            self.LOG_HANDLE.info("Running SVD on the training set with measures = {0} and CV folds = {1}".format(str(model_params.all_models_training_error_measures), str(model_params.cross_validation_folds)))

            # Use the famous SVD algorithm.
            algo = SVD()

            # Run cross-validation and print results
            # cross_validate(algo, ratings_dataset, measures=model_params.all_models_training_error_measures, cv=model_params.cross_validation_folds, verbose=True)
            # Train the algorithm on the trainset, and predict ratings for the testset
            algo.fit(trainset)
            predictions = algo.test(testset)

            # Then compute RMSE
            accuracy.rmse(predictions)




