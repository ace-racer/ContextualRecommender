# custom imports
import constants
import configurations
from base_operations import base_operations
from stream_similarity.jaccard_similarity import jaccard_similarity
from stream_similarity.custom_stream_distance import custom_stream_distance
from stream_similarity.cosine_similarity import cosine_similarity

# standard imports
import pandas as pd
import os

# constants
NEWLINE = "\n"


class stream_similarity_evaluator(base_operations):
    """Generates the outputs from the best model that has been obtained"""
    def __init__(self, distance_measure):
        super(stream_similarity_evaluator, self).__init__(constants.STREAMS_SIMILARITY_EVALUATOR)
        self.distance_measure = distance_measure


    def perform_operation(self):
        self.LOG_HANDLE.info("Running the selected distance measure algorithms...")
        latest_tag_frequency_file = self.get_latest_output_file_name(configurations.TAG_FREQUENCY_STREAMS, next=False)[1]
        latest_tag_frequency_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_tag_frequency_file)
        self.LOG_HANDLE.info("Stream tag frequency file location: " + latest_tag_frequency_file_location)

        similar_streams_generated_file = self.get_latest_output_file_name(configurations.SIMILAR_STREAMS_GENRATED_FILE_NAME)[1]
        similar_streams_generated_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, similar_streams_generated_file)
        print("Evaluating distances")

        distance_measures_to_evaluate = None
        if self.distance_measure == constants.JACCARD_SIMILARITY:
            self.LOG_HANDLE.info("Finding the Jaccard similarity between the streams")
            distance_measures_to_evaluate = jaccard_similarity()

        if self.distance_measure == constants.CUSTOM_DISTANCE:
            self.LOG_HANDLE.info("Finding the custom distance between the streams")
            distance_measures_to_evaluate = custom_stream_distance()

        if self.distance_measure == constants.COSINE_SIMILARITY:
            self.LOG_HANDLE.info("Finding the cosine distance between the streams")
            distance_measures_to_evaluate = cosine_similarity()

        if distance_measures_to_evaluate:
            distance_measures_to_evaluate.compute_similarities_generate_similar_streams(latest_tag_frequency_file_location, similar_streams_generated_file_location)
            self.LOG_HANDLE.info("Generated the similar streams file")
        else:
            self.LOG_HANDLE.error("There is no similarity measure with the name {0}".format(self.distance_measure))
            print("There is no similarity measure with the name {0}".format(self.distance_measure))

