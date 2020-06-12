"""Use the form data to create accounts, users, shower flows, etc. """

from model import (db, connect_to_db, Caregiver, User, Flow, Flow_Activity, Activity, Product)
import json


def create_caregiver(email, telephone, password):
    """Pt 1 of form will collect this data: 
        ...
        Plan is to call this function when the person moves from Pt 1 to Pt 2 so the Caregiver object will be available for the next function """
      
    caregiver = User(email=email, telephone=telephone, password=password)
        
    db.session.add(caregiver)
    db.session.commit()

    return caregiver


def create_client(name, body, caregiver):
    """P2 of form will collect this data:
        ...
        Expecting to be able to call on caregiver data based on either P1 or an existing caregiver account """

    client = Client(client_name=name, client_body=body, caregiver=caregiver)

    db.session.add(client)
    db.session.commit()

    return user



def get_user_by_caregiver(caregiver):
    """Returns a list of users associated with a given caregiver"""

    print(caregiver.caregiver_id)

    users = db.session.query(User).filter(User.caregiver_id == caregiver.caregiver_id).all()

    return users


def create_flow(activities, user):
    """Will call upon an existing User object to create a shower routine 
        (numbering the order of activities) """

    flow = Flow(title="daily", user=user)

    flow_obj = []
    prod_obj = []

    # ['shampoo', 'bar soap', 'shave face']
    for activity in activities:
        act = db.session.query(Activity).filter(Activity.activity_name == activity).first()
        prod = db.session.query(Product).filter(Product.product_name == activity).first()
        step = Flow_Activity(act, flow)
        flow_obj.append(step)
        thing = Flow_Product(step, prod)
        prod_obj.append(thing)

    db.session.add(flow)
    db.session.add_all(flow_obj)
    db.session.add_all(prod_obj)
    db.session.commit()

    return flow


def get_client_by_caregiver(caregiver):
    """Returns a list of all users associated with a caregiver ID"""

    users = db.session.query(Client).filter(Client.caregiver_id == caregiver.user_id).all()

    return users


def get_caregiver_by_email(email):
    """Get info on a Caregiver so they can log in. """

    caregiver = User.query.get(User.email == email)

    return caregiver


def create_flow_activities(flow, steps):
    """ Steps is a dictionary of activities [shampoo, condition, shave, etc.] 
            in an order designated by the caregiver during creation.
Need to figure out this part--> Time is a whole-shower unit that will be 
        segmented out to each step in the flow.
        From flow, pull title and flow_id
        """

    # steps = {1: "shampoo", 2: "shave face", 3: "scrub body"}  <--json file??
    for keys, values, in steps:
        Flow_Activity.seq_step = key
        Activity.description = Activities_dictionary[value]
        Product.product_name = value

# Needed: a database of descriptions to pull from for Activity.description
#        (future feature to allow a caregiver to record their voice?)

    # Maybe this dictionary is where the images of a user's products can be stored?
    # Or, at least the url that would get the image, if kept separately. 
    # Is there a master dictionary and then one that gets built for the flow? 
    # This could allow someone to potentially overwrite the description and 
    # still be able to revert to the default if desired.


def get_products(user, flow):
    """Gets names and images of all products that will 
        be needed for a shower """

    pass

    # return [products.product_name and products.product_image]


def get_users_flow(user, flow):
    """Loads the shower routine for a given user and flow.title """

    pass

    # return [how the fuck am I doing this??]


def update_product_images():
    """Update the database with new photos """

    pass

    # return success or fail message



if __name__ == '__main__':
    from server import app
    connect_to_db(app)