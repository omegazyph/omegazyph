"""
-------------------------------------------------------------------------
PROJECT  : Flask Request Handler
FILE     : Get_request.py
AUTHOR   : omegazyph
CREATED  : 04-15-24
UPDATED  : 12-30-2025
DESCRIPTION: A demonstration of handling different HTTP methods (GET/POST) 
             using the Flask web framework.
-------------------------------------------------------------------------
"""

from flask import Flask, request

# Creating the Flask application instance
app = Flask(__name__)

# --- ROUTE DEFINITIONS ---

@app.route("/")
def index():
    """
    Home Route: Dynamically detects and displays the HTTP method 
    used to access the page (usually GET).
    """
    return f"Method used: {request.method}"

@app.route("/bacon", methods=['GET', 'POST'])
def bacon():
    """
    Bacon Route: Handles both GET and POST requests.
    Useful for testing how servers respond to form submissions (POST)
    versus direct URL access (GET).
    """
    if request.method == 'POST':
        return "You are using POST"
    else:
        # Default behavior for standard browser navigation
        return "You are probably using GET"

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # Runs the local development server
    app.run(debug=True)