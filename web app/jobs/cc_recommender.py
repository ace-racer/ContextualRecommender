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
        try:
            # initialize the job
            self.LOG_HANDLE.info("Execution started for: %s", constants.CC_RECOMMENDER_NAME)
            job_id = utility.add_job(constants.CC_RECOMMENDER_NAME, self.LOG_HANDLE)
            if job_id >= 0:
                self.LOG_HANDLE.info("Running job with ID: %s", str(job_id))
                # Do some job...and set the job_status to stopped when required
                time.sleep(5)


        except Exception as e:
            self.LOG_HANDLE.error("An error occurred. Details: %s", str(e))
        finally:
            #final clean ups
            utility.update_job(job_id, {constants.STATUS_STR: job_status}, self.LOG_HANDLE, True)
            self.LOG_HANDLE.info("Job with Id %s completed.", str(job_id))



