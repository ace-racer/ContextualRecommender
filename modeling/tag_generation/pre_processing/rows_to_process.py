import pandas as pd
import os
import re

FILES_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\content"
SOURCE_FILE_NAME = "card_module_details.csv"
TARGET_FILE_NAME = "card_module_details_to_process.csv"

ENGLISH_IDENTIFIER = "EN_"

UTF_ERROR_PATTERN = "??"

SHOULD_PROCESS_ROW = "SHOULD_PROCESS"
LANGUAGE_COLUMN_NAME = "LANGUAGE"
MODULE_NAME_COLUMN_NAME = "MODULENAME"
URL_PATTERN = "([a-zA-Z0-9-_/])+\.[a-z\\n]+$"
TEXT_DETAILS_COLUMN_NAME = "TEXTDETAILS"

source_file_location = os.path.join(FILES_LOCATION, SOURCE_FILE_NAME)
input_df = pd.read_csv(source_file_location, encoding = "ISO-8859-1")
num_rows = input_df.shape[0]

is_english_initial_values = [1] * num_rows
input_df[SHOULD_PROCESS_ROW] = is_english_initial_values


for idx, row in input_df.iterrows():
    text_details = str(row[TEXT_DETAILS_COLUMN_NAME])
    
    # if text details is not empty
    if text_details:
        # if the text details corresponds to a URL
        if re.search(URL_PATTERN, text_details):
            print("{0} is a URL".format(text_details))
            input_df.loc[idx, SHOULD_PROCESS_ROW] = 0
        else: 
            if ENGLISH_IDENTIFIER not in row[LANGUAGE_COLUMN_NAME]:
                input_df.loc[idx, SHOULD_PROCESS_ROW] = 0
            else:
                if UTF_ERROR_PATTERN in text_details:
                    input_df.loc[idx, SHOULD_PROCESS_ROW] = 0
    else:
        input_df.loc[idx, SHOULD_PROCESS_ROW] = 0

target_file_location = os.path.join(FILES_LOCATION, TARGET_FILE_NAME)
input_df.to_csv(target_file_location, index=False, encoding = "ISO-8859-1")
print("Output file with the {0} column has been generated.".format(SHOULD_PROCESS_ROW))
