# custom imports
import constants
import configurations
from base_operations import base_operations
from svd_algo_wrapper import svd_algo_wrapper
from svdpp_algo_wrapper import svdpp_algo_wrapper
import model_params

# standard imports
import pandas as pd
import os

# Surprise library imports
from surprise.reader import Reader
from surprise import Dataset
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import train_test_split

# constants
NEWLINE = "\n"


class best_model_output_generator(base_operations):
    """Generates the outputs from the best model that has been obtained"""
    def __init__(self):
        super(best_model_output_generator, self).__init__(constants.COLLABORATIVE_FILTERING_MODELER_NAME)
        # the best algorithm
        self.best_algo = svd_algo_wrapper()

    def perform_operation(self):
        self.LOG_HANDLE.info("Running the best collaborative filtering algorithm...")
        latest_ratings_file_name = self.get_latest_output_file_name(configurations.RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME, next=False)[1]
        latest_ratings_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_ratings_file_name)
        self.LOG_HANDLE.info("Training best recommender model on the file here: " + latest_ratings_file_location)
        print("Training best recommender model")

        # Params from here: http://surprise.readthedocs.io/en/stable/reader.html
        reader = Reader(sep=constants.COMMA_STR)

        # Get the users and streams that are of interest
        latest_actual_ratings_file_name = self.get_latest_output_file_name(configurations.CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME, next=False)[1]
        latest_actual_ratings_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_actual_ratings_file_name)

        self.LOG_HANDLE.info("Reading user ratings from: " + latest_actual_ratings_file_location)
        print("Reading existing user ratings")

        # TODO: Add other logic to get streams for which to predict ratings
        user_streams_to_predict_df = self.get_streams_not_viewed_by_user(latest_actual_ratings_file_location)

        # user_streams_to_predict = Dataset.load_from_df(user_streams_to_predict_df, Reader(rating_scale=(0, configurations.RATINGS_UPPER)))
        data_auto_folds_train_ratings = DatasetAutoFolds(latest_ratings_file_location, reader)
        data_auto_folds_test_ratings = DatasetAutoFolds(df=user_streams_to_predict_df, reader = Reader(rating_scale=(0, configurations.RATINGS_UPPER)))

        ratings_dataset = data_auto_folds_train_ratings.build_full_trainset()
        test_dataset = data_auto_folds_test_ratings.build_full_trainset().build_testset()

        predictions = self.best_algo.train_best_model_generate_ratings_test(ratings_dataset, test_dataset)

        # print the predictions to a file - http://surprise.readthedocs.io/en/stable/predictions_module.html?highlight=prediction%20class
        prediction_output = constants.COMMA_STR.join(constants.PREDICTED_RATINGS_FILE_COLUMN_NAMES) + NEWLINE
        predictions_for_users = {}

        for prediction in predictions:
            # The uid, iid and estimated rating
            prediction_output += str(prediction[0]) + constants.COMMA_STR + str(prediction[1]) + constants.COMMA_STR + str(prediction[3]) + NEWLINE
            if predictions_for_users.get(str(prediction[0])):
                predictions_for_users[str(prediction[0])].append((str(prediction[1]), str(prediction[3])))
            else:
                predictions_for_users[str(prediction[0])] = [(str(prediction[1]), str(prediction[3]))]

        prediction_output_file_name = self.get_latest_output_file_name(configurations.PREDICTED_RATINGS_FILE_NAME)[1]
        prediction_output_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, prediction_output_file_name)

        with open(prediction_output_location, "w") as fw:
            fw.writelines(prediction_output)

        print("Generated the prediction results file")
        self.LOG_HANDLE.info("Generated the prediction results file")

        # Sort the predictions for the users
        for user in predictions_for_users:
            predictions_for_users[user] = sorted(predictions_for_users[user], reverse=True, key=lambda x: x[1])

        predicted_streams_content = ""
        for user in predictions_for_users:
            predicted_streams_content += str(user) + constants.COMMA_STR
            num_streams_for_user = min(configurations.NUM_STREAMS_PER_USER, len(predictions_for_users[user]))
            for stream_id, _ in predictions_for_users[user][:num_streams_for_user]:
                predicted_streams_content += str(stream_id) + constants.COMMA_STR

            predicted_streams_content += NEWLINE

        predicted_streams_output_file_name = self.get_latest_output_file_name(configurations.PREDICTED_STREAMS_FOR_USER)[1]
        predicted_streams_output_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, predicted_streams_output_file_name)

        with open(predicted_streams_output_location, "w") as fw:
            fw.writelines(predicted_streams_content)

        print("Generated the streams recommended to the user")
        self.LOG_HANDLE.info("Generated the streams recommended to the user")


    def get_streams_not_viewed_by_user(self, complete_ratings_file_location):
        """
        Get the streams that have not yet been viewed by the user
        :param complete_ratings_file_location:
        :return: A dataframe with the user stream details and 0 as ratings
        """
        if complete_ratings_file_location:
            ratings_df = pd.read_csv(complete_ratings_file_location, header=0, index_col=0)
            required_ratings = []
            for index, row in ratings_df.iterrows():
                for stream_id in ratings_df:
                    if row[stream_id] == 0:
                        required_ratings.append([str(index), str(stream_id), str(row[stream_id])])
            return pd.DataFrame(required_ratings)

        return None

