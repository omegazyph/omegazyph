from flask import Flask, request

app = Flask(__name__)


# Home page
@app.route("/")
def index():
    return "Method used %s" % request.method

@app.route("/bacon", methods=['GET','POST'])
def bacon():
    if request.method == 'POST':
        return "You are using POST"
    else:
        return "You are probaliy using GET"

if __name__ == "__main__":
    app.run()