## A contextual recommender for an organization that wants to drive user engagement by suggesting relevant contents to the users of their app

### Project components
1. The data that is inside the data folder can be found here: https://nusu.sharepoint.com/:f:/r/sites/IW_ContextualReco2/Shared%20Documents/Data/Sample?csf=1&e=MbgWYn
2. Refer here: http://jupyter.readthedocs.io/en/latest/install.html to understand the how to install Anaconda Python distribution and use Jupyter notebooks to execute the code

### Description of the Jupyter notebooks and the generated files
|	File name	| Description |	Source code | notebook file |
| --- | --- | --- | --- |
| 1 |	content_views_per_user.csv |	The number of times a stream is viewed by a user	| DataProcessor |
| 2	| content_views_per_user_scaled.csv |	The content views for the users scaled by MinMax transformation along the total number of views for the stream across all users. A 1 means that this user has watched the stream the most number of times	| DataProcessor |
| 3	| content_views_per_user_scaled_transposed.csv |	This is transpose of #2 for processing purpose	| DataProcessor |
| 4	| Users_with_roles_updated.csv | This contains the users CSV with the roles added from the available roles	| UserRoles |
| 5	| stream_tag_mapping_updated.csv |	This the stream tag mapping CSV with further tags added for some of the streams randomly as asked	| Stream_Tag_mapping |
| 6	| Tag_frequency_streams.csv	| This contains the streams with a 0/1 indicating whether a tag occurs for the stream	| Stream_tag_transformation |
| 7	| Nearest_neighbhor_streams.csv |	This contains the nearest neighbors for the specific stream	| Content_content_recommender |

### Please note
1. All data files will be stored in a folder named data that will be created in the same location as this repository
2. None of the data files will be committed to git since they can be of confidential nature
3. All source code that goes inside the master branch will be after a peer review has been completed to ensure that the application when built from source is stable
4. Please commit code only when there is a logical completion and add tests if applicable!
