"""Contains the methods for getting details of content"""
import sqlite3
import json
import datetime

import constants
import configurations

class content_controller:

    def __init__(self):
        pass

    def get_stream_details_with_tags(self, streamids):
       """
       Get the details including the tags of all the streams whose IDs are provided
       :param streamids: The ID of the streams
       :return: The details of all the streams
       """

       if streamids and len(streamids) > 0:


        return None


    def get_stream_details(self, streamids):
        """
        Get only the stream details of all the streams whose IDs are provided
        :param streamids: The ID of the streams
        :return: The details of all the streams
        """
        select_query_details = "select organization, streamid, streamname, cardid, cardname from {0} where streamid in ({1})"

        # envelop the stream Ids in quotes
        streamids = ["\"" + streamid + "\"" for streamid in streamids]
        selectids_select_param = ",".join(streamids)
        print("Select param: " + selectids_select_param)

        select_query_details_updated = select_query_details.format(constants.stream_details_table_name, selectids_select_param)
        print("Complete query: " + select_query_details_updated)

        conn = sqlite3.connect(configurations.db_location)
        try:
            c = conn.cursor()
            c.execute(select_query_details_updated)
            stream_details = c.fetchall()
            print("Number of results: " + str(len(stream_details)))

            # TODO: Add code to get tags for the streams and concatenate them

            return stream_details
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()
