"""Seed a database for testing out all these tables"""

import os
import json
import crud
import model
import server

os.system('dropdb sbtesting')
os.system('createdb sbtesting')

model.connect_to_db(server.app)  #yea? Dig in here
model.db.create_all()  #again, are we sure?

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