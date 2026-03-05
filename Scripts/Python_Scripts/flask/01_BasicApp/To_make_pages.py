# Imports the Flask class from the flask module
from flask import Flask

# Creates a Flask application object with the name of the current module
app = Flask(__name__)

# Decorators are used to define routes in Flask.
# When a request is made to the specified route, the associated function is called.

# Defines a route for the home page '/'
@app.route('/')
def index():
    return 'This is the home page'

# Defines a route for '/tuna'
@app.route('/tuna')
def tuna():
    return '<h2>Tuna is good</h2>'

# Defines a dynamic route '/profile/<username>'
# <username> is a variable that will be passed to the profile function
@app.route('/profile/<username>')
def profile(username):
    return "Hey there %s" % username

# Defines a dynamic route '/post/<int:post_id>'
# <post_id> is a variable that will be passed as an integer to the post function
@app.route('/post/<int:post_id>')
def post(post_id):
    return "<h2>Post ID is %s</h2>" % post_id

# Conditionally starts the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run()
