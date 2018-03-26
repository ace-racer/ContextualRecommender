"""Contains the methods for CRUD operations with the customer views"""
import sqlite3
import json
import datetime

import constants
import configurations


class views_controller:
    """Contains methods for the CRUD operations on the views table"""


    def __init__(self):
        pass


    def get_contents_viewed_by_userid(self, userId):
        """
        Get the contents viewed by the user with the user Id
        :param userId: The userId of the user we are interested to see
        :return: list of the contents viewed by the user
        """
        if userId:
            print("UserId: " + userId)
            conn = sqlite3.connect(configurations.db_location)
            try:
                c = conn.cursor()
                c.execute(constants.select_view_by_user_query.format(userId))
                data = c.fetchall()
                return json.dumps(data)
            except Exception as e:
                print(e)
                return None
            finally:
                conn.close()

    def add_contents_viewed_by_user(self, card_view_details):
        """
        Create a new record in the user views table
        :param card_view_details: The details of the card that is viewed by the user
        :return: Whether the operation was a success
        """
        error_string = ""
        if card_view_details:
            userId = card_view_details.get(constants.userid_str, "")
            cardId = card_view_details.get(constants.cardid_str, "")
            print("UserId: " + userId)
            if userId and cardId:
                conn = sqlite3.connect(configurations.db_location)
                try:
                    c = conn.cursor()
                    moduleId = card_view_details.get(constants.moduleid_str, "")
                    streamId = card_view_details.get(constants.streamid_str, "")
                    now = datetime.datetime.now()
                    timestamp = now.strftime(constants.date_format)
                    query = constants.insert_view_by_user_query.format(userId, cardId, streamId, moduleId, timestamp)
                    print("Query: " + query)
                    c.execute(query)
                    conn.commit()
                    return True, error_string
                except Exception as e:
                    return False, str(e)
                finally:
                    conn.close()
            else:
                error_string = "Both user Id and card Id are required"

        return False, error_string