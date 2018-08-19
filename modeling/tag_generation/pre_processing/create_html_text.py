import pandas as pd
from bs4 import BeautifulSoup


# configurations
input_location = "/Users/shriyashekhar/Documents/IWork/IW-2/card_module_details_to_process.csv"
output_file = "/Users/shriyashekhar/Documents/IWork/IW-2/output_8.csv"
# end of configurations

# constants
NEWLINE = "\n"
HTML_CONTENT_COLUMN_NAME = "HTML_CONTENT"
LANGUAGE_COLUMN_NAME = "LANGUAGE"
MODULE_NAME_COLUMN_NAME = "MODULENAME"
SHOULD_PROCESS = "SHOULD_PROCESS"
TEXTDETAILS = "TEXTDETAILS"
# end of constants


input_df = pd.read_csv(input_location, encoding="ISO-8859-1")
num_rows = input_df.shape[0]

# is_english_initial_values = [1] * num_rows
input_df[HTML_CONTENT_COLUMN_NAME] = ""

for idx, row in input_df.iterrows():
    # print row[SHOULD_PROCESS]
    if row[SHOULD_PROCESS] == 1:
        # row[IS_ENGLISH_CONTENT_COLUMN_NAME] = False
        if not pd.isnull(row[TEXTDETAILS]):
            source_data = row[TEXTDETAILS]
            # print(row[TEXTDETAILS])
            soup = BeautifulSoup(source_data)
            if soup and soup.p:
                soup = soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
                soup = BeautifulSoup(soup.encode('ascii', 'ignore') )

                i = 0
                while i < len(soup.find_all('p')):
                    input_df.loc[idx, HTML_CONTENT_COLUMN_NAME] += soup.find_all('p')[i].text
                    # print i
                    # print soup.find_all('p')[i].text
                    i += 1


input_df[HTML_CONTENT_COLUMN_NAME] = input_df[HTML_CONTENT_COLUMN_NAME].replace('\n','', regex=True)
# target_file_location = os.path.join(FILES_LOCATION, TARGET_FILE_NAME)
input_df.to_csv(output_file, index=False, encoding="ISO-8859-1")
print("Output file with the html text is generated.")
