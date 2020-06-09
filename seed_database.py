"""Seed a database for testing out all these tables"""

import os
import json
import crud
import model
import server

os.system('dropdb testing')
os.system('createdb testing')

model.connect_to_db(server.app)  #From server.py, app is the argument passed in to this function to set up the database

model.db.create_all()  #Make all the tables on the model.py file

# Examples:

# Caregiver: Robin@aol.com, 555-222-7890, pass1234
#     User: Bob, male, daily showers, shampoo, soap, shave face


# def example_dats():

#     c = Caregiver(email="Robin@aol.com",telephone="555-222-7890", password="pass1234")
#     # creating a user object called c 
#     # including c in constructor call for our user creates the relationship
#     u = User(user_name="Bob", user_body=male, caregiver=c)
#     new_flow = Flow(.....)
#     act1 = .......
#     new_flow.activities.append(act1) #append things one at a time, see if you can use extened if you need to do many at once
#     db.session.add(new_flow, u)


Activities_dictionary = {
    "shampoo": {
        "description": "Put a small amount of shampoo into your hand, pat your hands together, and then rub this shampoo into your hair. Use your fingertips to massage your head, so the shampoo can clean your scalp.", 
        "video": "video_file.mpeg",
        "image": "shampoo.jpg"
        }, 
    "conditioner": {
        "description": "Put a small amount of conditioner into your hand, pat your hands together, and then massage this conditioner into your hair.", 
        "video": "video_file2.mpeg",
        "image": "conditioner.jpg"
        },
    "bar soap": {
        "description": "Get the bar of soap wet and rub the bar onto a washcloth to create a lather. Use washcloth to scrub your body. Be sure to spend extra time on the trinity.",
        "video": "video_file3.mpeg",
        "image": "bar_soap.jpg"
    }
}

def seed_activities(dictionary):
    """Fill the Activity table with standard data"""

    actions = []

    for key in Activities_dictionary:
        act = model.Activity(activity_name=key, 
                description=Activities_dictionary[key]["description"], 
                activity_video=Activities_dictionary[key]["video"])
        actions.append(act)


    model.db.session.add_all(actions)
    model.db.session.commit()


def seed_products(dictionary):
    """Fill in some default products """

    stuff = []

    for key in Activities_dictionary:
        thing = model.Product(product_name=key, 
            product_img=Activities_dictionary[key]["image"])
        stuff.append(thing)

    model.db.session.add_all(stuff)
    model.db.session.commit()


# >>> robin = model.Caregiver(email="robin@aol.com", password="1234pass", telephone="555-789-4561")
# >>> lola = model.User(user_name="Lola", user_body="female", caregiver=robin)
# >>> model.db.session.add(robin)
# >>> model.db.session.add(lola)