#imports
from flask import Flask

# start of the app
app = Flask(__name__)

# @ sinifies a decorator - way to wrap a function and modifying its behavior
#the webpages
@app.route('/')
def index():
    return 'This is the home page'


# to start the app on 127.0.0.1:5000
if __name__ == "__main__":
    app.run()