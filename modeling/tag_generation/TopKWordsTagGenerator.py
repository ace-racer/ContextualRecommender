import math
import pandas as pd
import numpy as np
import os

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
            content = content.lower()

            # only select non-punctuation marks (loses - which connects words)
            tokenizer = RegexpTokenizer(r'\w+')
            
            word_tokens = tokenizer.tokenize(content)
            
            filtered_content_list = [w for w in word_tokens if not w in stop_words and w != ""]
            if configurations.GENERATE_WORD_CLOUD_FOR_STREAMS:
                if not os.path.exists(configurations.WORD_CLOUD_FOLDER_NAME):
                    os.makedirs(configurations.WORD_CLOUD_FOLDER_NAME)
                
                self.generate_word_cloud(k, filtered_content_list)

            top_k_most_common = Counter(filtered_content_list).most_common(self.TOP_K_K_VALUE)
            
            # Add the top K most common words as tags
            for item in top_k_most_common:
                stream_id_tag_list.append((str(k), str(item[0])))

        self.create_stream_tag_mapping_file(stream_id_tag_list)

    def generate_word_cloud(self, stream_id, filtered_content_list):
        if filtered_content_list:
            filtered_content = " ".join(filtered_content_list)

            # Refer sample here: https://github.com/amueller/word_cloud/blob/master/examples/simple.py
            wordcloud = WordCloud(max_font_size=40).generate(filtered_content)
            plt.figure()
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            complete_location = os.path.join(configurations.WORD_CLOUD_FOLDER_NAME, str(stream_id) + "." + constants.WORDCLOUD_FILE_EXTENSION)
            plt.savefig(complete_location)




