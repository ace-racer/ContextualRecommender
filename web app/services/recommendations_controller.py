"""Contains the methods for content - content recommendations"""
import sqlite3
import json
import datetime
import os
import pandas as pd
import re
import math

import constants
import configurations
from content_controller import content_controller

# constants
FILE_NUMBER_PATTERN = "_([0-9]+).csv$"

class recommender_controller:

    def __init__(self):
        pass

    def get_nearest_neighbors_by_streamid(self, streamid):
        """
        Get the pre-computed nearest neighbors by the stream id
        :param streamid: The stream Id
        :return: The details of the streams that are the nearest neighbors of the current stream
        """
        all_stream_details = {}
        controller = content_controller()
        original_stream_details_list = controller.get_stream_details([streamid])

        if original_stream_details_list is not None and len(original_stream_details_list) > 0:
            original_stream_details = original_stream_details_list[0]
            all_stream_details["Target"] = original_stream_details
            nearest_neighbor_query = "select n1streamid, n2streamid, n3streamid, n4streamid, n5streamid from nearest_neighbor_streams where targetstreamid = \"{0}\""
            nearest_neighbor_query_updated = nearest_neighbor_query.format(streamid)
            print("NN query: " + nearest_neighbor_query_updated)
            conn = sqlite3.connect(configurations.db_location)
            try:
                c = conn.cursor()
                c.execute(nearest_neighbor_query_updated)
                nearest_neighbors = c.fetchall()
                print(nearest_neighbors)
                neighbors = [n for n in nearest_neighbors[0]]
                print("Number of nearest neighbors: " + str(len(neighbors)))
                neighbor_details = controller.get_stream_details(neighbors)

                if neighbor_details:
                    all_stream_details["Neighbors"] = [neighbor_detail for neighbor_detail in neighbor_details]

                return json.dumps(all_stream_details)
            except Exception as e:
                print(e)
                return None
            finally:
                conn.close()

        return None

    def get_recommendations_for_user(self, userid):
        """
        Get the recommendations for the user
        :param userid: The ID of the user for whom to get the recommendations
        :return: Recommendations for the user
        """
        if userid:
            print("Trying to get recommendations for user: " + userid)
            all_recommended_stream_details = {}
            controller = content_controller()
            try:
                userid = int(userid)
                latest_predicted_streams_file_name = self.get_latest_output_file_name(configurations.PREDICTED_STREAMS_FOR_USER, False)[1]
                latest_predicted_streams_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_predicted_streams_file_name)
                input_df = pd.read_csv(latest_predicted_streams_file_location, index_col=0, header=None)
                print(input_df.head())
                recommended_streams_row = input_df.loc[userid]
                recommended_streams_row = [str(int(streamid)) for streamid in recommended_streams_row if not math.isnan(streamid)]
                print(recommended_streams_row)
                print("Number of recommended streams: " + str(len(recommended_streams_row)))

                recommended_streams = controller.get_stream_details(recommended_streams_row)
                if recommended_streams:
                    all_recommended_stream_details["RecommendedStreams"] = [recommended_stream for recommended_stream in recommended_streams]

                return json.dumps(all_recommended_stream_details)

            except KeyError:
                print("The user with ID: {0} was not found.".format(userid))
                raise
            except Exception as ex:
                print("An exception occurred: " + str(ex))
            return None

    def get_latest_output_file_name(self, file_name_pattern, next=True):
        """
        Get the name of the latest output file name
        :param file_name_pattern: The pattern expected in the output file
        :param next: Whether to return the next file names or the current latest ones
        :return: A tuple where the first element is the number of the output file and the second is the complete file name with the number
        """

        if file_name_pattern:
            largest_output_file_number = 0
            for item in os.listdir(configurations.OUTPUT_FILES_DIRECTORY):
                if os.path.isfile(os.path.join(configurations.OUTPUT_FILES_DIRECTORY, item)) and file_name_pattern in item:
                    # search if the file number pattern is present in the current file
                    if re.search(FILE_NUMBER_PATTERN, item):
                        current_file_number = int(re.findall(FILE_NUMBER_PATTERN, item)[0])
                        if current_file_number > largest_output_file_number:
                            largest_output_file_number = current_file_number

            if next:
                next_file_number = largest_output_file_number + 1
                return next_file_number, file_name_pattern + constants.UNDERSCORE_STR + str(next_file_number) + constants.CSV_FILE_EXTENSION
            else:
                if largest_output_file_number == 0:
                    raise ValueError("No file has been generated yet and so cannot retrieve")
                return largest_output_file_number, file_name_pattern + constants.UNDERSCORE_STR + str(largest_output_file_number) + constants.CSV_FILE_EXTENSION
