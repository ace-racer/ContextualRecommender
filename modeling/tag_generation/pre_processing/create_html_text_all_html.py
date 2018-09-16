import pandas as pd
from bs4 import BeautifulSoup
import os
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

# configurations
FILES_LOCATION = "H:\\TeamStreamz_IW\\code\\data\\tag_generation_content"
input_location = os.path.join(FILES_LOCATION, "card_module_details_to_process.csv")
output_file = os.path.join(FILES_LOCATION, "card_module_details_content_extracted.csv")
# end of configurations

# constants
NEWLINE = "\n"
HTML_CONTENT_COLUMN_NAME = "HTML_CONTENT"
LANGUAGE_COLUMN_NAME = "LANGUAGE"
MODULE_NAME_COLUMN_NAME = "MODULENAME"
SHOULD_PROCESS = "SHOULD_PROCESS"
TEXTDETAILS = "TEXTDETAILS"
DECKID_COLUMN_NAME = "DECKID"

# end of constants


input_df = pd.read_csv(input_location, encoding="ISO-8859-1")
num_rows = input_df.shape[0]

input_df[HTML_CONTENT_COLUMN_NAME] = ""

for idx, row in input_df.iterrows():
    if row[SHOULD_PROCESS] == 1:
        if not pd.isnull(row[TEXTDETAILS]):
            source_data = row[TEXTDETAILS]
            source_data = source_data.replace("&nbsp;", " ")
            source_data = source_data.replace(u'\xa0', ' ')
            input_df.loc[idx, HTML_CONTENT_COLUMN_NAME] = striphtml(source_data)


input_df = input_df[input_df[SHOULD_PROCESS] == 1]
input_df[HTML_CONTENT_COLUMN_NAME] = input_df[HTML_CONTENT_COLUMN_NAME].replace('\n','', regex=True)
input_df.to_csv(output_file, index=False, encoding="ISO-8859-1")
print("Output file with the html text is generated.")
