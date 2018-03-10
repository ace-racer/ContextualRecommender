from flask import Flask,jsonify
from views_controller import views_controller


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


if __name__ == '__main__':
    app.run(debug=True)