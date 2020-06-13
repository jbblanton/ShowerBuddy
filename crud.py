"""Use the form data to create accounts, users, shower flows, etc. """

from model import (db, connect_to_db, Caregiver, User, Flow, Flow_Activity, Activity, Flow_Product, Product)
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

    users = db.session.query(User).filter(User.caregiver_id == caregiver.caregiver_id).all()

    return users


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

    flows = db.session.query(Flow).filter(Flow.user_id == user.user_id).all()

    flow_id = flows[0].flow_id
    # hard coding this due to every user currently only having one flow.  
    # TO DO: Edit when additional routines are an option!

    return flow_id


def get_caregiver_by_email(email):
    """Get info on a Caregiver so they can log in. """

    caregiver = User.query.get(User.email == email)

    return caregiver


#####  TO DO:  #####


def get_products(user, flow):
    """Gets names and images of all products that will 
        be needed for a shower """

    pass

    # return [products.product_name and products.product_image]


def update_product_images():
    """Update the database with new photos """

    pass

    # return success or fail message



if __name__ == '__main__':
    from server import app
    connect_to_db(app)