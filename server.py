"""Server file for Shower Buddy"""

from flask import (Flask, render_template, jsonify, request, flash, session, redirect, url_for) 
from jinja2 import StrictUndefined
import crud
import model
from twilio.rest import Client
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


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

    error = None

    # If caregiver not logged in / brand new, 
    #   get info, create new caregiver, and log them in:
    if not current_user.is_authenticated:

        # Get Caregiver info from form:
        cg_name = request.form.get('caregiver-name')
        cg_email = request.form.get('caregiver-email')
        cg_pass = request.form.get('caregiver-password')
        cg_phone = request.form.get('caregiver-phone')

        password = generate_password_hash(cg_pass, method='sha256')

        # Instantiate a Caregiver object
        caregiver = crud.create_caregiver(cg_name, cg_email, cg_phone, password)
        
        login_user(caregiver)

    if current_user.is_authenticated:
        caregiver = current_user   

    # Create a user profile:
    name = request.form.get('user-name')
    user_name = name.capitalize()
    user_body = request.form.get('body')
    flow = request.form.get('flow-name')
    if flow == " " :
        flow = 'daily'
    flow_title = flow.lower()

    dupe = crud.prevent_duplicates(caregiver, user_name, user_body, flow_title)

    if not dupe:
        new_user = crud.create_user(user_name, user_body, caregiver)
    
        # Create a flow:
        activities = request.form.getlist('activity')
        duration = int(request.form.get('duration'))

        new_flow = crud.create_flow(activities=activities, duration=duration, user=new_user, title=flow_title)

        # Get the list of associated users for display on the dashboard:
        users = caregiver.users

        # Success alert to caregiver:
        alert = crud.send_creation_alert(API_SID, AUTH, DEMO_PHONE)

        return redirect(url_for('caregiver_control_panel'))

    else:
        error = 'Duplicate user'
        flash('Oops! Looks like you already have a flow for this person.  If you\'re trying to create additional routines, give it a new name.')
    
    return render_template('create_user.html', error=error)



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
    
    error = None

    if request.method == "POST":
        email = request.form.get('cg-email')
        password = request.form.get('cg-password')

        active = model.Caregiver.check_if_registered(email)

        if active and check_password_hash(active.password, password):
            name = active.caregiver_name
            users = active.users
            login_user(active)
            return redirect(url_for('caregiver_control_panel', cg_name=name, users=users))
        else:
            error = 'Invalid credentials.'
            flash('Account not found. Please try again, or create an account!')

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

    # Get the flow_id from the FE based on who's in the drop-down:
        flow_id = request.form.get('user_id')
        print(flow_id)

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


@app.route('/edit_user')
def show_edit_pg():
    """Show edit_user page"""

    return render_template('edit_user.html')


@app.route('/edit_user/<flow_id>')
@login_required
def edit_existing_user(flow_id):
    """Link from dashboard.
        Can make edits to an existing user & their flow 
    Plans include:
        - Rename flow
        - Re-order activities
        - Add / remove activities
        - Add / remove / change images
        - Add custom activites  
    """

    flow = crud.get_flow_object(flow_id)
    title = flow.title

    activities = crud.create_shower(flow_id)
    activity_list = []
    for action in activities:
        activity_list.append(activities[action]['name'])

    duration = crud.get_length_of_shower(flow_id)

    try:
        return jsonify({"success" : True, 
                    "html" : 'edit_user.html',
                    "title" : title,
                    "activities" : activity_list, 
                    "duration" : duration,})
    except Exception as err:
        return jsonify({"success" : False, "message" : err})


# @app.route('/submit_edits')
# def make_edits():
#     """Make requested changes to database"""

#     flow_id = request.form.get('flow')
#     print(flow_id)
#     activities = request.form.getlist('upd-activity')
#     # duration = int(request.form.get('upd-duration'))

#     print(activities)
#     # print(duration)

#     title = request.form.get('flow-title')
#     if title == " " :
#         title = 'daily'
#     flow_title = title.lower()
#     #update = crud.update_user_flow_title(flow_id, flow_title)
#     print(flow_title)


#     try:
#         return jsonify({"success" : True, 
#                     "msg" : 'This routine has been updated!',})
#     except Exception as err:
#         return jsonify({"success" : False, "message" : err})





if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

