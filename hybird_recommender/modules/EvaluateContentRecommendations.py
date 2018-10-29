import CombinedRecommender
import UserStreamViews
import ContentRecommender
import pandas as pd
import sys

stream_content_df = pd.read_csv("../data/stream_content_processed.csv", header=0, encoding="ISO-8859-1")

stream_views_df = pd.read_csv("../data/content_views_raw.csv", header=0)

# stream_views_df['TIMESTAMP'] = pd.to_datetime(stream_views_df['TIMESTAMP'], format="%Y-%m-%d %H:%M")
stream_views_df['TIMESTAMP'] = pd.to_datetime(stream_views_df['TIMESTAMP'], format="%d-%m-%Y %H:%M")

def show_recommended_streams(recommendations):
    recommended_streams = [x[0] for x in recommendations]
    print("Recommended streams:")
    print(recommended_streams)
    recommended_stream_content_df = stream_content_df[stream_content_df["StreamID"].isin(recommended_streams)]
    if recommended_stream_content_df.empty:
        print("Content for the recommended streams are not available")
    else:
        print(recommended_stream_content_df)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError("The first parameter is the stream id expected")

    streamid = int(sys.argv[1])
    
    recommended_stream_ids = ContentRecommender.get_similar_streams_based_on_history([streamid], ContentRecommender.constant)
    show_recommended_streams(recommended_stream_ids)

