"""Server file for Shower Buddy"""

from flask import (Flask, render_template, jsonify, request, flash, session, redirect, url_for) 
from jinja2 import StrictUndefined
import crud
import model
from twilio.rest import Client
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = os.environ['SUPER_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined  

########### TWILIO #############

API_SID = os.environ['ACCOUNT_SID']
AUTH = os.environ['AUTH_TOKEN']
DEMO_PHONE = os.environ['PHONE']

########### Flask Login ########

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
LoginManager.login_view = "/"

@login_manager.user_loader
def load_user(caregiver_id):
    """Returns a Caregiver object, based on unique ID"""

    return model.Caregiver.query.get(int(caregiver_id))

##### Routes ###########

@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('homepage.html')


@app.route('/create_user')
def create_user():
    """Go to New User form """

    return render_template('create_user.html')


@app.route('/create_user', methods=["POST"])
def register_user():
    """Add a new user.
        Check if caregiver info already exists
        else create both objects """

    if not current_user.is_authenticated:

        # Get Caregiver info from form:
        cg_name = request.form.get('caregiver-name')
        cg_email = request.form.get('caregiver-email')
        cg_pass = request.form.get('caregiver-password')
        cg_phone = request.form.get('caregiver-phone')

        # Instantiate a Caregiver object
        caregiver = crud.create_caregiver(cg_name, cg_email, cg_phone, cg_pass)
        
        login_user(caregiver)


    if current_user.is_authenticated:
        caregiver = current_user   


    # Create a user profile:
    name = request.form.get('user-name')
    user_name = name.capitalize()
    user_body = request.form.get('body')

    new_user = crud.create_user(user_name, user_body, caregiver)


    # Create a flow:
    activities = request.form.getlist('activity')
    duration = int(request.form.get('duration'))

    new_flow = crud.create_flow(activities=activities, duration=duration, user=new_user)


    # Get the list of associated users for display on the dashboard:
    users = caregiver.users

    # Success alert to caregiver:
    alert = crud.send_creation_alert(API_SID, AUTH, DEMO_PHONE)

    return redirect(url_for('caregiver_control_panel'))
# , users=users, cg_name=current_user.caregiver_name

@app.route('/dashboard')
@login_required
def caregiver_control_panel():
    """A page for a caregiver to 
        -Add a new user
        -Add a new flow to existing user
TO DO:  -Edit a flow/user
        -Start the shower for one of their users
        """

    return render_template('dashboard.html')


@app.route('/login', methods=['POST'])
def log_in():
    """Log in a caregiver.
        Render Dashboard"""

    email = request.form.get('cg-email')
    password = request.form.get('cg-password')

    active = model.Caregiver.check_if_registered(email)

    if active:
        name = active.caregiver_name
        users = active.users
        login_user(active)
        return redirect(url_for('caregiver_control_panel', cg_name=name, users=users))
    else:
        error = 'Invalid credentials.'
        flash('Account not found.')

    return render_template('homepage.html', error=error)


@app.route('/logout')
@login_required
def log_out():
    """Exit a session"""

    logout_user()

    return redirect('/')


@app.route('/start_shower')
@login_required
def show_shower_page():
    """Render the shower page"""

    return render_template('start_shower.html')


@app.route('/start_shower', methods=["POST"])
@login_required
def play_shower():
    """Play the shower flow.

TO DO:    Event listener for Snooze and Next buttons """

    if request.method == "POST":
    # Get the user_id from the FE based on who's in the drop-down
        user_id = int(request.form.get('user_id')) 

    # Send a user_id, receive a flow_id
        flow_id = crud.get_users_flow_id(user_id)

    # Get a dictionary of activities for this flow
        activities = crud.create_shower(flow_id)

    # Get a dictionary of products for this flow
        products = crud.create_product_dict(flow_id)

    # Get duration of the shower flow (10, 20, 30 minutes)
        duration = crud.get_length_of_shower(flow_id)

        try:
            return jsonify({"success" : True, 
                            "html" : 'start_shower.html',
                            "activities" : activities, 
                            "products" : products,
                            "duration" : duration,})
        except Exception as err:
            return jsonify({"success" : False, "message" : err})


@app.route('/send_help')
def alert_caregiver():
    """For use with the SOS button.
        System will send a text to the caregiver"""

    user_id = request.args.get('user_id')
    user = crud.get_user_by_user_id(user_id)

    # Notify caregiver via text; includes user name:
    alert = crud.send_SOS_alert(API_SID, AUTH, user, DEMO_PHONE)

    try:
        return jsonify({"success" : True, 
                    "msg" : 'Help is on the way!',})
    except Exception as err:
        return jsonify({"success" : False, "message" : err})



if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

