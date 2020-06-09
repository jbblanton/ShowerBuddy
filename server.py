"""Server file for Shower Buddy"""

from flask import (Flask, render_template, request, flash, session, redirect) 
import crud
from jinja2 import StrictUndefined
from model import connect_to_db

app = Flask(__name__)

app.secret_key = 'lola'
app.jinja_env.undefined = StrictUndefined  




@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('/homepage.html')


# This will be turned into a toggle button to allow ABOUT to show up 
# on main pg with a click
@app.route('/about')
def about_app():
    """Take visitor to the About page"""

    return render_template('/about.html')


@app.route('/create_user')
def create_user():
    """Go to new user form """

    return render_template('/create_user.html')




@app.route('/create_user', methods=["POST"])
def register_user():
    """Add a new user.
        Check if caregiver info already exists and make connection; 
        else create both objects """

    # create a caregiver:
    cg_email = request.form.get('caregiver-email')
# If cg_email already in system, need to divert to adding an addtl user, not creating 2 accounts
    cg_pass = request.form.get('caregiver-password')
    cg_phone = request.form.get('caregiver-phone')

    caregiver = crud.create_caregiver(cg_email, cg_phone, cg_pass)

    session["cg_email"] = cg_email


    # create a user profile:
    user_name = request.form.get('user-name')
    user_body = request.form.get('body')

    new_user = crud.create_user(user_name, user_body, caregiver)


    # get the list of associated users for display on the start_shower page:
    users = crud.get_user_by_caregiver(caregiver=caregiver)
    print(users)

    return render_template('/start_shower.html', users=users)


@app.route('/login', methods=['POST'])
def log_in():
    """Log in a caregiver.
        Render P3 (choose user / start shower) """

    pass


@app.route('/start_shower')
def choose_flow():
    """Display users and their shower flows.
        Only associated user(s) will display.
        Caregiver will be able to select and start a flow"""

    users = crud.get_user_by_caregiver()

    return render_template('start_shower', users=users)


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
    connect_to_db(app)  
    app.run(host='0.0.0.0', debug=True)

