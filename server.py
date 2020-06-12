"""Server file for Shower Buddy"""

from flask import (Flask, render_template, request, flash, session, redirect) 
from jinja2 import StrictUndefined
from model import (db, connect_to_db, Caregiver, User)
from flask_login import (LoginManager, login_user, login_required, logout_user)
import crud
import model
# from model import (db, connect_to_db, Caregiver, User)
import test

app = Flask(__name__)
app.secret_key = 'lola'
app.jinja_env.undefined = StrictUndefined  



##### Routes ###########


### App Routes:
@app.route('/')
def homepage():
    """Render the homepage"""

    return render_template('/homepage.html')


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
    activities = request.form.get('activity')
    new_flow = crud.create_flow(activities, user=new_user)


    # get the list of associated users for display on the start_shower page:
    users = crud.get_user_by_caregiver(caregiver=caregiver)
    print(users)

    return render_template('/start_shower.html', users=users)    


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

    email = request.form.get('cg-email')
    password = request.form.get('cg-password')

    active = model.Caregiver.check_if_registered(email)

    if active:
        users = crud.get_user_by_caregiver(caregiver=active)
        return render_template('/start_shower.html', users=users)
    else:
        flash('No account found. Please try again!')



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

    # shower_flow.take_shower()



    return render_template('/start_shower.html')


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

