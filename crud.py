"""Use the form data to create accounts, users, shower flows, etc. """

from model import db, Caregiver, User, Flow, Flow_Activity, Activity, Product
import json

def create_caregiver(email, telephone, password):
    """Pt 1 of form will collect this data: 
        ...
        Plan is to call this function when the person moves from Pt 1 to Pt 2 so the Caregiver object will be available for the next function """

    caregiver = Caregiver(email=email, telephone=telephone, password=password)

    db.session.add(caregiver)
    db.session.commit()


def create_user(name, body, caregiver):
    """P2 of form will collect this data:
        ...
        Expecting to be able to call on caregiver data based on either P1 or an existing caregiver account """

    user = User(user_name=name, user_body=body, caregiver=caregiver)

    db.session.add(user)
    db.session.commit()


# Can we make a default title here?
def create_flow(title, user):
    """Will call upon an existing User object to create a shower routine 
        (numbering the order of activities) """

    flow = Flow(title=title, user=user)

    db.session.add(flow)
    db.session.commit()

# Should this be blended in to the next function to do all in one?

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




#####  TO DO:  #####

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