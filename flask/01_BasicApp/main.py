#imports
from flask import Flask

# start of the app
app = Flask(__name__)

# @ sinifies a decorator - way to wrap a function and modifying its behavior
#the webpages
@app.route('/')
def index():
    return 'This is the home page'

@app.route('/tuna')
def tuna():
    return'<h2>Tuna is good</h2>'


@app.route('/profile/<username>')
def profile(username):
    return "Hey there %s" %username

@app.route('/post/<int:post_id>')
def post(post_id):
    return "<h2>Post ID is %s</h2>" %post_id


# to start the sever
if __name__ == "__main__":
    app.run(debug=True)