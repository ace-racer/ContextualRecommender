"""Run the modelling tasks using SurPRISE library: http://surpriselib.com/"""
from surprise import SVD
from surprise.model_selection import cross_validate

# standard imports
import matplotlib.pyplot as plt
import os
import pandas


# custom imports
import constants
import configurations
from base_operations import base_operations

# constants


class collaborative_filtering_modeller(base_operations):
    """
    The class containing the data preparer methods
    """
    def __init__(self):
        super(collaborative_filtering_modeller, self).__init__(constants.COLLABORATIVE_FILTERING_MODELER_NAME)

    def perform_operation(self):
        latest_ratings_file_name = self.get_latest_output_file_name(configurations.RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME)[1]
        latest_ratings_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_ratings_file_name)
        self.perform_SVD(latest_ratings_file_location)

    def perform_SVD(self, ratings_file_location):
        if ratings_file_location:
            