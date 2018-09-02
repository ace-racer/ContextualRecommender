"""Contains the methods for getting details of content"""
import sqlite3
import json
import datetime
import pandas as pd

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
        all_stream_details_formatted = []

        if configurations.CONNECT_TO_DATABASE:
            print("Getting the stream details from database")
            select_query_details = "select organization, streamid, streamname, cardid, cardname from {0} where streamid in ({1}) order by streamid"

            original_stream_id_list = streamids
            # envelop the stream Ids in quotes
            streamids = ["\"" + streamid + "\"" for streamid in streamids]
            selectids_select_param = ",".join(streamids)
            # print("Select param: " + selectids_select_param)

            select_query_details_updated = select_query_details.format(constants.stream_details_table_name, selectids_select_param)
            # print("Complete query: " + select_query_details_updated)

            stream_tag_query = "select streamid, tagname from {0} where streamid in ({1}) order by streamid"
            stream_tag_query_updated = stream_tag_query.format(constants.stream_tag_mapping_table_name, selectids_select_param)
            # print("Stream tag query: " + stream_tag_query_updated)

            conn = sqlite3.connect(configurations.db_location)
            try:
                c = conn.cursor()
                c.execute(select_query_details_updated)
                stream_details = c.fetchall()

                if stream_details is None:
                    return None

                # print("Number of results: " + str(len(stream_details)))
                num_stream_details = len(stream_details)
                # print(stream_details)

                c.execute(stream_tag_query_updated)
                stream_tag_mapping_query_results = c.fetchall()
                all_stream_tag_mapping = {}
                for stream_tag_mapping_query_result in stream_tag_mapping_query_results:
                    if all_stream_tag_mapping.get(stream_tag_mapping_query_result[0]):
                        all_stream_tag_mapping[stream_tag_mapping_query_result[0]].append(stream_tag_mapping_query_result[1])
                    else:
                        all_stream_tag_mapping[stream_tag_mapping_query_result[0]] = [stream_tag_mapping_query_result[1]]

                itr = 0
                while itr < num_stream_details:
                    stream_details_formatted = {}
                    current_stream_id = stream_details[itr][1]
                    stream_details_formatted["streamid"] = current_stream_id
                    stream_details_formatted["organization"] = stream_details[itr][0]
                    stream_details_formatted["streamname"] = stream_details[itr][2]
                    stream_details_formatted["order"] = original_stream_id_list.index(str(current_stream_id))
                    stream_details_formatted["tags"] = all_stream_tag_mapping.get(current_stream_id, [])

                    jtr = itr
                    cards = []
                    while jtr < num_stream_details and stream_details[jtr][1] == current_stream_id:
                        card_details = {}
                        card_details["cardid"] = stream_details[jtr][3]
                        card_details["cardname"] = stream_details[jtr][4]
                        cards.append(card_details)

                        jtr += 1

                    stream_details_formatted["cards"] = cards
                    all_stream_details_formatted.append(stream_details_formatted)
                    itr = jtr

                return all_stream_details_formatted
            except Exception as e:
                print(e)
                return None
            finally:
                conn.close()
        else:
            print("Getting the stream details from file")
            stream_details_df = pd.read_csv(configurations.STREAM_DETAILS_LOCATION, encoding = "ISO-8859-1")
            if stream_details_df is not None:

                # convert to integers
                streamids = [int(streamid) for streamid in streamids]
                
                # keep only the unique stream IDs
                unique_stream_ids = list(set(streamids))
                
                # get the details for the streams sorted by the stream id
                required_stream_details_df = stream_details_df[stream_details_df[configurations.STREAM_ID_COLUMN_NAME].isin(unique_stream_ids)].sort_values(by=[configurations.STREAM_ID_COLUMN_NAME])
                

            else:
                raise ValueError("The stream details file cannot be found")

