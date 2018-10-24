import pandas as pd
import numpy as np
from collections import Counter


def get_latest_streams_for_user(stream_views_df, userid, max_views_to_consider = 25, max_num_unique_streams = 5):
    
    """
        Get a dictionary of the streams with their views that were viewed most recently by the user
    """
    
    # sort the streams views in descending order by time
    # print(stream_views_df.head())
    stream_views_df = stream_views_df.sort_values(by="TIMESTAMP", ascending=False)
    stream_views_for_user_df = stream_views_df[stream_views_df["USERID"] == userid]
    
    streams_viewed = np.array(stream_views_for_user_df["STREAMID"])
    
    num_streams_viewed = len(streams_viewed)
    
    recent_stream_views = streams_viewed[:min(max_views_to_consider, num_streams_viewed)]
    
    stream_counts = Counter(recent_stream_views)
    
    num_unique_streams = min(max_num_unique_streams, len(stream_counts))

    if num_unique_streams == 0:
        raise ValueError("No views for the user with the ID: {0}".format(userid))

    return stream_counts.most_common(num_unique_streams)