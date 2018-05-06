import math
import pandas as pd
import numpy as np

import configurations
import constants

NEWLINE = "\n"
knn_columns_to_select = configurations.COLUMNS_TO_SELECT
num_nghbrs = configurations.NUM_SIMILAR_STREAMS

class cosine_similarity:
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
        :param num_streams:
        :param num_tags:
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


    def compute_similarities_generate_similar_streams(self, stream_tag_frequency_location, similar_streams_generated_file_location):
        self.df = pd.read_csv(stream_tag_frequency_location, header = 0, index_col = 0)

        # The rows are the number of streams
        num_streams = self.df.shape[0]
        print("Num Streams: " + str(num_streams))

        # The columns are the number of tags
        num_tags = self.df.shape[1]
        print("Num tags: " + str(num_tags))

        tf_idf_values = self.compute_tf_idf_for_streams(num_streams, num_tags)

        # print(tf_idf_values)
        nearest_neighbors_content = self._get_column_names()
        cosine_similarity_values = []
        for stream_row_num in range(0, num_streams):
            cosine_similarity_current_stream = []
            for other_stream_row_number in range(0, num_streams):
                cosine_similarity_value = self._compute_cosine_similarity_between_lists(tf_idf_values[stream_row_num], tf_idf_values[other_stream_row_number])
                cosine_similarity_current_stream.append(cosine_similarity_value)
            cosine_similarity_values.append(cosine_similarity_current_stream)

        print(cosine_similarity_values)
        print("Nearest neighbors using cosine distance generated...")