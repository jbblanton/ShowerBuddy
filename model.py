"""Models for the Shower Buddy app"""

import os
from flask_sqlalchemy import SQLAlchemy
import crud
import server

os.system('dropdb testing')
os.system('createdb testing')

db = SQLAlchemy()

# Can there be a connection between 2 (eg: cg_id = 12, user_id = 12.1 ?)
# Can the incrementing start at a certain point, or start with min digits?


################# Models & Info ##################################

class Caregiver(db.Model):
    """A Caregiver"""

    __tablename__ = "caregivers"

    caregiver_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    #caregiver_name =db.Column(db.String(25),)
    email = db.Column(db.String(50), unique = True, nullable = False,)
    password = db.Column(db.String(25), nullable = False,)
    telephone = db.Column(db.String(12),)

    user = db.relationship('User')

    def __repr__(self):
        return f'<Caregiver caregiver_id={self.caregiver_id}, \
                email={self.email}, phone={self.telephone}>'


class User(db.Model):
    """A User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    user_name = db.Column(db.String(50), nullable = False,)
    user_body = db.Column(db.String(6),)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregivers.caregiver_id'))

    caregiver = db.relationship('Caregiver')
    flow = db.relationship('Flow')

    def __repr__(self):
        return f'<User name={self.user_name} user_id={self.user_id}>'


class Flow(db.Model):
    """A user's shower routine"""

    __tablename__ = "flows"

    flow_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    title = db.Column(db.String(60),)
# default title = 'daily'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    user = db.relationship('User')

    def __repr__(self):
        return f'<Flow flow_id={self.flow_id}, title={self.title}, \
                user={self.user.user_name}>'
        # I don't know if I can write that last bit like that... FIND OUT


class Flow_Activity(db.Model):
    """Connector table between Flow & Activities"""

    __tablename__ = "flow_acts"

    flow_act_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    seq_step = db.Column(db.Integer, nullable = False,)
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.flow_id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))

    flow = db.relationship('Flow')
    activity = db.relationship('Activity')

    def __repr__(self):
        return f'<Flow_Activity flow_act_id={self.flow_act_id}, \
                step in sequence={self.seq_step}>'


class Activity(db.Model):
    """Activities that occur during a shower sequence or 'flow' """

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    activity_name = db.Column(db.String(30))
    description = db.Column(db.Text,)
    activity_video = db.Column(db.Text,)

    flow_act = db.relationship('Flow_Activity')
    #act_prod_id = db.relationship('Activity_Product')

    def __repr__(self):
        return f'<Activity id={self.activity_id}, description={self.description}, \
                video={self.activity_video}>'



## Deactivated this table on 6/5 based on a conversation with mentor R. 
## Since one activity (shampooing) can have many products due to the number of 
## unique users (Bob uses Pert, Lola uses Suave, Pickle uses Pantene, etc.), 
## this was a messy connection.
## This table is being replaced by Flow_Product which will tuple a 
## flow_act_id and product_id to allow the unique combo of user + product.
##
# class Activity_Product(db.Model):
#     """Connector table between Activities & Products """

#     __tablename__ = "activity_products"

#     act_prod_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
#     activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

#     activity = db.relationship('Activity')
#     product = db.relationship('Product')

#     def __repr__(self):
#         return f'<Act_Prod id={self.act_prod_id}, activity_id={self.activity_id}, \
#                 product_id={self.product_id}>' 


# class Flow_Product(db.Model):
#     """Tying a unique flow to the necessary products"""

#     __tablename__ = "flow_products"

#     fa_id = db.Column(db.Integer, db.ForeignKey('flow_acts.flow_act_id'), primary_key = True,)
#     prod_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key = True, )

#     flowacts = db.relationship('Flow_Activity')
#     products = db.relationship('Product')


# REFERENCE:
#    CREATE TABLE my_association (
#   user_id INTEGER REFERENCES user(id),
#   account_id INTEGER REFERENCES account(id),
#   PRIMARY KEY (user_id, account_id)
# )

class Product(db.Model):
    """Info on Products used for a Shower """

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    product_img = db.Column(db.String(75),)
    product_name = db.Column(db.String(25), nullable = False,)
    product_label_color = db.Column(db.String(20),)

    # act_prod_id = db.relationship('Activity_Product')

    def __repr__(self):
        return f'<Product id={self.product_id}, name={self.product_name}, \
                label color={self.product_label_color}>'


################ end of models ##################################

def connect_to_db(flask_app, db_uri='postgresql:///testing', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')