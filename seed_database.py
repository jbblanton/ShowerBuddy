"""Seed a database for testing out all these tables"""

import os
import json
import crud
import model
import server
from werkzeug.security import generate_password_hash

os.system('dropdb testing')
os.system('createdb testing')

model.connect_to_db(server.app)  #From server.py, app is the argument passed in to this function to set up the database

model.db.create_all()  #Make all the tables on the model.py file


def example_people():

    caregivers = []
    users = []
    flows = []

    a = model.Caregiver(caregiver_name="Jane", email="atest@test.com", password=generate_password_hash("passworda", method='sha256'), telephone="555-789-4561")
    b = model.Caregiver(caregiver_name="paula", email="btest@test.com", password=generate_password_hash("passwordb", method='sha256'), telephone="555-789-4561")
    c = model.Caregiver(caregiver_name="George", email="ctest@test.com", password=generate_password_hash("passwordc", method='sha256'), telephone="555-789-4561")
    caregivers.extend([a,b,c])

    lola = model.User(user_name="Lola", user_body="female", caregiver=a)
    Tuesday = model.User(user_name="Tuesday", user_body="other", caregiver=b)
    pickle = model.User(user_name="Pickle", user_body="male", caregiver=b)
    toca = model.User(user_name="Toca", user_body="female", caregiver=c)
    users.extend([lola, Tuesday, pickle, toca])

    one = crud.create_flow(["shampoo", "conditioner", "bar-soap", "shave-armpits"], lola, 20)
    two = crud.create_flow(["conditioner", "liquid-soap", "shave-legs"], Tuesday, 10)
    three = crud.create_flow(["bar-soap", "shave-face"], pickle, 10)
    four = crud.create_flow(["shampoo", "conditioner", "liquid-soap", "shave-armpits", "shave-legs"], toca, 30)
    flows.extend([one, two, three, four])


    model.db.session.add_all(caregivers)
    model.db.session.add_all(users)
    model.db.session.add_all(flows)
    model.db.session.commit()


def seed_activities():
    """Fill the Activity table with standard data"""
    
    Activities_dictionary = {
    "shampoo": {
        "description": "Put a small amount of shampoo into your hand, pat your hands together, and then rub this shampoo into your hair. Use your fingertips to massage your head, so the shampoo can clean your scalp.", 
        "video": "https://giphy.com/embed/1dPi0Gy6t0rTQQvTZ6",
        "image": "/static/img/shampoo.png"
        }, 
    "conditioner": {
        "description": "Put a small amount of conditioner into your hand, pat your hands together, and then massage this conditioner into your hair.", 
        "video": "https://giphy.com/embed/mRvJKBHGhJFIc",
        "image": "/static/img/conditioner.png"
        },
    "bar-soap": {
        "description": "Get the bar of soap wet and rub the bar onto a washcloth to create a lather. Scrub!",
        "video": "https://giphy.com/embed/3o6MbjjOqVPMHZvuve",
        "image": "/static/img/bar_soap.png"
        },
    "liquid-soap": {
        "description": "Squirt soap on loofah and scrub!",
        "video": "https://giphy.com/embed/3o6nUOysbD4Q4WEKuA",
        "image": "/static/img/liquid_soap.png"
        },
    "shave-face": {
        "description": "Shave your face",
        "video": "https://giphy.com/embed/l3q2NRoiCbOtccRqw",
        "image": "/static/img/razor2.png"
        },
    "shave-armpits": {
        "description": "Shave under your arms",
        "video": "https://giphy.com/embed/pXPytwoLcTRJu",
        "image": "/static/img/razor_blades.png"
        },
    "shave-legs": {
        "description": "Shave your legs",
        "video": "https://giphy.com/embed/LvBMdu0KRfKlq",
        "image": "/static/img/lady_razor.png"
        },
}


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



seed_activities()
example_people()


#####********###########*************##########***********#########***

# PLEASE DO NOT FORGET THAT THESE ARE ALL TERRIBLE.  REPLACE BEFORE DEMO!!

# <iframe src="https://giphy.com/embed/l3q2NRoiCbOtccRqw" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/loop-man-hair-l3q2NRoiCbOtccRqw">via GIPHY</a></p>   shave-face

# <iframe src="https://giphy.com/embed/LvBMdu0KRfKlq" width="480" height="286" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/shaving-LvBMdu0KRfKlq">via GIPHY</a></p> shave-legs

# <iframe src="https://giphy.com/embed/pXPytwoLcTRJu" width="480" height="265" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/yeah-armpits-youladies-pXPytwoLcTRJu">via GIPHY</a></p>  shave-armpits

# <iframe src="https://giphy.com/embed/3o6nUOysbD4Q4WEKuA" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/video-art-zita-nagy-3o6nUOysbD4Q4WEKuA">via GIPHY</a></p>  liquid-soap

# <iframe src="https://giphy.com/embed/1dPi0Gy6t0rTQQvTZ6" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/kingoftheroad-viceland-shampoo-shampooing-1dPi0Gy6t0rTQQvTZ6">via GIPHY</a></p>  shampoo

# <iframe src="https://giphy.com/embed/mRvJKBHGhJFIc" width="480" height="266" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/sing-problem-shower-mRvJKBHGhJFIc">via GIPHY</a></p> conditioner

# <iframe src="https://giphy.com/embed/1tK61mF7P7x4I" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/shower-loop-dexter-1tK61mF7P7x4I">via GIPHY</a></p>  Dexter-get-wet

# <iframe src="https://giphy.com/embed/3o6MbjjOqVPMHZvuve" width="480" height="362" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/season-4-the-simpsons-4x3-3o6MbjjOqVPMHZvuve">via GIPHY</a></p> Homer-soap

# <iframe src="https://giphy.com/embed/kDBhX1Il2PZL66ljiL" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/farmersinsurance-bear-farmers-insurance-drying-off-kDBhX1Il2PZL66ljiL">via GIPHY</a></p>  Bear drying off


# ACTUAL QUALITY: 
# <iframe src="https://giphy.com/embed/MBZKkYQYgv95pantzk" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/virus-washing-hands-sanitize-MBZKkYQYgv95pantzk">via GIPHY</a></p>  wash-hands

# <iframe src="https://giphy.com/embed/yoJC2zNPBxSVPNQC0o" width="480" height="271" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/skintimate-shower-shave-gel-yoJC2zNPBxSVPNQC0o">via GIPHY</a></p>  shaving-cream

# <iframe src="https://giphy.com/embed/l0HlEIP347YAFjq6I" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/wikihow-daily-bath-l0HlEIP347YAFjq6I">via GIPHY</a></p>  taking a shower