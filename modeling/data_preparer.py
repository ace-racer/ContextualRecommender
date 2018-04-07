import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import configurations
import os
import constants

from base_operations import base_operations


CONTENT_VIEWS_BY_USER_BY_CARD_GENERATED_FILE_NAME = "content_views_by_user_by_card.csv"


class data_preparer(base_operations):
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
