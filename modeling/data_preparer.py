import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import configurations
import os
from collections import Counter

import constants
import math


from base_operations import base_operations

# constants
CONTENT_VIEWS_BY_USER_BY_CARD_GENERATED_FILE_NAME = "content_views_by_user_by_card.csv"
CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME = "content_views_user_rating.csv"


class data_preparer(base_operations):
    """
    The class containing the data preparer methods
    """
    def __init__(self):
        super(data_preparer, self).__init__(constants.DATA_PREPARER_NAME)

    def discretize_by_equal_counts(self, values):
        if values is not None:
            num_values = len(values)
            available_ratings = range(configurations.RATINGS_LOWER, configurations.RATINGS_UPPER + 1)
            num_ratings = len(available_ratings)
            ratings_labels = [str(x) for x in available_ratings]

            # contains the count of items for each label
            label_counts = [0] * num_ratings

            # approx. number of items per label
            approx_items_per_label = num_values // num_ratings

            c = Counter(values)
            value_rating_mapper = c.keys()
            current_label_index = 0
            for k, c in c.items():
                if not math.isnan(k) and k != 0:
                    # if the count for the label after adding the count for this key is less than the approx number alloted then give this key the current label
                    if label_counts[current_label_index] + c <= approx_items_per_label:
                        value_rating_mapper[k] = str(current_label_index)
                        label_counts[current_label_index] = label_counts[current_label_index] + c
                    else:
                        # value by which this label count will exceed
                        exceeding_value = label_counts[current_label_index] + c - approx_items_per_label

                        #
                        if exceeding_value > (c // 2):
                            value_rating_mapper[k] = str(current_label_index)
                            label_counts[current_label_index] = label_counts[current_label_index] + c
                            current_label_index = current_label_index + 1
                        else:
                            if current_label_index < (num_ratings - 1):
                                current_label_index = current_label_index + 1

                            value_rating_mapper[k] = str(current_label_index)
                            label_counts[current_label_index] = label_counts[current_label_index] + c







    def perform_operation(self):
        stream_details_df = pd.read_csv(configurations.STREAM_DETAILS_FILE_LOCATION, encoding="ISO-8859-1")

        # Get the number of cards per stream
        cards_per_stream = stream_details_df.groupby('STREAMID')['CARDID'].nunique()

        content_views_df = pd.read_csv(configurations.STREAM_VIEWS_FILE_LOCATION, encoding="ISO-8859-1")

        # Get the content views by user
        unique_num_content_views_by_user = content_views_df.groupby('USERID')["STREAMID"].nunique()

        # Generate a pivot table from the views data
        content_views_by_user = pd.pivot_table(content_views_df, index="USERID", columns="STREAMID", values="TIMESTAMP",
                                               aggfunc="count")

        # fill the NA values with 0 - since there are no views for these contents
        content_views_by_user = content_views_by_user.fillna(value=0)

        print(content_views_by_user.head())

        # Get the number of views for a stream by the number of cards in that stream for the user
        for streamId in content_views_by_user:
            if cards_per_stream.get(streamId):
                content_views_by_user[streamId] = content_views_by_user[streamId] / cards_per_stream[streamId]
            else:
                self.LOG_HANDLE.info("No cards for the stream: " + str(streamId))

        content_views_by_card_by_user_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY,
                                                              CONTENT_VIEWS_BY_USER_BY_CARD_GENERATED_FILE_NAME)
        content_views_by_user.to_csv(content_views_by_card_by_user_location)
        self.LOG_HANDLE.info("Content views by user by card generated: " + content_views_by_card_by_user_location)

        # Get the ratings by binning the values across the streams - inclusive of the upper range
        self.LOG_HANDLE.info("Trying to get ratings for the streams")
        available_ratings = range(configurations.RATINGS_LOWER, configurations.RATINGS_UPPER + 1)
        num_ratings = len(available_ratings)
        ratings_labels = [str(x) for x in available_ratings]

        # change all 0's to not a number to avoid binning
        content_views_by_user[content_views_by_user == 0] = np.nan

        if configurations.SAME_INTERVALS:
            # the below performs equal interval binning
            for stream_id in content_views_by_user:
                content_views_by_user[stream_id] = pd.cut(content_views_by_user[stream_id], num_ratings, labels = ratings_labels, include_lowest = False)
        else:
            for stream_id in content_views_by_user:
                content_views_by_user[stream_id] = pd.qcut(content_views_by_user[stream_id], num_ratings, labels = ratings_labels, duplicates = 'drop')

        # fill the NA values with 0 - revert back the NA changes for binning
        # content_views_by_user = content_views_by_user.fillna(value="0")

        # write the ratings output to file
        content_views_by_card_ratings_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME)
        content_views_by_user.to_csv(content_views_by_card_ratings_location)
        self.LOG_HANDLE.info("Content views by user by card ratings generated: " + content_views_by_card_ratings_location)

