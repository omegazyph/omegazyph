#imports
from flask import Flask, render_template

# new files 
#static (files the never change like css)
#Templates (for html files)



# name of the app
app = Flask(__name__)


# Start a web page
@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name=name) # looks for profile.html in Templates


# run the app
if __name__=="__main__":
    app.run()