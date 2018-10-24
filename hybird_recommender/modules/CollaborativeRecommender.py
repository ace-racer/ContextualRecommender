import nltk
from nltk import FreqDist, word_tokenize
import string
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

content_views_per_user_scaled_df = pd.read_csv("../data/content_views_per_user_scaled.csv", header=0)
new_column_names = ["UserID"]
new_column_names.extend(content_views_per_user_scaled_df.columns[1:])
content_views_per_user_scaled_df.columns = new_column_names
# content_views_per_user_scaled_df.head()

features_df = content_views_per_user_scaled_df.drop("UserID", axis=1)
user_similarities = cosine_similarity(features_df.values)
user_similarities.shape

def get_similar_streams_based_on_other_users(current_user_id, max_similar_streams = 10, max_users_to_consider = 5):
    """
        current_user_id: The ID of the current user.
        max_similar_streams: The maximum number of similar streams to return
    max_users_to_consider: The maximum number of users to consider
    
    Returns: A list of stream IDs based on similar users who have watched the most
    
    """
    
    if current_user_id:
        userid_index = (content_views_per_user_scaled_df[content_views_per_user_scaled_df["UserID"] == current_user_id].index[0])
        similarity_current_user_other_users = user_similarities[userid_index]
        similarity_current_user_other_users = np.squeeze(similarity_current_user_other_users)
        #print(distance_current_user_other_users)
        
        user_ids = content_views_per_user_scaled_df["UserID"].values
        #print(type(user_ids))
        #print(user_ids.shape)
        #print(distance_current_user_other_users.shape)
        
        # concatenate the user ID and the similarity score sum as pairs
        user_similarity = list(zip(user_ids, similarity_current_user_other_users))
        
        #print(user_similarity)
        
        # sort the user similarity on the score in ascending order
        user_similarity.sort(key = lambda x: x[1], reverse=True)
        
        #print(user_similarity)
        
        # candidate users are those which are other users closest to the current user
        candidate_users = [x for x in user_similarity if (x[0] != current_user_id) and (x[1] > 0.6)]
        # print("Users the current user is most similar to: ")
        # print(candidate_users)
        
        num_candidate_users = len(candidate_users)
        candidate_users = candidate_users[:min(num_candidate_users, max_similar_streams)]
        #print(type(candidate_users[0]))
        
        # create an array of 0's equal to the number of columns other than UserID (# of streams)
        stream_views_sum = np.zeros(features_df.shape[1])
        
        # get the sum of the views
        for candidate_user in candidate_users:
            
            # weigh scores by similarity measure
            weight_factor = candidate_user[1]
            
            #print(weight_factor)
            stream_views_for_user = content_views_per_user_scaled_df[content_views_per_user_scaled_df["UserID"] == candidate_user[0]].values
            
            # remove the first column (UserID)
            stream_views_for_user = np.squeeze(stream_views_for_user)[1:]
            stream_views_for_user = np.array(stream_views_for_user)
            stream_views_sum = stream_views_sum + (weight_factor * stream_views_for_user)
        
        
        stream_ids = features_df.columns
        
        # concatenate the stream ID and the view score sum as pairs
        streams_with_sum_views = list(zip(stream_ids, stream_views_sum))
        
        
        # sort the stream views on the sum in descending order
        streams_with_sum_views.sort(key = lambda x: x[1], reverse = True)
        
        # print(streams_with_sum_views)
        
        # candidate streams are those which have greater than 0 views
        candidate_streams = [x for x in streams_with_sum_views if (x[1] > 0)]
        
        num_candidate_streams = len(candidate_streams)

        if num_candidate_streams == 0:
            # print("There are no candidate streams based on similar users")
            return None
        
        return candidate_streams[:min(num_candidate_streams, max_similar_streams)]
            
        
            
