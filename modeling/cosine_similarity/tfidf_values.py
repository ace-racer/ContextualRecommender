import math
import csv
import pandas as pd
import numpy as np

# configurations
stream_tag_frequency_location = "/Users/shriyashekhar/Documents/IWork/ProcessedData/tag_frequency_streams_1.csv"
no_of_tags_in_stream = 3
num_nghbrs = 5
knn_columns_to_select = ["StreamID"]
tfidf_streams_output_file = "/Users/shriyashekhar/Documents/IWork/ProcessedData/tfidf_values_1.csv"
streamlist = []
tf_idf_array =[]
# end of configurations

# constants
NEWLINE = "\n"
# end of constants

df = pd.read_csv(stream_tag_frequency_location, header=None)

stream_tag_frequencies = None
with open(stream_tag_frequency_location, "r") as fr:
    stream_tag_frequencies = [line.strip().split(",") for line in fr.readlines()]

# remove the first column for stream IDs
num_tags = len(df.loc[1, :])

# remove the first row for headers
num_streams = len(df[0])-1
streams_in_collection = num_streams

print("# Tags: " + str(num_tags))
print("# Streams: " + str(num_streams))
print(stream_tag_frequencies)
# print(df.iloc[0])
# print(df.loc[1, :][0])



def getColumnNames():
    """Get the column names for the output file"""
    column_names = []

    # Generate column names for the target from the test data
    for column in df.iloc[0]:
        column_names +=  column + ','

    column_names += "\n"
    return column_names



tfidf_content = getColumnNames()


def tf_calculate(num_streams):
    tf_value = []
    tf_value_for_a_stream =[]
    for stream_index in range(1, num_streams):
        no_of_tags_in_stream =  no_of_tags_with_a_stream(stream_index)

        cell_content = df.iloc[stream_index]
        for each_tag in range(1, num_tags):
            if cell_content[each_tag] == '0':
                tf_value_for_a_stream = 0
            else:
                tf_value_for_a_stream += float(1.0/(1.0+no_of_tags_in_stream))
            tf_value.append(tf_value_for_a_stream)
        B = np.reshape(tf_value, (-1, 67))
            # tf_value += tf_value_for_a_stream
    print(B)
    return B

def no_of_tags_with_a_stream(stream_index):
    #df = pd.read_csv(stream_tag_frequency_location, header=None)
    tags_for_stream = df.iloc[stream_index]
    # print(len(tags_for_stream[tags_for_stream == '1']))
    return len(tags_for_stream[tags_for_stream == '1'])


def no_of_streams_with_a_tag(tag_index):
    stream_for_tag = df.iloc[:,tag_index]
    # print(stream_for_tag)
    return len(stream_for_tag[stream_for_tag == '1'])


def idf_calculate(num_tags):
    idf_value =[]
    for tag_index in range(1, num_tags):
        idf_value_for_a_tag = math.log((num_streams) / (1.0 + no_of_streams_with_a_tag(tag_index)))
        idf_value.append(idf_value_for_a_tag)
    print(idf_value)
    # print(len(idf_value))
    return idf_value

# tf_calculate(num_streams)
tf =[]
tf = tf_calculate(num_streams)
idf =[]
idf =idf_calculate(num_tags)
for i in range(0, num_streams-1):
    tfidf_content += df.loc[i + 1, :][0]  + "," + " "
    for j in range(0, num_tags-1):
        tf_idf = tf[i][j] * idf[j]
        tfidf_content += str(tf_idf) + "," + " "
        # tfidf_content = tf_idf_array
    tfidf_content += NEWLINE



with open(tfidf_streams_output_file, "w") as fw:
    fw.writelines(tfidf_content)


print("TFIDF Values generated...")
