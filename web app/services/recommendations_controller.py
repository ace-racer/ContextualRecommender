"""Contains the methods for content - content recommendations"""
import sqlite3
import json
import datetime

import constants
import configurations
from content_controller import content_controller

class cc_recommender_controller:

    def __init__(self):
        pass

    def get_nearest_neighbors_by_streamid(self, streamid):
        """
        Get the pre-computed nearest neighbors by the stream id
        :param streamid: The stream Id
        :return: The details of the streams that are the nearest neighbors of the current stream
        """
        controller = content_controller()
        original_stream_details = controller.get_stream_details([streamid])

        if original_stream_details is not None:
            nearest_neighbor_query = "select n1streamid, n2streamid, n3streamid, n4streamid, n5streamid from nearest_neighbor_streams where targetstreamid = \"{0}\""
            nearest_neighbor_query_updated = nearest_neighbor_query.format(streamid)
            print("NN query: " + nearest_neighbor_query_updated)
            conn = sqlite3.connect(configurations.db_location)
            try:
                c = conn.cursor()
                c.execute(nearest_neighbor_query_updated)
                all_stream_details = c.fetchall()


                return json.dumps(all_stream_details)
            except Exception as e:
                print(e)
                return None
            finally:
                conn.close()

        return None