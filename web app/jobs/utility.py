import sqlite3
import json
import datetime

import constants
import configurations

def add_job(job_name, log_handle):
    conn = sqlite3.connect(configurations.OPERATIONS_DATBASE_LOCATION)
    try:
        c = conn.cursor()
        now = datetime.datetime.now()
        start_timestamp = now.strftime(constants.date_format)
        insert_query = "insert into job_status(name, start_time, status) values (\"{0}\", \"{1}\", \"{2}\");".format(job_name, start_timestamp, constants.STARTED_STATUS_STR)
        log_handle.info(insert_query)
        c.execute(insert_query)
        conn.commit()
        return True
    except Exception as e:
        log_handle.error("An error occurred while starting the job: %s", str(e))
        return False
    finally:
        conn.close()


def update_job(job_id, values):
    """
    :param job_id: The integer Job Id
    :param values: A dictionary of values that need to be updated
    :return: True, if the operation is a success
    """
    pass