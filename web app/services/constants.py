select_view_by_user_query = "SELECT userid, cardid, cardtitle, streamid, streamname, timestamp, moduleid, modulename from customer_card_view where userid = {0} order by cardid"
insert_view_by_user_query = "insert into customer_card_view(userid, cardid, streamid, moduleid, timestamp) values (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\");"

card_title_str = "cardtitle"
userid_str = "userid"
streamid_str = "streamid"
moduleid_str = "moduleid"
cardid_str = "cardid"
content_view_fields = [userid_str, streamid_str, moduleid_str, cardid_str]

date_format = "%d-%m-%Y %H:%M"

all_tags_table_name = "all_tags"
customer_card_view_table_name = "customer_card_view"
nearest_neighbors_streams_table_name = "nearest_neighbor_streams"
stream_details_table_name = "stream_details"
stream_tag_mapping_table_name = "stream_tag_mapping"
tag_frequency_streams = "tag_frequency_streams"