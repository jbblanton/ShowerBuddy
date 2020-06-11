"""Seed a database for testing out all these tables"""

import os
import json
import crud
import model
import server

os.system('dropdb sbtesting')
os.system('createdb sbtesting')

model.connect_to_db(server.app)  #From server.py, app is the argument passed in to this function to set up the database

model.db.create_all()  #Make all the tables on the model.py file


def example_people():

    caregivers = []
    users = []

    a = model.Caregiver(email="atest@test.com", password="password", telephone="555-789-4561")
    caregivers.append(a)
    b = model.Caregiver(email="btest@test.com", password="password", telephone="555-789-4561")
    caregivers.append(b)
    c = model.Caregiver(email="ctest@test.com", password="password", telephone="555-789-4561")
    caregivers.append(c)

    lola = model.User(user_name="Lola", user_body="female", caregiver=a)
    users.append(lola)
    Tuesday = model.User(user_name="Tuesday", user_body="other", caregiver=b)
    users.append(Tuesday)
    pickle = model.User(user_name="Pickle", user_body="male", caregiver=b)
    users.append(pickle)
    toca = model.User(user_name="Toca", user_body="female", caregiver=c)
    users.append(toca)

    # flows = []

    flow = {
        f = {"user": lola, "title": "daily",
            1: "shampoo", 2: "conditioner", 3: "bar_soap", 4: "shave armpits"},
        l = {"user": Tuesday, "title": "weekly",
            1: "conditioner", 2: "liquid_soap", 3: "shave legs"},
        o = {"user": pickle, "title": "daily",
            1: "bar_soap", 2: "shave face"},
        w = {"user": Tuesday, "title": "Mon, Thur",
            1: "shampoo", 2: "conditioner", 3: "liquid_soap", 
            4: "shave armpits", 5: "shave legs"}
            }

    for key in flow:



    # lola-daily = Flow(title="daily", user=lola)
    # flows.append(lola-daily)
    # tues-weekly = Flow(title="weekly", user=Tuesday)
    # flows.append(tues-weekly)
    # pickle = Flow(title="daily", user=pickle)
    # flows.append(pickle)
    # tues = Flow(title="Mon, Thur", user=Tuesday)
    # flows.append(tues)

    # one = Flow_Activity(seq_step=1, flow=pickle)

    model.db.session.add_all(caregivers)
    model.db.session.add_all(users)
    #model.db.session.add_all(flows)
    model.db.session.commit()


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
    stuff = []

    for key in Activities_dictionary:
        act = model.Activity(activity_name=key, 
                description=Activities_dictionary[key]["description"], 
                activity_video=Activities_dictionary[key]["video"])
        actions.append(act)
        thing = model.Product(product_name=key,
            product_img=Activities_dictionary[key]["image"])
        stuff.append(thing)


    model.db.session.add_all(actions)
    model.db.session.add_all(stuff)
    model.db.session.commit()




