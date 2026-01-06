# Importing necessary modules from the Flask library
from flask import Flask, render_template

# Creating a Flask application object with the name of the current module
app = Flask(__name__)

# Define routes and associated functions

# Route for the home page and a dynamic route that accepts a username
@app.route("/")
@app.route("/<user>")
def user(user=None):
    # Renders the template 'user.html' and passes the 'user' variable to it
    return render_template("user.html", user=user)

# Conditionally starts the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run()
