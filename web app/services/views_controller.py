"""Contains the methods for CRUD operations with the customer views"""
import sqlite3
import json

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
            conn = sqlite3.connect(configurations.views_db_location)
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