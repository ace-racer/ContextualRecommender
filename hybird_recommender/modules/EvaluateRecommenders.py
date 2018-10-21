import CombinedRecommender
import UserStreamViews
import pandas as pd
import sys

stream_content_df = pd.read_csv("../data/stream_content.csv", header=0, encoding="ISO-8859-1")

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
        raise ValueError("The first parameter is the user id expected")

    userid = int(sys.argv[1])
    recent_viewed_streams = UserStreamViews.get_latest_streams_for_user(stream_views_df, userid)
    print(recent_viewed_streams)
    recent_viewed_stream_ids = [x[0] for x in recent_viewed_streams]
    print("recent viewed streams...")
    print(recent_viewed_stream_ids)
    recommended_stream_ids, selection_reasoning = CombinedRecommender.get_recommended_stream_ids(userid, recent_viewed_stream_ids)
    show_recommended_streams(recommended_stream_ids)
    print(selection_reasoning)

