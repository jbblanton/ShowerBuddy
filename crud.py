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

    flows = db.session.query(Flow).filter(Flow.user_id == user).all()

    flow_id = flows[0].flow_id
    # hard coding this due to every user currently only having one flow.  
    # TO DO: Edit when additional routines are an option!

    return flow_id


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


def create_shower(flow_id):
    """Use this function to make a list of activities for a given user"""
    # Shower Flow = { activity_id:
    #                 activity_name:
    #                 description:
    #                 video:          }

    shower_flow = {}

    action = db.session.query(Activity).join(Flow_Activity).filter(Flow_Activity.flow_id == flow_id).all()

    for i, act in enumerate(action):
        shower_flow[action[i].activity_id] = {"name" : action[i].activity_name, 
                                "description" : action[i].description,
                                "video" : action[i].activity_video,
                                "act_prod_id" : action[i].flow_act.flow_act_id}

    return shower_flow


def create_product_dict(flow_id):
    """Use this to make a dictionary of products needed during a given flow"""

    # Product = { product_id:
    #                 product_image:
    #                 product_name:
    #                 product_color_label:
    #             }

    product_dict = {}

    # SELECT * FROM flow_acts WHERE flow_id = 2;
    #   returns list of objects with flow_act_id, seq_step, and activity_id
    all_products = db.session.query(Flow_Activity).filter(flow_id == flow_id)

    prod_list = []
    # Make a list of the flow_act_ids
    for i, prod in enumerate(all_products):
        prod_list.append(products[i].flow_act_id)

    # SELECT * FROM products JOIN flow_products ON products.product_id = flow_products.prod_id WHERE fa_id = 5;
    for num in prod_list:
        product = db.session.query(Product).join(Flow_Product).filter(fa_id == num)
        product_dict[product.fa_id] = {"name" : product.product_name, 
                                    "image" : product.product_img, 
                                    "label_color" : product.product_label_color,}
        
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