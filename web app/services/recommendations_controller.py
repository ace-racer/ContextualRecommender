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
        all_stream_details = {}
        controller = content_controller()
        original_stream_details = controller.get_stream_details([streamid])

        if original_stream_details is not None:
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