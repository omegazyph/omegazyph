#imports
from flask import Flask

# name of the app
app = Flask(__name__)


# Start a web page
@app.route("/")
def index():
    return "Hompage"


# run the app
if __name__=="__main__":
    app.run()