"""Models for the Shower Buddy app"""

from flask_sqlalchemy import SQLAlchemy

sb_db = SQLAlchemy()

# ** To do: figure out how to prevent all these ids from getting jumbled!
# Can there be a connection between 2 (eg: cg_id = 12, user_id = 12.1 ?)
# Can the incrementing start at a certain point, or start with min digits?

class Caregiver(db.Model):
    """A Caregiver"""

    __tablename__ = "caregivers"

    caregiver_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    email = db.Column(db.String(50), unique = True, nullable = False,)
    password = db.Column(db.String(25), nullable = False,)
    telephone = db.Column(db.String(10),)

    user = db.relationship('User')

    def __repr__(self):
        return f'<Caregiver caregiver_id={self.caregiver_id}, \
                email={self.email}, phone={self.telephone}>'


class User(db.Model):
    """A User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    user_name = db.Column(db.String(50), nullable = False,)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # Should the Flow.title be nullable? is there a way to set a default? 
    # At least set a suggestion ("daily shower"), along with a suggested flow.

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
    description = db.Column(db.Text,)
    activity_video = db.Column(db.Text,)

    flow_act = db.relationship('Flow_Activity')

    def __repr__(self):
        return f'<Activity id={self.activity_id}, description={self.description}, \
                video={self.activity_video}>'

class Activity_Product(db.Model):
    """Connector table between Activities & Products """

    __tablename__ = "activity_products"

    act_prod_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    activity = db.relationship('Activity')
    product = db.relationship('Product')

    def __repr__(self):
        return f'<Act_Prod id={self.act_prod_id}, activity_id={self.activity_id}, \
                product_id={self.product_id}>' 


class Product(db.Model):
    """Info on Products used for a Shower """

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key = True, autoincrement = True,)
    product_img = db.Column(db.String(75),)
    product_name = db.Column(db.String(25), nullable = False,)
    product_label_color = db.Column(db.String(20),)

    act_prod_id = db.relationship('activity_products.act_prod_id')

    def __repr__(self):
        return f'<Product id={self.product_id}, name={self.product_name}, \
                label color={self.product_label_color}>'