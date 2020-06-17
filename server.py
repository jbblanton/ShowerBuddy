"""Server file for Shower Buddy"""

from flask import (Flask, render_template, jsonify, request, flash, session, redirect) 
from jinja2 import StrictUndefined
import crud
import model
# from model import (db, connect_to_db, Caregiver, User)


app = Flask(__name__)
app.secret_key = 'lola'
app.jinja_env.undefined = StrictUndefined  


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

# TO DO: If cg_email already in system, need to divert to adding an addtl user, not creating 2 accounts
    

    # create a caregiver:
    cg_email = request.form.get('caregiver-email')
    cg_pass = request.form.get('caregiver-password')
    cg_phone = request.form.get('caregiver-phone')

    caregiver = crud.create_caregiver(cg_email, cg_phone, cg_pass)

    session["cg_email"] = cg_email


    # create a user profile:
    user_name = request.form.get('user-name')
    user_body = request.form.get('body')

    new_user = crud.create_user(user_name, user_body, caregiver)


    # create a flow:
    activities = request.form.getlist('activity')

    new_flow = crud.create_flow(activities, user=new_user)


    # get the list of associated users for display on the dashboard:
    cg = crud.get_caregiver_by_email(session['cg_email'])
    users = cg.users

    return render_template('start_shower.html', users=users)


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

    if active:
        cg = crud.get_caregiver_by_email(session['cg_email'])
        users = cg.users
        session["cg_email"] = email
        return render_template('dashboard.html', users=users)
    else:
        redirect('homepage.html')
# TO DO fix this to actually work


@app.route('/start_shower', methods=["GET"])
def choose_flow():
    """Display users and their shower flows.
        Only associated user(s) will display.
        Caregiver will be able to select from dropdown and start a flow"""

    cg = crud.get_caregiver_by_email(session['cg_email'])

    users = cg.users

    return render_template('start_shower.html', users=users)


@app.route('/start_shower', methods=["POST"])
def play_shower():
    """Play the shower flow.
        Will need user_id.

# TO DO Add connection for the SOS button?
        Event listener for Snooze and Next buttons """

    # Get the user_id from the FE based on who's in the drop-down
    user_id = int(request.form.get('user_id')) 
    print(user_id)

    # Send a user_id, receive a flow_id
    flow_id = crud.get_users_flow_id(user_id)

    # Get a dictionary of activities for this flow
    activities = crud.create_shower(flow_id)

    # Get a dictionary of products for this flow
    products = crud.create_product_dict(flow_id)

    try:
        return jsonify({"success" : True, 
                        "activities" : activities, 
                        "products" : products,})
    except Exception as err:
        return jsonify({"success" : False, "message" : err})



if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

