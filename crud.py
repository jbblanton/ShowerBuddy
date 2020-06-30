"""Use the form data to create accounts, users, shower flows, etc. """

from model import (db, connect_to_db, Caregiver, User, Flow, Flow_Activity, Activity, Flow_Product, Product)
import json
from twilio.rest import Client


def send_creation_alert(ACCOUNT_SID, AUTH_TOKEN, cg_phone):
    """Text sent to Caregiver after create_user completed
        ...
        >>> crud.send_creation_alert(API_SID, AUTH, DEMO_PHONE)
        SMe4c8c4664c6548108925f5030adbab88

        For an un-verified number:
        >>> crud.send_creation_alert(API_SID, AUTH, '+19876543210')
        twilio.base.exceptions.TwilioRestException:
        HTTP Error Your request was:

        POST /Accounts/AC74fda96dded3b27bbd09502ceb5639d1/Messages.json

        Twilio returned the following information:

        Unable to create record: The number  is unverified. Trial accounts cannot send messages to unverified numbers; verify  at twilio.com/user/account/phone-numbers/verified, or purchase a Twilio number to send messages to unverified numbers.

        More information may be available here:

        https://www.twilio.com/docs/errors/21608
        """

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
        .create(
            body="Nice job on creating a new user! Please visit your ShowerBuddy dashboard to start a shower.",
            from_='+12058968145',
            to=cg_phone,
            )

    print(message.sid)


def send_SOS_alert(ACCOUNT_SID, AUTH_TOKEN, user_name, cg_phone):
    """Send text message to caregiver if SOS Button is pressed

        >>> crud.send_SOS_alert(API_SID, AUTH, 'Lola', DEMO_PHONE)
        SM928107b713b644808792cf51d24dc2bc
        """

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
        .create(
            body=f"{user_name} needs help in the bathroom!",
            from_='+12058968145',
            to=cg_phone,
            )

    print(message.sid)


#TO DO: Write what calls this function:
def alert_shower_started(ACCOUNT_SID, AUTH_TOKEN, user_name, cg_phone):
    """Send a text message to caregiver when a shower is started.
        USE CASE: if/when a user is able to start their own shower routine.
            This alert is intended to alert the caregiver so they will 
            respond quickly to any SOS alert """

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
        .create(
            body=f"{user_name} is starting a shower; Please keep your phone nearby until they have finished.",
            from_='+12058968145',
            to=cg_phone,
            )

    print(message.sid)
    

#TO DO: Write what calls this function:
def alert_shower_completed(ACCOUNT_SID, AUTH_TOKEN, user_name, cg_phone):
    """Send a text message when a shower flow is completed. """

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
        .create(
            body=f"{user_name} has finished showering!",
            from_='+12058968145',
            to=cg_phone,
            )

    print(message.sid)    


def get_user_by_flow_id(flow_id):
    """Pull the name of user by their flow ID to get the user ID;
        for use with phone alerts.
        """

    flow = db.session.query(Flow).filter(Flow.flow_id == flow_id).first()
    user_id = flow.user_id

    user = db.session.query(User).filter(User.user_id == user_id).first()
    name = user.user_name

    return name


def create_caregiver(name, email, telephone, password):
    """ Data gathered at bottom of Create User form: 

        >>> crud.create_caregiver("Vera", "vvanderbilt@test.com", '147-258-3690', 'password')
        ...
        <Caregiver caregiver_id=4, email=vvanderbilt@test.com, phone=147-258-3690>
        
        >>> crud.create_caregiver(name="Jane", email="atest@test.com", password='password', telephone='789-456-1236')
        psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "caregivers_email_key"
        DETAIL:  Key (email)=(atest@test.com) already exists.
        """

    caregiver = Caregiver(caregiver_name=name, email=email, telephone=telephone, password=password)

    db.session.add(caregiver)
    db.session.commit()

    return caregiver


def create_user(name, body, caregiver):
    """ Data gathered from create_user form
        May be created at time of Caregiver creation or as an addtion to an
        existing Caregiver (with expectation that they be logged inn) """

    user = User(user_name=name, user_body=body, caregiver=caregiver)

    db.session.add(user)
    db.session.commit()

    return user


def get_caregiver_by_email(email):
    """Search database by email; Used for login. 
        Returns Caregiver Object

        >>> crud.get_caregiver_by_email('btest@test.com')
        <Caregiver caregiver_id=2, email=btest@test.com, phone=555-789-4561>

        >>> crud.get_caregiver_by_email('nobody@test.com')
        >>>
        """

    caregiver = db.session.query(Caregiver).filter(Caregiver.email == email).first()

    return caregiver


