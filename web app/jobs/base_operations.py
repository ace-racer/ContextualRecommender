"""Methods for logging and error handling"""
import logging
import os

import configurations
import constants

class base_operations:
    def __init__(self, source_name):
        self.LOG_HANDLE = self.set_logging_parameters(configurations.LOG_LEVEL, source_name)

    def set_logging_parameters(self, log_level, source_name):
        logger = logging.getLogger(source_name)
        log_file_path = os.path.join(configurations.log_file_folder_location, source_name + constants.LOG_FILE_EXTENSION)
        hdlr = logging.FileHandler(log_file_path)
        formatter = logging.Formatter(configurations.log_pattern)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(log_level)
        return logger

    def perform_operation(self):
        pass