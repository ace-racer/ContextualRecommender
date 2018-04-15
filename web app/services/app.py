from flask import Flask, request
from views_controller import views_controller
from recommendations_controller import recommender_controller
from content_controller import content_controller
from flask_cors import CORS

import constants


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to a Contextual recommender for TeamStreamz"

@app.route('/views/<userid>')
def getUserViews(userid):
    controller = views_controller()
    views = controller.get_contents_viewed_by_userid(userid)
    if views is not None:
        return views
    return "No views for the user yet"


@app.route('/views/add', methods=['POST'])
def addUserView():
    if request:
        content = request.get_json()

        view_details = {}
        for field in constants.content_view_fields:
            print(field)
            print(content.get(field, ""))
            view_details[field] = content.get(field, "")

        controller = views_controller()
        operation_result = controller.add_contents_viewed_by_user(view_details)
        if not operation_result[0]:
            return operation_result[1]
    return "OK"

@app.route('/streams/neighbors/<streamid>')
def getStreamDetails(streamid):
    if streamid:
        controller = recommender_controller()
        stream_details = controller.get_nearest_neighbors_by_streamid(streamid)
        if stream_details is None:
            return "No streams with the streamid {0}".format(streamid)
        return stream_details

@app.route('/streams/recommendations/<userid>')
def getUserRecommendations(userid):
    if userid:
        controller = recommender_controller()
        recommended_stream_details = controller.get_recommendations_for_user(userid)
        if recommended_stream_details is None:
            return "No streams recommended for the user with ID: {0}".format(userid)
        return recommended_stream_details


if __name__ == '__main__':
    app.run(debug=True)