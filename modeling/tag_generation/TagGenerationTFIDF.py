import nltk
import string
from nltk.corpus import stopwords
import pandas as pd
import numpy as np

import configurations
import constants
from base_operations import base_operations
from tag_generation.TagGeneratorBase import TagGeneratorBase
from sklearn.feature_extraction.text import TfidfVectorizer



class TagGenerationTFIDF(TagGeneratorBase):
    def __init__(self):
        print("The TFIDF tag generator will be used." )
        TagGeneratorBase.__init__(self)
        self._stop = stopwords.words('english')
        self._snowball = nltk.SnowballStemmer('english')

    def _preprocess(self, toks):
        toks = [ t.lower() for t in toks if t not in string.punctuation ]
        toks = [t for t in toks if t not in self._stop ]
        toks = [ self._snowball.stem(t) for t in toks ]
    #   toks = [ wnl.lemmatize(t) for t in toks ]
        toks_clean = [ t for t in toks if len(t) >= 3 ]
        return toks_clean

    def generate_tags(self):
        complete_stream_details_dict = self.get_stream_details()
        all_streams_cleaned_tokens = []
        stream_ids = []
        for stream_id in complete_stream_details_dict:
            stream_ids.append(stream_id)
            stream_content = complete_stream_details_dict[stream_id]
            stream_content_tokens = nltk.word_tokenize(stream_content)
            stream_cleaned_tokens = self._preprocess(stream_content_tokens)
            all_streams_cleaned_tokens.append(stream_cleaned_tokens)

        all_streams_cleaned_text = [ ' '.join(f) for f in all_streams_cleaned_tokens ]

        # And tfidf indexing
        all_streams_tfidf_vectorizer = TfidfVectorizer(min_df = 2)
        all_streams_tfidf = all_streams_tfidf_vectorizer.fit_transform(all_streams_cleaned_text)

        token_values = {all_streams_tfidf_vectorizer.vocabulary_[token]: token for token in all_streams_tfidf_vectorizer.vocabulary_}

        all_streams_tfidf_coo = all_streams_tfidf.tocoo()

        # create a dictionary indexed by the stream (row) number
        token_tfidf_dict = {}
        for idx, stream_index in enumerate(all_streams_tfidf_coo.row):
            stream_id = stream_ids[stream_index]
            #print("Stream index: {0} and stream ID: {1}".format(stream_index, stream_id))
            if token_tfidf_dict.get(stream_id):
                token_tfidf_dict[stream_id].append((all_streams_tfidf_coo.col[idx], all_streams_tfidf_coo.data[idx]))
            else:
                token_tfidf_dict[stream_id] = [(all_streams_tfidf_coo.col[idx], all_streams_tfidf_coo.data[idx])]

        for k in token_tfidf_dict:
            num_tokens = min(configurations.NUM_TAGS_TO_GENERATE, len(token_tfidf_dict[k]))
            top_k_token_ids = sorted(token_tfidf_dict[k], key=lambda x: x[1], reverse=True)[: num_tokens]
            top_k_tokens = [token_values[token_index] for token_index, tfidf_score in top_k_token_ids]
            token_tfidf_dict[k]= top_k_tokens

        stream_id_tag_list = []
        for stream_id in token_tfidf_dict:
            for tag in token_tfidf_dict[stream_id]:
                stream_id_tag_list.append((stream_id, tag))

        self.create_stream_tag_mapping_file(stream_id_tag_list)
        
