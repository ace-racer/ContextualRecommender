from flask import Flask, request
from views_controller import views_controller

import constants


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)