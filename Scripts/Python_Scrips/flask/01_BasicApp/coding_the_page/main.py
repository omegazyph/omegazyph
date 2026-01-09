# Imports necessary modules from Flask library
from flask import Flask, render_template

# Name of the Flask application, '__name__' refers to the current module
app = Flask(__name__)

# Defines a route '/profile/<name>' where '<name>' is a variable
# When a request is made to this route, the function below is executed
@app.route("/profile/<name>")
def profile(name):
    # Renders the template 'profile.html' and passes the 'name' variable to it
    return render_template("profile.html", name=name)

# Runs the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run()
