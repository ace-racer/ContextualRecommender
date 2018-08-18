import pandas as pd
import os

FILES_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\content"
SOURCE_FILE_NAME = "card_module_details.csv"
TARGET_FILE_NAME = "card_module_details_with_eng.csv"

ENGLISH_IDENTIFIER = "EN_"

OTHER_LANGUAGE_IDENTIFIERS = ["JP-"]

IS_ENGLISH_CONTENT_COLUMN_NAME = "Is English Content"
LANGUAGE_COLUMN_NAME = "LANGUAGE"
MODULE_NAME_COLUMN_NAME = "MODULENAME"

source_file_location = os.path.join(FILES_LOCATION, SOURCE_FILE_NAME)
input_df = pd.read_csv(source_file_location)
num_rows = input_df.shape[0]

is_english_initial_values = [True] * num_rows
input_df[IS_ENGLISH_CONTENT_COLUMN_NAME] = is_english_initial_values

for _, row in input_df.iterrows():
    if ENGLISH_IDENTIFIER not in row[LANGUAGE_COLUMN_NAME]:
        row[IS_ENGLISH_CONTENT_COLUMN_NAME] = False
    else:
        for other_language_identifier in OTHER_LANGUAGE_IDENTIFIERS:
            if other_language_identifier in row[MODULE_NAME_COLUMN_NAME]:
                 row[IS_ENGLISH_CONTENT_COLUMN_NAME] = False

target_file_location = os.path.join(FILES_LOCATION, TARGET_FILE_NAME)
input_df.to_csv(target_file_location, index=False)
print("Output file with the Is English content generated.")
