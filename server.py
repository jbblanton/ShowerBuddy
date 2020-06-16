"""Server file for Shower Buddy"""

from flask import (Flask, render_template, json, request, flash, session, redirect) 
from jinja2 import StrictUndefined
import crud
import model
# from model import (db, connect_to_db, Caregiver, User)
import test

app = Flask(__name__)
app.secret_key = 'lola'
app.jinja_env.undefined = StrictUndefined  


##### Routes ###########

@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('/homepage.html')


# TO DO: Modify this to be a toggle button on the main pg: show/no show
@app.route('/about')
def about_app():
    """Take visitor to the About page"""

    return test.test_function()

    #return render_template('/about.html')


@app.route('/create_user')
def create_user():
    """Go to New User form """

    return render_template('/create_user.html')


@app.route('/create_user', methods=["POST"])
def register_user():
    """Add a new user.
        Check if caregiver info already exists
        else create both objects """

    # create a caregiver:
    cg_email = request.form.get('caregiver-email')
# TO DO: If cg_email already in system, need to divert to adding an addtl user, not creating 2 accounts
    cg_pass = request.form.get('caregiver-password')
    cg_phone = request.form.get('caregiver-phone')

    caregiver = crud.create_caregiver(cg_email, cg_phone, cg_pass)

# Why?? I'm not even doing anything with sessions.... UGH
    session["cg_email"] = cg_email

    # create a user profile:
    user_name = request.form.get('user-name')
    user_body = request.form.get('body')

    new_user = crud.create_user(user_name, user_body, caregiver)

    # create a flow:
    activities = request.form.getlist('activity')

    new_flow = crud.create_flow(activities, user=new_user)

    # get the list of associated users for display on the start_shower page:
    users = crud.get_user_by_caregiver(caregiver=caregiver)

    return render_template('/start_shower.html', users=users)    


@app.route('/login', methods=['POST'])
def log_in():
    """Log in a caregiver.
        Render P3 (choose user / start shower) """

    email = request.form.get('cg-email')
    password = request.form.get('cg-password')

    active = model.Caregiver.check_if_registered(email)

    if active:
        users = crud.get_user_by_caregiver(caregiver=active)
        return render_template('/start_shower.html', users=users)
    else:
        flash('No account found. Please try again!')
        # TO DO fix this to actually work


@app.route('/start_shower')
def choose_flow():
    """Display users and their shower flows.
        Only associated user(s) will display.
        Caregiver will be able to select and start a flow"""

    users = crud.get_user_by_caregiver()

    return render_template('/start_shower.html', users=users)


@app.route('/start_shower', methods=["GET", "POST"])
def play_shower():
    """Play the shower flow.
        Will need user_id / flow_id

        Add connection for the SOS button?
        Event listener for Snooze and Next buttons """


    user_id = request.form.get['user_id.id'] 
    print(user_id)
    # Get the user_id from the FE based on who's in the drop-down

    flow_id = crud.get_users_flow_id(int(user_id))
    # Send a user_id, receive a flow_id

    activities = crud.create_shower(flow_id)
    acts_json = json.dumps(activities)
    # Get a dictionary of activities for this flow; convert to json

    products = crud.create_product_dict(flow_id)
    prods_json = json.dumps(products)
    # Get a dictionary of products for this flow; convert to json

    return render_template('/start_shower.html', acts_json, prods_json)


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

