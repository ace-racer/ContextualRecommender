"""Methods for logging and error handling"""
"""Copied from the version in jobs"""

import logging
import os
import re

import configurations
import constants

FILE_NUMBER_PATTERN = "_([0-9]+).csv$"

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

    def get_latest_output_file_name(self, file_name_pattern):
        """
        Get the name of the latest output file name
        :param file_name_pattern: The pattern expected in the output file
        :return: A tuple where the first element is the number of the output file and the second is the complete file name with the number
        """

        if file_name_pattern:
            largest_output_file_number = 0
            for item in os.listdir(configurations.OUTPUT_FILES_DIRECTORY):
                if os.path.isfile(os.path.join(configurations.OUTPUT_FILES_DIRECTORY, item)) and file_name_pattern in item:
                    # search if the file number pattern is present in the current file
                    if re.search(FILE_NUMBER_PATTERN, item):
                        current_file_number = int(re.findall(FILE_NUMBER_PATTERN, item)[0])
                        if current_file_number > largest_output_file_number:
                            largest_output_file_number = current_file_number

            next_file_number = largest_output_file_number + 1
            return next_file_number, file_name_pattern + constants.UNDERSCORE_STR + str(next_file_number) + constants.CSV_FILE_EXTENSION
