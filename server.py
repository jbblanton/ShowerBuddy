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


    # # If not in the database, create a new Caregiver and add to session:
    # active = model.Caregiver.check_if_registered(cg_email)
    # print(active)

    if current_user.is_authenticated:
        caregiver = current_user   


    # create a user profile:
    name = request.form.get('user-name')
    user_name = name.capitalize()
    user_body = request.form.get('body')

    new_user = crud.create_user(user_name, user_body, caregiver)


    # create a flow:
    activities = request.form.getlist('activity')

    new_flow = crud.create_flow(activities, user=new_user)


    # get the list of associated users for display on the dashboard:
    # cg = crud.get_caregiver_by_email(cg_email)
    users = caregiver.users

    alert = crud.send_creation_alert(API_SID, AUTH, DEMO_PHONE)

    return render_template('dashboard.html', users=users, cg_name=current_user.caregiver_name)


@app.route('/dashboard')
def caregiver_control_panel():
    """A page for a caregiver to 
        Add a new user
        Add a new flow to existing user
        Edit a flow/user
        Start the shower for one of their users
        """

    return render_template('dashboard.html')



@app.route('/login', methods=['POST'])
def log_in():
    """Log in a caregiver.
        Render P3 (choose user / start shower) """

    email = request.form.get('cg-email')
    password = request.form.get('cg-password')

    active = model.Caregiver.check_if_registered(email)
    print('****************************')
    print(active)
    
    
    if active:
        name = active.caregiver_name
        users = active.users
        login_user(active)
        return render_template('dashboard.html', cg_name=name, users=users)
    else:
        flash('Account not found.')
        return redirect('/')


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
        Will need user_id.

# TO DO Add connection for the SOS button?
        Event listener for Snooze and Next buttons """

    if request.method == "POST":
    # Get the user_id from the FE based on who's in the drop-down
        user_id = int(request.form.get('user_id')) 
        print(user_id)

    # Send a user_id, receive a flow_id
        flow_id = crud.get_users_flow_id(user_id)

    # Get a dictionary of activities for this flow
        activities = crud.create_shower(flow_id)
        # session['activities'] = activities


    # Get a dictionary of products for this flow
        products = crud.create_product_dict(flow_id)
        # session['products'] = products


        # return render_template('start_shower.html', activities= activities, products= "products")
        try:
            return jsonify({"success" : True, 
                            "html" : 'start_shower.html',
                            "activities" : activities, 
                            "products" : products,})
        except Exception as err:
            return jsonify({"success" : False, "message" : err})


@app.route('/send_help')
def alert_caregiver():
    """For use with the SOS button.
        System will send a text to the caregiver"""

    user_id = request.args.get('user_id')
    user = crud.get_user_by_user_id(user_id)

    alert = crud.send_SOS_alert(API_SID, AUTH, user, DEMO_PHONE)

    try:
        return jsonify({"success" : True, 
                    "msg" : 'Help is on the way!',})
    except Exception as err:
        return jsonify({"success" : False, "message" : err})



if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

