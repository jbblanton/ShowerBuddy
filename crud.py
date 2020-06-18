"""Use the form data to create accounts, users, shower flows, etc. """

from model import (db, connect_to_db, Caregiver, User, Flow, Flow_Activity, Activity, Flow_Product, Product)
import json
from twilio.rest import Client


def send_creation_alert(ACCOUNT_SID, AUTH_TOKEN):
    """TESTING Twilio functionality"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
                    .create(
                        body="Nice job on creating a new user!",
                        from_='+12058968145',
                        to="+15085794940"
                        )

    print(message.sid)


def send_SOS_alert(ACCOUNT_SID, AUTH_TOKEN):
    """Send text message to caregiver if SOS Button is pressed"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages \
                    .create(
                        body="HELP is needed!",
                        from_='+12058968145',
                        to="+15085794940"
                        )

    print(message.sid)


def create_caregiver(email, telephone, password):
    """Pt 1 of form will collect this data: 
        ...
        Plan is to call this function when the person moves from Pt 1 to Pt 2 so the Caregiver object will be available for the next function """

    caregiver = Caregiver(email=email, telephone=telephone, password=password)

    db.session.add(caregiver)
    db.session.commit()

    return caregiver


def create_user(name, body, caregiver):
    """P2 of form will collect this data:
        ...
        Expecting to be able to call on caregiver data based on either P1 or an existing caregiver account """

    user = User(user_name=name, user_body=body, caregiver=caregiver)

    db.session.add(user)
    db.session.commit()

    return user


def get_caregiver_by_email(email):

    caregiver = db.session.query(Caregiver).filter(Caregiver.email == email).first()

    return caregiver


# For now, default title = 'Daily'
def create_flow(activities, user):
    """Will call upon an existing User object to create a shower routine 
        (returns a flow object) """

    flow = Flow(title="daily", user=user)

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


def get_users_flow_id(user):
    """Loads all available shower routines for a given user.
        Returns a list of objects:
        [<Flow flow_id=1, title=daily, user=Honey>]
        """

    flows = db.session.query(Flow).filter(Flow.user_id == user).all()

    flow_id = flows[0].flow_id
    # hard coding this due to every user currently only having one flow.  
# TO DO: Edit when additional routines are an option!

    return flow_id
    # print(flows)

def create_shower(flow_id):
    """Use this function to make a list of activities for a given user"""
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
    # print(shower_flow)

def create_product_dict(flow_id):
    """Use this to make a dictionary of products needed during a given flow"""

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


#####  TO DO:  #####


def update_product_images():
    """Update the database with new photos """

    pass

    # return success or fail message


def update_user_flow():
    """Update order, or elements, of a user's flow"""

    pass


if __name__ == '__main__':
    from server import app
    connect_to_db(app)