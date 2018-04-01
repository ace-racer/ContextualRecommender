from base_operations import base_operations

import constants
import utility
import time

class cc_recommender(base_operations):
    def __init__(self):
        super(cc_recommender, self).__init__(constants.CC_RECOMMENDER_NAME)

    def perform_operation(self):
        job_status = constants.ERROR_STATUS_STR
        job_id = -1
        new_streams_to_process = 0
        error_str = ""
        try:
            # initialize the job
            self.LOG_HANDLE.info("Execution started for: %s", constants.CC_RECOMMENDER_NAME)
            job_id = utility.add_job(constants.CC_RECOMMENDER_NAME, self.LOG_HANDLE)
            if job_id >= 0:
                self.LOG_HANDLE.info("Running job with ID: %s", str(job_id))

                # check if there are new streams that have been added
                new_streams_to_process = utility.get_num_records_to_process(constants.stream_details_table_name, self.LOG_HANDLE)
                if new_streams_to_process > 0:
                    self.LOG_HANDLE.info("There are {0} streams to process".format(str(new_streams_to_process)))
                    # Do some job...and set the job_status to stopped when required
                    time.sleep(5)
                    job_status = constants.STOPPED_STATUS_STR
                else:
                    self.LOG_HANDLE.info("There are no streams to process...")
                    job_status = constants.STOPPED_STATUS_STR
        except Exception as e:
            error_str = str(e)
            self.LOG_HANDLE.error("An error occurred. Details: %s", error_str)
            job_status = constants.ERROR_STATUS_STR
        finally:
            #final clean ups
            utility.update_job(job_id, {constants.STATUS_STR: job_status, constants.RECORDS_PROCESSED_STR: str(new_streams_to_process), constants.OTHER_DETAILS_STR: error_str}, self.LOG_HANDLE, True)
            self.LOG_HANDLE.info("Job with Id %s completed.", str(job_id))



