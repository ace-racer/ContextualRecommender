import math
import pandas as pd
import numpy as np
import os

import configurations
import constants
from base_operations import base_operations


class TagGeneratorBase(base_operations):
    def __init__(self):
        pass

    def get_stream_details(self):
        print("Reading the stream details...")
        complete_stream_details_df = pd.read_csv(configurations.COMPLETE_STREAM_DETAILS_LOCATION, encoding="ISO-8859-1")
        if complete_stream_details_df is not None:
            complete_stream_details_dict = {}
            for _, row in complete_stream_details_df.iterrows():
                
                stream_id = str(row["CARDID"])
                # if the stream ID already exists in the dictionary
                if complete_stream_details_dict.get(stream_id):
                    existing_content = complete_stream_details_dict[stream_id]
                    new_content = existing_content + "\n" + row["HTML_CONTENT"]
                    complete_stream_details_dict[stream_id] = new_content
                else:
                    complete_stream_details_dict[stream_id] = row["HTML_CONTENT"]
            
            return complete_stream_details_dict

    def create_stream_tag_mapping_file(self, stream_id_tag_list):
        """
         Creates the stream tag mapping file
        """
        output_content = ""
        if stream_id_tag_list and len(stream_id_tag_list) > 0:
            for stream_id_tag in stream_id_tag_list:
                output_content += str(stream_id_tag[0]) + "," + stream_id_tag[1] + "\n"
            
            with open(configurations.STREAM_TAG_MAPPING_FILE_LOCATION, "w", encoding = "ISO-8859-1") as fw:
                fw.writelines(output_content)
            
            print("Output tags written to file here: " + configurations.STREAM_TAG_MAPPING_FILE_LOCATION)

    def generate_tags(self):
        pass




        