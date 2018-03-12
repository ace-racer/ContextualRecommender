select_view_by_user_query = "SELECT userid, cardid, cardtitle, streamid, streamname, timestamp, moduleid, modulename from customer_card_view where userid = {0} order by cardid"
insert_view_by_user_query = "insert into customer_card_view(userid, cardid, streamid, moduleid, timestamp) values (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\");"

card_title_str = "cardtitle"
userid_str = "userid"
streamid_str = "streamid"
moduleid_str = "moduleid"
cardid_str = "cardid"
content_view_fields = [userid_str, streamid_str, moduleid_str, cardid_str]

date_format = "%d-%m-%Y %H:%M"