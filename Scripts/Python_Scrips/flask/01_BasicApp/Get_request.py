# Importing the Flask class and the request object from the flask module
from flask import Flask, request

# Creating a Flask application object with the name of the current module
app = Flask(__name__)

# Define routes and associated functions

# Route for the home page
@app.route("/")
def index():
    # Returns a response indicating the HTTP method used in the request
    return "Method used %s" % request.method

# Route for '/bacon' with GET and POST methods allowed
@app.route("/bacon", methods=['GET', 'POST'])
def bacon():
    # Check if the request method is POST
    if request.method == 'POST':
        return "You are using POST"
    else:
        return "You are probably using GET"

# Conditionally starts the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run()