# For now, default title = 'Daily'
def create_flow(activities, user, duration=20, title="daily"):
    """ Data gathered from create_user form 
        Must be created at time of User creation """

    flow = Flow(title=title, duration=duration, user=user)

    flow_obj = []
    prod_obj = []

    # ['shampoo', 'bar soap', 'shave face']
    for activity in activities:
        act = db.session.query(Activity).filter(Activity.activity_name == activity).first()
        prod = db.session.query(Product).filter(Product.product_name == activity).first()
        step = Flow_Activity(activity=act, flow=flow)
        flow_obj.append(step)
        thing = Flow_Product(flowacts=step, products=prod)
        prod_obj.append(thing)

    db.session.add(flow)
    db.session.add_all(flow_obj)
    db.session.add_all(prod_obj)
    db.session.commit()

    return flow


def create_shower_dict(flow_id):
    """Make a dictionary of activities for a given user"""
    # Shower Flow = { activity_id:
    #                 activity_name:
    #                 description:
    #                 video:          }

    shower_flow = {}

    action = db.session.query(Activity).join(Flow_Activity).filter(Flow_Activity.flow_id == flow_id).all()

    for i, act in enumerate(action):
        shower_flow[action[i].activity_id] = {
                            "name" : action[i].activity_name, 
                            "description" : action[i].description,
                            "video" : action[i].activity_video,
                            }

    return shower_flow


def get_length_of_shower(flow_id):
    """Return duration of this shower flow"""

    length = db.session.query(Flow).filter(Flow.flow_id == flow_id).first()
 
    shower_length = length.duration
   
    return shower_length


def create_product_dict(flow_id):
    """Make a dictionary of products needed during a given flow"""

    # Product = { product_id:
    #                 product_image:
    #                 product_name:
    #                 product_color_label:
    #             }

    product_dict = {}

    all_products = db.session.query(Flow_Activity).filter(Flow_Activity.flow_id == flow_id).all()

    prod_list = []
    # Make a list of the flow_act_ids
    for i, prod in enumerate(all_products):
        prod_list.append(all_products[i].flow_act_id)
  
    for num in prod_list:
        product = db.session.query(Product).join(Flow_Product).filter(Flow_Product.fa_id == num).all()
        product_dict[num] = {"name" : product[0].product_name, 
                            "image" : product[0].product_img, 
                            "label_color" : product[0].product_label_color,}
        
    return product_dict


def prevent_duplicates(caregiver, name, body, title):
    """Check the database before creating a new user"""

    # if cg is logged in and creates a new user/flow, 
    #     check their user names and compare
    #         already exist?
    #             'theres someone with this name; let\'s name a new flow, instead'

    for user in caregiver.users:
        if user.user_name == name:
            if user.user_body == body:
                if title == 'daily':
                    return True

    return False


def get_flow_object(flow_id):
    """I know there has to be a better way..."""

    flow = db.session.query(Flow).filter(Flow.flow_id == flow_id).first()

    return flow


def update_user_flow(flow_id, new_duration, new_title):
    """Update a users flow title and duration"""
    
    old_flow = db.session.query(Flow).filter(Flow.flow_id == flow_id).first()

    old_flow.title = new_title
    old_flow.duration = new_duration

    db.session.commit()

    return old_flow


def update_user_activities(flow_id, activities):
    """Update the activities in a flow"""

    old_action = db.session.query(Activity).join(Flow_Activity).filter(Flow_Activity.flow_id == flow_id).all()

    if len(old_action) == len(activities):
        for idx, act in enumerate(old_action):
            for index, activity in enumerate(activities):
                old_action[idx] = db.session.query(Activity).filter(Activity.activity_name == activities[idx]).first()
        db.session.commit()

    if len(old_action) > len(activities):
        old = set(old_action) #this is printing a set of objects
        print(old)
        print('OLD')
        new = set(activities)
        print(new)
        print('NEW')
        remove = old - new
        for act in list(remove):
            print(act)
            print('***********')



    # old_flow.

    # flow = Flow(title="daily", duration=duration, user=user)

    # flow_obj = []

    # # ['shampoo', 'bar soap', 'shave face']
    # for activity in activities:
    #     act = db.session.query(Activity).filter(Activity.activity_name == activity).first()
    #     prod = db.session.query(Product).filter(Product.product_name == activity).first()
    #     step = Flow_Activity(activity=act, flow=flow)
    #     flow_obj.append(step)



    # db.session.add(flow)
    # db.session.add_all(flow_obj)
    # db.session.add_all(prod_obj)
    # db.session.commit()

    # return flow




#####  TO DO:  #####    


def update_product_images():
    """Update the database with new photos """

    pass

    # return success or fail message





if __name__ == '__main__':
    from server import app
    connect_to_db(app)