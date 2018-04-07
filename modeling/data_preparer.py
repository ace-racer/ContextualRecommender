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
NEWLINE = "\n"
RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME = "ratings_file_required_format.csv"


class data_preparer(base_operations):
    """
    The class containing the data preparer methods
    """
    def __init__(self):
        super(data_preparer, self).__init__(constants.DATA_PREPARER_NAME)

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

        # write with the NAs
        content_views_by_card_ratings_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY,
                                                              CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME)
        content_views_by_user.to_csv(content_views_by_card_ratings_location)

        # fill the NA values with 0 - revert back the NA changes for binning
        content_views_by_user = pd.read_csv(content_views_by_card_ratings_location)
        content_views_by_user = content_views_by_user.fillna(value="0")

        # write the ratings output to file
        content_views_by_card_ratings_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, CONTENT_VIEWS_BY_USER_BY_CARD_RATINGS_GENERATED_FILE_NAME)
        content_views_by_user.to_csv(content_views_by_card_ratings_location)
        self.LOG_HANDLE.info("Content views by user by card ratings generated: " + content_views_by_card_ratings_location)
        print("Created the ratings file...")

        # The format of the ratings for further processing is user ; item ; rating ;
        output_ratings_content = ""
        for stream_id in content_views_by_user:
            for index, row in content_views_by_user[stream_id].iterrows():
                if row[stream_id] != 0:
                    output_ratings_content += index + "," + stream_id + "," + row[stream_id] + NEWLINE

        with open(RATINGS_FILE_IN_REQUIRED_FORMAT_FILE_NAME, "w") as fw:
            fw.writelines(output_ratings_content)

        self.LOG_HANDLE.info("Generated the ratings file in required format")
        print("Generated ratings file in required format.")