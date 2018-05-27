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

    def get_nearest_neighbors_by_streamid(self, streamid, userid):
        """
        Get the pre-computed nearest neighbors by the stream id
        :param streamid: The stream Id
        :param userid: The user Id
        :return: The details of the streams that are the nearest neighbors of the current stream
        """
        print("Neighbors for Stream ID requested: " + streamid + " and for user: " + userid)
        all_stream_details = {}
        controller = content_controller()
        original_stream_details_list = controller.get_stream_details([streamid])

        if original_stream_details_list is not None and len(original_stream_details_list) > 0:
            original_stream_details = original_stream_details_list[0]
            all_stream_details["Target"] = original_stream_details

            try:
                latest_similar_streams_file_name = self.get_latest_output_file_name(configurations.SIMILAR_STREAMS_GENRATED_FILE_NAME, False)[1]
                latest_similar_streams_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_similar_streams_file_name)

                latest_stream_tag_mapping_file_name = self.get_latest_output_file_name(configurations.TAG_FREQUENCY_STREAMS, False)[1]
                latest_stream_tag_mapping_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, latest_stream_tag_mapping_file_name)

                input_df = pd.read_csv(latest_similar_streams_file_location, index_col=0, header=0)
                print(input_df.head())
                similar_streams_row = input_df.loc[int(streamid)]
                similar_streams_row = [str(int(streamid)) for streamid in similar_streams_row if not math.isnan(streamid)]
                print("Number of similar streams: " + str(len(similar_streams_row)))

                similar_stream_details = controller.get_stream_details(similar_streams_row)

                filtered_similar_streams = self.filter_streams_user_permitted_to_view(similar_stream_details, configurations.USER_DETAILS_FILE_LOCATION, latest_stream_tag_mapping_file_location, userid)
                if filtered_similar_streams:
                    all_stream_details["Neighbors"] = filtered_similar_streams

                return json.dumps(all_stream_details)

            except Exception as e:
                print(e)
                raise
                #return None

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
                filtered_recommended_streams = recommended_streams

                if filtered_recommended_streams:
                    all_recommended_stream_details["RecommendedStreams"] = filtered_recommended_streams
                else:
                    print("The user is not authorized to view any of the similar streams")

                return json.dumps(all_recommended_stream_details)

            except KeyError:
                print("The user with ID: {0} was not found.".format(userid))
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


    def filter_streams_user_permitted_to_view(self, candidate_streams, user_details_file_location, stream_tag_mapping_file_location, userid):
        """
        Filter the streams the user is permitted to view
        :param candidate_streams: The list of candidate streams to be filtered
        :param user_details_file_location: The location of the user details file
        :param stream_tag_mapping_file_location: The location of the file containing the stream tag mapping
        :param userid: The ID of the current user
        :return: the streams that the user is permitted to view
        """
        if not os.path.exists(user_details_file_location):
            print("The path for the user details file {0} does not exist.".format(user_details_file_location))
            return candidate_streams

        print("Getting the streams user is permitted to view")
        user_details_df = pd.read_csv(user_details_file_location, header=0, encoding="ISO-8859-1")
        streams_with_tags_df = pd.read_csv(stream_tag_mapping_file_location, header=0, index_col=0, encoding="ISO-8859-1")

        available_streams_with_tags = set(streams_with_tags_df.index.values)
        permitted_streams = []
        print("Number of streams in candidate: " + str(len(candidate_streams)))
        for stream in candidate_streams:
            stream_id = stream["streamid"]
            if int(stream_id) in available_streams_with_tags:
                attribute_values = []
                for attribute in configurations.USER_ATTRIBUTES_TO_SELECT:
                    attribute_values.append(user_details_df.loc[user_details_df[configurations.USER_ID_COLUMN_NAME] == int(userid)][attribute].values[0])

                should_add_stream = True
                attribute_value = ""

                for attribute_value in attribute_values:

                    # check if the attribute value exists as a tag for the streams
                    if attribute_value in streams_with_tags_df:

                        # get the value of the attribute in the stream
                        stream_attribute_value = int(streams_with_tags_df.at[int(stream_id), str(attribute_value)])

                        # if the value of the attribute in the stream is 0
                        if stream_attribute_value == 0:
                            should_add_stream = False
                            break

                if should_add_stream:
                    permitted_streams.append(stream)
                else:
                    print("Not added the stream {0} for the user {1} due to the attribute: {2}".format(str(stream_id), userid, attribute_value))
        print("Number of permitted streams: " + str(len(permitted_streams)))
        return permitted_streams

