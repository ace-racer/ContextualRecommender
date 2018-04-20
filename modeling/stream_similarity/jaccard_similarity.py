import csv
import pandas as pd
import numpy as np

import configurations
import constants

# constants
NEWLINE = "\n"
knn_columns_to_select = ["StreamID"]
num_nghbrs = 5
min_distance_threshold = 0

class jaccard_similarity:
    def __init__(self):
        pass
    def getColumnNames(self):
        """Get the column names for the output file"""
        column_names = ""

        # Generate column names for the target from the test data
        for column in knn_columns_to_select:
            column_names += "Target " + column + ","

        for itr in range(0, num_nghbrs):
            for column in knn_columns_to_select:
                column_names += "Neighbour " + str(itr + 1) + " " + column + ","

        column_names += "\n"
        return column_names
  
    def jaccard(self,im1, im2):

        im1 = np.asarray(im1).astype(np.bool)
        im2 = np.asarray(im2).astype(np.bool)

        intersection = np.logical_and(im1, im2)

        union = np.logical_or(im1, im2)
        # print intersection.sum() / (1+ float(union.sum()))

        return intersection.sum() / (1+float(union.sum()))

    def compute_similarities_generate_similar_streams(self, stream_tag_frequency_location, similar_streams_generated_file_location):
    
        df = pd.read_csv(stream_tag_frequency_location, header=None)

        stream_tag_frequencies = None
        with open(stream_tag_frequency_location, "r") as fr:
            stream_tag_frequencies = [line.strip().split(",") for line in fr.readlines()]

        # remove the first column for stream IDs
        num_tags = len(df.loc[1, :])

        # remove the first row for headers
        num_streams = len(df[0])-1

        print("# Tags: " + str(num_tags))
        print("# Streams: " + str(num_streams))

        LOW_VALUE = 0

        nearest_neighbors_content = self.getColumnNames()

        for stream_row_num in range(1, num_streams + 1):
            stream_id = stream_tag_frequencies[stream_row_num][0]
            source_stream_tag_frequencies = stream_tag_frequencies[stream_row_num][1:]
            nearest_neighbors_content += stream_id + ","
            # print("Source stream: " + stream_id)
            distances = []

            for other_stream_row_num in range(1, num_streams + 1):
                # Get the required values from the other stream row
                other_stream_id = stream_tag_frequencies[other_stream_row_num][0]
                other_stream_tag_frequencies = stream_tag_frequencies[other_stream_row_num][1:]
                # print("    Current stream: " + other_stream_id)

                if other_stream_row_num != stream_row_num:
                    distance = self.jaccard(source_stream_tag_frequencies, other_stream_tag_frequencies)
                     # print("Distance: " + str(distance))
                    distances.append((other_stream_id, distance))
                else:
                    distances.append((other_stream_id, LOW_VALUE))

            idx = 0
            distances = sorted(distances, key=lambda x: x[1],reverse=True)
            # print distances
            for stream_id_distance_mapping in distances:
                if idx < num_nghbrs:
                    print("Distance: " + str(stream_id_distance_mapping[1]))
                    nearest_neighbors_content += stream_id_distance_mapping[0] + ","
                    idx += 1
                else:
                    break

            nearest_neighbors_content += NEWLINE

        with open(similar_streams_generated_file_location, "w") as fw:
            fw.writelines(nearest_neighbors_content)

        print("Nearest neighbors using jaccarding distance generated...")
    
    