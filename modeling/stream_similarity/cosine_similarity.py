import math
import pandas as pd
import numpy as np
import os

import configurations
import constants
from base_operations import base_operations

NEWLINE = "\n"
knn_columns_to_select = configurations.COLUMNS_TO_SELECT
num_nghbrs = configurations.NUM_SIMILAR_STREAMS

class cosine_similarity(base_operations):
    def __init__(self):
        pass

    def _get_column_names(self):
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

    def _get_number_of_tags_for_stream(self, stream_index):
        """
        Get the number of tags for a stream - the number of 1's for the tags
        :param stream_index: The index of the stream
        :return: The number of tags for the stream
        """
        tags_for_stream = self.df.iloc[stream_index]
        if tags_for_stream[tags_for_stream == 1] is not None:
            return len(tags_for_stream[tags_for_stream == 1])
        else:
            return 0

    def _get_number_of_streams_for_tag(self, tag_index):
        """
        Get the number of streams for a tag identified by its index
        :param tag_index:
        :return:
        """
        stream_for_tag = self.df.iloc[:, tag_index]
        if stream_for_tag[stream_for_tag == 1] is not None:
             return len(stream_for_tag[stream_for_tag == 1])
        else:
            return 0

    def _get_term_frequency_for_streams(self, num_streams, num_tags):
        """
        Get the term frequency for all the streams
        :param num_streams: The number of streams
        :param num_tags: The number of tags
        :return: A num streams * num tags matrix with the TF of the streams and the tags
        """
        tf_value = []

        for stream_index in range(0, num_streams):
            num_tags_for_stream = self._get_number_of_tags_for_stream(stream_index)
            stream_row = self.df.iloc[stream_index]
            tf_value_for_a_stream = []
            for tag_index in range(1, num_tags):
                if stream_row[tag_index] == 1:
                    tf_value_for_a_stream.append(float(1.0 / (1.0 + num_tags_for_stream)))
                else:
                    tf_value_for_a_stream.append(0)
            tf_value.append(tf_value_for_a_stream)

        return tf_value

    def _get_inverse_document_frequency_for_tags(self, num_streams, num_tags):
        """
        Get the inverse document frequency for the tags
        :param num_streams:
        :param num_tags:
        :return: The IDF values for the tags
        """
        idf_value = []
        for tag_index in range(0, num_tags):
            idf_value_for_a_tag = math.log(num_streams / (1.0 + self._get_number_of_streams_for_tag(tag_index)))
            idf_value.append(idf_value_for_a_tag)

        return idf_value

    def compute_tf_idf_for_streams(self, num_streams, num_tags, generate_file=False):
        """
         Computes the TF IDF values for tge streams and tags and returns a matrix of ||S|| * ||T|| dimension
        :param generate_file: If the output file needs to be generated
        :param num_streams: Number of streams
        :param num_tags: Number of tags
        :return: a matrix of ||S|| * ||T|| dimension
        """

        term_frequency_for_streams = self._get_term_frequency_for_streams(num_streams, num_tags)
        inverse_document_frequencies_for_tags = self._get_inverse_document_frequency_for_tags(num_streams, num_tags)
        tf_idf_values = []
        for stream_index in range(0, num_streams):
            tf_idf_values_current_row = term_frequency_for_streams[stream_index]
            for itr, _ in enumerate(tf_idf_values_current_row):
                tf_idf_values_current_row[itr] = tf_idf_values_current_row[itr] * inverse_document_frequencies_for_tags[itr]

            tf_idf_values.append(tf_idf_values_current_row)

        return tf_idf_values

    def _compute_cosine_similarity_between_lists(self, v1, v2):
        """
        Compute the Cosine similarity between 2 lists v1 and v2
        :param v1: The list V1
        :param v2: The list V2
        :return: The cosine similarity between the lists
        """
        # Convert to numpy float arrays
        v1 = np.array(v1).astype(np.float)
        v2 = np.array(v2).astype(np.float)

        # check if the denominator can be 0, the numerator is also 0
        if np.sum(v1 ** 2) == 0 or np.sum(v2 ** 2) == 0:
            return 0.0
        else:
            return np.dot(v1, v2) / (np.sqrt(np.sum(v1 ** 2)) * np.sqrt(np.sum(v2 ** 2)))

    def _generate_tfidf_files(self, tf_idf_values, tag_names, stream_ids, similar_streams_generated_file_location):
        """
        Generate the TF-IDF files for verifying the TF-IDF scores across the streams
        :param tf_idf_values: The matrix of of ||S|| * ||T|| dimension. List of lists.
        :param tag_names: An array of ||T|| size
        :param stream_ids: An array of ||S|| size
        :param similar_streams_generated_file_location: The complete location where the similar streams file will be generated
        :return: None
        """
        output_content = ",".join(tag_names) + NEWLINE

        # For each stream
        for idx, row in enumerate(tf_idf_values):
            # add the stream ID at the front
            output_content += str(stream_ids[idx]) + ","

            # cast row values to string
            row_str = [str(val) for val in row]

            # add the TF-IDF values for the various tags
            output_content += ",".join(row_str) + NEWLINE

        output_directory = os.path.dirname(similar_streams_generated_file_location)
        latest_tf_idf_file = self.get_latest_output_file_name(configurations.TF_IDF_FILE_NAME, next=True)[1]
        tfidf_output_file_location = os.path.join(output_directory, latest_tf_idf_file + ".csv")
        with open(tfidf_output_file_location, "w") as fw:
            fw.writelines(output_content)

        print("Generated file with TF-IDF values.")


    def compute_similarities_generate_similar_streams(self, stream_tag_frequency_location, similar_streams_generated_file_location):
        self.df = pd.read_csv(stream_tag_frequency_location, header = 0, index_col = 0)
        
        stream_tag_frequencies = None
        with open(stream_tag_frequency_location, "r") as fr:
            stream_tag_frequencies = [line.strip().split(",") for line in fr.readlines()]

        # The rows are the number of streams
        num_streams = self.df.shape[0]
        print("Num Streams: " + str(num_streams))

        # The columns are the number of tags
        num_tags = self.df.shape[1]
        print("Num tags: " + str(num_tags))

        tf_idf_values = self.compute_tf_idf_for_streams(num_streams, num_tags)

        # exclude the first row index as it says "StreamId"
        self._generate_tfidf_files(tf_idf_values, self.df.columns, self.df.index.values, similar_streams_generated_file_location)

        LOW_VALUE = 0
        
        nearest_neighbors_content = self._get_column_names()
        
        for stream_row_num in range(0, num_streams):
            stream_id = stream_tag_frequencies[stream_row_num+1][0]
            source_stream_tag_frequencies = tf_idf_values[stream_row_num][1:]
            nearest_neighbors_content += stream_id + ","
            # print("Source stream: " + stream_id)
            distances = []

            for other_stream_row_num in range(0, num_streams):
                # Get the required values from the other stream row
                other_stream_id = stream_tag_frequencies[other_stream_row_num+1][0]
                other_stream_tag_frequencies = tf_idf_values[other_stream_row_num][1:]
                # print("    Current stream: " + other_stream_id)

                if other_stream_row_num != stream_row_num:
                    distance = self._compute_cosine_similarity_between_lists(source_stream_tag_frequencies, other_stream_tag_frequencies)
                     # print("Distance: " + str(distance))
                    distances.append((other_stream_id, distance))
                else:
                    distances.append((other_stream_id, LOW_VALUE))

            idx = 0
            distances = sorted(distances, key=lambda x: x[1],reverse=True)
            # print distances
            for stream_id_distance_mapping in distances:
                if idx < num_nghbrs:
                    # print("Distance: " + str(stream_id_distance_mapping[1]))
                    nearest_neighbors_content += stream_id_distance_mapping[0] + ","
                    idx += 1
                else:
                    break

            nearest_neighbors_content += NEWLINE

#        print(nearest_neighbors_content)
        with open(similar_streams_generated_file_location, "w") as fw:
            fw.writelines(nearest_neighbors_content)
        print("Nearest neighbors using cosine distance generated...")