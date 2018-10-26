import nltk
from nltk import FreqDist, word_tokenize
import string
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

stream_content_df = pd.read_csv("../data/stream_content_processed.csv", header=0, encoding="ISO-8859-1")

def preprocess(tokens):
    
    # TODO: remove random sequences that contain with more than one caps and small or combination of letters and numbers
    
    tokens_nop = [t for t in tokens if t not in string.punctuation]
    tokens_nop = [t.lower() for t in tokens_nop]
    wnl = nltk.WordNetLemmatizer()
    stop = stopwords.words('english')
    tokens_nostop = [t for t in tokens_nop if t not in stop]
    tokens_lem = [wnl.lemmatize(t) for t in tokens_nostop]
    tokens_clean = [t for t in tokens_lem if len(t) >= 3] 
    return tokens_clean

stream_content_df['Content_processed'] = stream_content_df['Content'].map(word_tokenize)
stream_content_df['Content_processed'] = stream_content_df.Content_processed.apply(preprocess)
#stream_content_df.head()

stream_content_df['Content_processed'] = stream_content_df['Content_processed'].apply(lambda x: " ".join(x))
#stream_content_df.head()

all_streams_cleaned_text = stream_content_df['Content_processed']
all_streams_tfidf_vectorizer = TfidfVectorizer(min_df = 2)
all_streams_tfidf = all_streams_tfidf_vectorizer.fit_transform(all_streams_cleaned_text)
#all_streams_tfidf

token_values = {all_streams_tfidf_vectorizer.vocabulary_[token]: token for token in all_streams_tfidf_vectorizer.vocabulary_}


similarities = cosine_similarity(all_streams_tfidf)

def linear(x, total_steps):
    step_value = 1/total_steps
    return 1 - (x * step_value)

def constant(x, total_steps):
    return 1

def get_similar_streams_based_on_history(viewed_streams, weight_pattern = linear, max_similar_streams = 10, max_viewed_streams_to_consider = 5):
    """
        viewed_streams: list of stream IDs that have been viewed by the current user. The streams at a lower ID has been viewed more recently. So stream with ID 0 is the last viewed stream.
        weight_pattern: The weight pattern to weight the contributions due to the stream history
    max_similar_streams: The maximum number of similar streams to return
    max_viewed_streams_to_consider: The maximum number of viewed streams to consider for the recommendation 
    
    Returns: A list of stream ID, score pairs
    
    """
    
    if viewed_streams:
        num_viewed_streams = len(viewed_streams)
        
        # set the max viewed streams to consider 
        max_viewed_streams_to_consider = min(max_viewed_streams_to_consider, num_viewed_streams)
        
        # create an array of 0's
        similarity_sum = np.zeros(similarities.shape[0])
    
        for x, viewed_stream in enumerate(viewed_streams):
            if not stream_content_df[stream_content_df["StreamID"]==viewed_stream].empty:
                stream_index = stream_content_df[stream_content_df["StreamID"]==viewed_stream].index[0]
                weight_factor = weight_pattern(x, max_viewed_streams_to_consider)
                # print(weight_factor)
                similarity_sum = similarity_sum + (weight_factor * np.array(similarities[stream_index]))
        
        
        #print(similarity_sum)
        stream_ids = stream_content_df["StreamID"]
        
        # concatenate the stream ID and the similarity score sum as pairs
        stream_similarity = list(zip(stream_ids, similarity_sum))
        
        # print(stream_similarity)
        
        # sort the stream similarity on the score in descending order
        stream_similarity.sort(key = lambda x: x[1], reverse = True)
        
        # print(stream_similarity)
        
        # candidate streams are those which have greater than 0 score and they have not been viewed before
        candidate_streams = [x for x in stream_similarity if (x[1] > 0) and (x[0] not in viewed_streams)]
        
        num_candidate_streams = len(candidate_streams)

        if num_candidate_streams == 0:
            # print("None of the streams in history have their content available")
            return None
        
        return candidate_streams[:min(num_candidate_streams, max_similar_streams)]
            
            