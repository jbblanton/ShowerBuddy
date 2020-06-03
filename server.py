"""Server file for Shower Buddy"""

from flask import (Flask, render_template, request, flash, session, redirect) 
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
# app.secret.key = 'lola'
app.jinja_env.undefined = StrictUndefined
# ** Review what the heck this is for


@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('/homepage.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    """Add a new user.
        Check if caregiver info already exists and make connection; 
        else create both objects """

    pass

    # Lots of info from the forms to get and organize
    # Verify a user was added
    # "Start shower now?"


@app.route('/login', methods=['POST'])
def log_in():
    """Log in a caregiver.
        Render P3 (choose user / start shower) """

    pass


@app.route('/start_shower')
def play_shower():
    """Play the shower flow.
        Will need user_id / flow_id

        Add connection for the SOS button?
        Event listener for Snooze and Next buttons """

    pass


if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

