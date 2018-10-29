## A contextual recommender for an organization that wants to drive user engagement by suggesting relevant contents to the users of their app

### Project components
1. The data that is inside the data folder can be found here: https://drive.google.com/drive/u/0/folders/17PlasXUfiDhYC2eHyR8gWKZbl42moZMp
2. Refer here: http://jupyter.readthedocs.io/en/latest/install.html to understand the how to install Anaconda Python distribution and use Jupyter notebooks to execute the code
3. Python 3.6.3

### Description of the folders and contents
| # |	Folder name	| Description |
| --- | --- | --- |
| 1 | analysis | Contains scripts for initial data analysis of the input data files
| 2	| hybrid_recommender |	Contains the code to create the hybrid recommender combining content recommendations and collaborative filtering
| 3	| jupyter_notebooks |	Contains code to perform one-time exploration of the data before creating the recommendation systems
| 4	| modeling |	Contains the scripts for the various recommendation and filtering algorithms. Uses collaborative recommendation algorithms from [here](http://surpriselib.com/). Further details [here](https://github.com/ace-racer/ContextualRecommender/tree/master/modeling).
| 5	| web app |	Contains the Python [Flask](http://flask.pocoo.org/) application to show how the real-time recommendation experience will be. Further details [here](https://github.com/ace-racer/ContextualRecommender/tree/master/web%20app).
| 6	| nudge_framework |	The implementation of the Nudge framework which is used to send smart notifications for the available recommendations to the users.