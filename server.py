"""Server file for Shower Buddy"""

from flask import (Flask, render_template, request, flash, session, redirect) 
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
# app.secret.key = 'lola'  <-- **Figure out if/why this is needed!
app.jinja_env.undefined = StrictUndefined  # ** Review what the heck this is for


@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('/homepage.html')

@app.route('/about')
def about_app():
    """Take visitor to the About page"""

    return render_template('/about.html')


@app.route('/create_user')
def create_user():
    """Add a new user.
        Check if caregiver info already exists and make connection; 
        else create both objects """

    # , methods=['POST']
    # Lots of info from the forms to get and organize
    # Verify a user was added
    # "Start shower now?"

    return render_template('/create_user.html')


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


    # > Start
    #     >"Let's start by getting wet all over. Move under the spray, let the water
    #     get your hair all wet until it is fully soaked."
    #     >STEP ONE<  Retrieve info about step one (Action, Product, Image, Gif)
    #         >Time for the shampoo! 
    #         > Retrieve the shampoo (show bottle / color of label)  
    #         > Put some in your hand (show amount to user)
    #         > Now get that shampoo in your hair and scrub with your fingertips!
    #         > TIMER / SHOW gif/video of action while timer runs
    #             > End of timer: Are you done & ready to rinse?
    #                 > Y (next step) / N (extend timer) / HELP (call for CG. OR replay of instructions?)
    #         > TIMER / SHOW gif/video of action while timer runs
    #             > End of timer: Are you done & ready to rinse?
    #                 > Y (next step) / N (extend timer) / HELP (call for CG.)
    #     <STEP TWO< Retrieve info about step two (Action, Product, Image, Gif)
    #         >repeat of above with next product<


    return render_template('/start_shower.html')


if __name__ == "__main__":
    # connect_to_db(app)  <-- ** Figure out if you need something like this to function!
    app.run(host='0.0.0.0', debug=True)

