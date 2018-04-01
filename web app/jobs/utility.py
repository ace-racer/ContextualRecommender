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

        # get the row ID
        c.execute(constants.LAST_ROWID_QUERY)
        query_results = c.fetchall()
        job_id = query_results[0][0]
        print(job_id)
        return job_id
    except Exception as e:
        log_handle.error("An error occurred while starting the job: %s", str(e))
        return -1
    finally:
        conn.close()


def update_job(job_id, values, log_handle, end_job = False):
    """
    :param job_id: The integer Job Id
    :param values: A dictionary of values that need to be updated
    :return: True, if the operation is a success
    """
    if job_id < 0:
        return False

    update_query = "update job_status set {0} where id = {1}"
    update_str = ""

    if end_job:
        now = datetime.datetime.now()
        end_timestamp = now.strftime(constants.date_format)
        values["end_time"] = end_timestamp

    for k, v in values.items():
        update_str += "{0} = \"{1}\",".format(k, v)

    # remove the last ,
    update_str_no_last_comma = update_str[:-1]

    update_query_updated = update_query.format(update_str_no_last_comma, job_id)
    conn = sqlite3.connect(configurations.OPERATIONS_DATBASE_LOCATION)
    try:
        c = conn.cursor()
        log_handle.info(update_query_updated)
        c.execute(update_query_updated)
        conn.commit()
        return True
    except Exception as e:
        log_handle.error("An error occurred while updating the job: %s", str(e))
        return False
    finally:
        conn.close()


def get_num_records_to_process(table_name, log_handle):
    if table_name:
        count_processed_query_str = "select count(processed) from {0} where processed = 0".format(table_name)
        conn = sqlite3.connect(configurations.CONTENT_DATABASE_LOCATION)
        try:
            c = conn.cursor()
            c.execute(count_processed_query_str)
            count_results = c.fetchall()
            if count_results and count_results[0]:
                return count_results[0][0]
            return 0
        except Exception as ex:
            log_handle.error("An error occurred: " + str(ex))
            return 0
        finally:
            conn.close()



