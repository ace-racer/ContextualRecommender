import math
import pandas as pd
import numpy as np
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

import configurations
import constants
from base_operations import base_operations
from tag_generation.TagGeneratorBase import TagGeneratorBase

class TopKWordsTagGenerator(TagGeneratorBase):
    def __init__(self):
        self.TOP_K_K_VALUE = 5
        print("The Top K words tag generator will be used with K = " + str(self.TOP_K_K_VALUE))

    def generate_tags(self):
        complete_stream_details_dict = self.get_stream_details()
        stream_id_tag_list = []

        # Below snippets are partially taken from: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
        # get the stop words
        stop_words = set(stopwords.words('english'))

        for k in complete_stream_details_dict:
            content = complete_stream_details_dict[k]
            word_tokens = word_tokenize(content)
            filtered_content = [w for w in word_tokens if not w in stop_words]
            top_k_most_common = Counter(filtered_content).most_common(self.TOP_K_K_VALUE)
            
            # Add the top K most common words as tags
            for item in top_k_most_common:
                stream_id_tag_list.append((str(k), str(item[0])))

        self.create_stream_tag_mapping_file(stream_id_tag_list)



