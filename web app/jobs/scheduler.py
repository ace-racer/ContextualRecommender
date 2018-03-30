from base_operations import base_operations
from cc_recommender import cc_recommender
import configurations

import schedule
import time
import constants


def schedule_operations():
    operation = cc_recommender()
    schedule.every(1).minutes.do(operation.perform_operation)


if __name__=="__main__":
    schedule_operations()

    print(constants.JOB_SCHEDULER_NAME)

    while True:
        schedule.run_pending()
        time.sleep(configurations.POLLING_INTERVALS)