import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

# configurations
num_nghbrs = 5
stream_tag_frequency_location = "data/tag_frequency_streams.csv"
knn_columns_to_select = ["StreamID"]
min_distance_threshold = 0
nearest_neighbors_streams_output_file = "data/nearest_neighbor_streams.csv"
# end of configurations

# constants
NEWLINE = "\n"
# end of constants

def getColumnNames():
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

def tag_distance(x, y):
    """Get the tag distance between the records x and y"""
    num_tags = len(x)
    c1 = 0
    c2 = 0
    for itr in range(0, num_tags):
        if x[itr] == '1' and x[itr] == y[itr]:
            c1 += 1
        elif x[itr] != y[itr]:
            c2 += 1
    distance = -(100*c1 - c2)
    return distance

stream_tag_frequencies = None
with open(stream_tag_frequency_location, "r") as fr:
    stream_tag_frequencies = [line.strip().split(",") for line in fr.readlines()]

# remove the first column for stream IDs
num_tags = len(stream_tag_frequencies[0]) - 1

# remove the first row for headers
num_streams = len(stream_tag_frequencies) - 1

print("# Tags: " + str(num_tags))
print("# Streams: " + str(num_streams))

HIGH_VALUE = 1000000

nearest_neighbors_content = getColumnNames()

print("Value: " + stream_tag_frequencies[1][0])

for stream_row_num in range(1, num_streams + 1):
    stream_id = stream_tag_frequencies[stream_row_num][0]
    source_stream_tag_frequencies = stream_tag_frequencies[stream_row_num][1:]
    nearest_neighbors_content += stream_id + ","
    print("Source stream: " + stream_id)
    distances = []

    for other_stream_row_num in range(1, num_streams + 1):
        # Get the required values from the other stream row
        other_stream_id = stream_tag_frequencies[other_stream_row_num][0]
        other_stream_tag_frequencies = stream_tag_frequencies[other_stream_row_num][1:]
        # print("    Current stream: " + other_stream_id)

        if other_stream_row_num != stream_row_num:
            distance = tag_distance(source_stream_tag_frequencies, other_stream_tag_frequencies)
            #print("    Distance: " + str(distance))
            distances.append((other_stream_id, distance))
        else:
            distances.append((other_stream_id, HIGH_VALUE))

    idx = 0
    distances = sorted(distances, key=lambda x: x[1])
    for stream_id_distance_mapping in distances:
        if idx < num_nghbrs:
            print("    Distance: " + str(stream_id_distance_mapping[1]))
            nearest_neighbors_content += stream_id_distance_mapping[0] + ","
            idx += 1
        else:
            break

    nearest_neighbors_content += NEWLINE

with open(nearest_neighbors_streams_output_file, "w") as fw:
    fw.writelines(nearest_neighbors_content)

print("Nearest neighbors generated...")