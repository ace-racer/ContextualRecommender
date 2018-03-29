from base_operations import base_operations

from cc_recommender import cc_recommender


def schedule_operations():
    operation = cc_recommender()
    operation.perform_operation()


if __name__=="__main__":
    schedule_operations()