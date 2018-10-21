import ContentRecommender
import CollaborativeRecommender

from collections import defaultdict
def get_recommended_stream_ids(userid, stream_view_history, max_num_streams_required=5):
    
    userid = int(userid)
    similar_streams_based_on_history = ContentRecommender.get_similar_streams_based_on_history(stream_view_history)
    print("Similar streams based on history")
    print(similar_streams_based_on_history)
    
    streams_based_on_other_users = CollaborativeRecommender.get_similar_streams_based_on_other_users(userid)
    print("Similar streams based on other users")
    print(streams_based_on_other_users)

    c = defaultdict(lambda: 0)
    selection_reasoning = defaultdict(list)
    for similar_stream_history in similar_streams_based_on_history:
        c[int(similar_stream_history[0])] += similar_stream_history[1]
        selection_reasoning[int(similar_stream_history[0])].append("From content view {0}".format(round(similar_stream_history[1], 2)))
        
    for similar_stream_user in streams_based_on_other_users:
        c[int(similar_stream_user[0])] += similar_stream_user[1]
        selection_reasoning[int(similar_stream_user[0])].append("From similar users {0}".format(round(similar_stream_user[1], 2)))  
    
    count_values = [(k, c[k]) for k in c]
    count_values.sort(key=lambda x: x[1], reverse=True)
    
    return count_values[:min(len(count_values), max_num_streams_required)], selection_reasoning