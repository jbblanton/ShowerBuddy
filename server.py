"""Server file for Shower Buddy"""

from flask import (Flask, render_template, request, flash, session, redirect) 
import crud
from jinja2 import StrictUndefined
from model import (db, connect_to_db, User, Client)
from flask_login import (LoginManager, login_user, login_required, logout_user)



app = Flask(__name__)

app.secret_key = 'lola'
app.jinja_env.undefined = StrictUndefined  

### For using the flask_login tools:
login_manager = LoginManager()
login_manager.init_app(app)



### App Routes:
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
def render_create_user_page():
    """Go to new user form """

    return render_template('/create_user.html')


@app.route('/create_user', methods=["POST"])
def register_user():
    """Add a new user.
        Check if caregiver info already exists and make connection; 
        else create both objects """

    # create a caregiver:
    cg_email = request.form.get('caregiver-email')
    cg_pass = request.form.get('caregiver-password')
    cg_phone = request.form.get('caregiver-phone')

    cg = User.check_if_registered(cg_email)
    print('Here is the Caregiver')
    print(cg)
    if cg:
# The flash didn't happen, just the redirect; Maybe stop redirect and put a 
#   button to the log in page? 
        flash('There is already an account with this email. Please try again, or else Please log in')
        return '<h3>There is already an account with this email. Please try again, or else log in on the homepage.</h3>'
    else:
        caregiver = crud.create_caregiver(cg_email, cg_phone, cg_pass)
        session["cg_email"] = cg_email
    # create a user profile:
        user_name = request.form.get('user-name')
        user_body = request.form.get('body')
        new_user = crud.create_client(user_name, user_body, caregiver)
# get the list of associated users for display on the start_shower page:
        users = crud.get_client_by_caregiver(caregiver=caregiver)
    print('Here is the client')
    print(users)
    return render_template('/start_shower.html', users=users)


@app.route('/login')
def render_log_in_page():
    """Render the page where a caregiver can log in."""

    return render_template('/homepage.html')


# @app.route('/login', methods=["POST"])
# def log_in_user():
#     """"Log in an existing caregiver"""

#     email = request.form.get('caregiver-email')
#     password = request.form.get('caregiver-password')
#     caregiver = crud.get_caregiver_by_email(email)

#     if email == caregiver.email and password == caregiver.password:
#         flash('Successfully logged in!')
# # Pretty sure the flash won't work. Whatever happened to our 3 page app??
#         session["cg_email"] = caregiver.email
# # Pretty sure this should change to caregiver ID. Need to check in on this
#         users = crud.get_user_by_caregiver(caregiver=caregiver)
#         return render_template('/start_shower.html', users=users)
#     else: 
#         flash('Could not log in. Please try again!')
#         return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    print("this is the caregiver's id:")
    print(user_id)
    return User.query.get(int(user_id))


@app.route('/homepage', methods=["GET", "POST"])
def login():

    email = request.form['caregiver-email']

    user = User.query.filter_by(email=email).first()
    #password = request.form.get('cg-password')
    print(email)
    #caregiver = crud.get_caregiver_by_email(email)
    print(user)
    if not user:
        return '<h1>Account not found.</h1>'

    login_user(user)

    return '<h1>Login Successful!</h1>'


@app.route('/logout')
def log_out_user():
    """Logout a caregiver"""

    logout_user(user)
    return 'You are logged out. Have a great day!'


@app.route('/start_shower')
def choose_flow():
    """Display users and their shower flows.
        Only associated user(s) will display.
        Caregiver will be able to select and start a flow"""

    users = crud.get_client_by_caregiver()

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

