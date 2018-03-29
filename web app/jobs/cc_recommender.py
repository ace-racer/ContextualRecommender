from base_operations import base_operations

import constants
import utility

class cc_recommender(base_operations):
    def __init__(self):
        super(cc_recommender, self).__init__(constants.CC_RECOMMENDER_NAME)

    def perform_operation(self):
        try:
            self.LOG_HANDLE.info("Execution started for: %s", constants.CC_RECOMMENDER_NAME)
            add_status = utility.add_job(constants.CC_RECOMMENDER_NAME, self.LOG_HANDLE)
            if add_status:
                self.LOG_HANDLE.info("Running job")
        except Exception as e:
            self.LOG_HANDLE.error("An error occurred. Details: %s", str(e))