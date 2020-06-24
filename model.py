"""Models for the Shower Buddy app"""

import os
from flask_sqlalchemy import SQLAlchemy
import server
from flask_login import UserMixin



db = SQLAlchemy()


################# Models & Info ##################################

class Caregiver(UserMixin, db.Model):
    """A Caregiver
        Trying again to use Flask-Login"""

    __tablename__ = "caregivers"

    caregiver_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    caregiver_name =db.Column(db.String(25),)
    email = db.Column(db.String(50), unique = True, nullable = False,)
    password = db.Column(db.String(200), nullable = False,)
    telephone = db.Column(db.String(12),)

    users = db.relationship('User')


    def __repr__(self):
        return f'<Caregiver caregiver_id={self.caregiver_id}, email={self.email}, phone={self.telephone}>' 


    def check_if_registered(email):
        """Check if a caregiver is already registered;
            cg will either contain that Caregiver object 
            else equal None"""

        cg = db.session.query(Caregiver).filter(Caregiver.email == email).first()

        return cg

# Written to override the default method from UserMixin:
    def get_id(self):
        try:
            return str(self.caregiver_id)
        except AttributeError:
            raise NotImplementedError('No `caregiver_id` attribute - override `get_id`')


class User(db.Model):
    """A Client, aka: the end-User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    user_name = db.Column(db.String(50), nullable = False,)
    user_body = db.Column(db.String(20),)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregivers.caregiver_id'))


    caregiver = db.relationship('Caregiver')
    flow = db.relationship('Flow')

    def __repr__(self):
        return f'<Client client_name={self.client_name} client_id={self.client_id} user_id={self.caregiver_id}>'


    def check_if_client():
        """Look for the combo of user name & body + caregiver
            Goal: prevent duplication; redirect to "add a flow" """

        pass

    def check_if_user():
        """Look for the combo of user name & body + caregiver
            Goal: prevent duplication; redirect to "add a flow" """

        pass


class Flow(db.Model):
    """A user's shower routine"""

    __tablename__ = "flows"

    flow_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    title = db.Column(db.String(60),)
    duration = db.Column(db.Integer,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User')

    def __repr__(self):
        return f'<Flow flow_id={self.flow_id}, title={self.title}, user={self.user.user_name}>' 


class Flow_Activity(db.Model):
    """Connector table between Flow & Activities"""

    __tablename__ = "flow_acts"

    flow_act_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    seq_step = db.Column(db.Integer, nullable = True,)
    flow_id = db.Column(db.Integer, db.ForeignKey('flows.flow_id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))

    flow = db.relationship('Flow')
    activity = db.relationship('Activity')

    def __repr__(self):
        return f'<Flow_Activity flow_act_id={self.flow_act_id},  step in sequence={self.seq_step}>'


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
        return f'<Activity id={self.activity_id}, description={self.description}, video={self.activity_video}>'


class Flow_Product(db.Model):
    """Tying a unique flow to the necessary products"""

    __tablename__ = "flow_products"
    __table_args__ = (db.UniqueConstraint('fa_id', 'prod_id', name="flow_prod_id"),)
    
    flow_prod_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    fa_id = db.Column(db.Integer, db.ForeignKey('flow_acts.flow_act_id'),)
    prod_id = db.Column(db.Integer, db.ForeignKey('products.product_id'),)

    flowacts = db.relationship('Flow_Activity')
    products = db.relationship('Product')


class Product(db.Model):
    """Info on Products used for a Shower """

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    product_img = db.Column(db.String(75),)
    product_name = db.Column(db.String(25), nullable = False,)
    product_label_color = db.Column(db.String(20),)

    # act_prod_id = db.relationship('Activity_Product')

    def __repr__(self):
        return f'<Product id={self.product_id}, name={self.product_name}, label color={self.product_label_color}>'


################ end of models ##################################


def connect_to_db(flask_app, db_uri='postgresql:///testing', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print("Connected to DB.")