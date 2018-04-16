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
NEWLINE = "\n"
comma_str = ","
stream_name_location = 2
stream_id_location = 1
tag_location = 0


class stream_tag_one_hot_encoder(base_operations):
    """
    The class containing the data preparer methods
    """
    def __init__(self):
        super(stream_tag_one_hot_encoder, self).__init__(constants.DATA_PREPARER_NAME)
        self.unique_tags = None
        self.unique_tags_position_mapping = None

    def perform_operation(self):
        self.LOG_HANDLE.info("Starting the data preparation for similar streams recommendation...")

        ## Get the unique tags which are non-empty
        with open(configurations.STREAM_TAG_MAPPING_FILE_LOCATION, "r") as fr:
            unique_tags = {line.split(",")[tag_location].strip() for line in fr.readlines() if
                           line != "" and line.split(",")[tag_location].strip() != ""}

        ## Make a tag, position mapping
        unique_tags_position_mapping = {elem[1]: elem[0] for elem in enumerate(unique_tags)}

        stream_tag_mapping_original = None
        with open(configurations.STREAM_TAG_MAPPING_FILE_LOCATION, "r") as fr:
            stream_tag_mapping_original = [tuple(line.strip().split(",")) for line in fr.readlines()]

        # set to contain mapping between stream and unique tags
        stream_tag_mapping = {}
        output_file_name = self.get_latest_output_file_name(configurations.TAG_FREQUENCY_STREAMS)[1]
        output_file_location = os.path.join(configurations.OUTPUT_FILES_DIRECTORY, output_file_name)

        stream_tag_columns = 3

        for item in stream_tag_mapping_original:
            if len(item) != stream_tag_columns:
                continue

            stream_id = item[stream_id_location]
            tag = item[tag_location].strip()
            tag_pos = unique_tags_position_mapping[tag]

            if stream_tag_mapping.get(stream_id):
                stream_tag_mapping[stream_id].add(tag_pos)
            else:
                stream_tag_mapping[stream_id] = {tag_pos}

        output_frequency_content = ""
        num_unique_tags = len(unique_tags_position_mapping)

        # create the column headers
        output_frequency_content += "StreamID" + comma_str + comma_str.join(unique_tags_position_mapping) + NEWLINE

        for stream_id, tag_positions in stream_tag_mapping.items():
            # initialize all tags as 0
            frequencies_for_stream = ["0"] * num_unique_tags

            # set the values to 1 where tags are seen
            for tag_position in tag_positions:
                frequencies_for_stream[tag_position] = "1"

            output_frequency_content += stream_id + comma_str + comma_str.join(frequencies_for_stream) + NEWLINE

        with open(output_file_location, "w") as fw:
            fw.writelines(output_frequency_content)

        print("Tag frequencies written to file...")
        self.LOG_HANDLE.info("Tag frequencies written to file...")
