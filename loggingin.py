"""A file to manage the Login information"""

from flask_login import LoginManager, UserMixin



from flask_login import (LoginManager, login_user, login_required, logout_user)
### For using the flask_login tools:
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(caregiver_id):
    return Caregiver.query.get(int(caregiver_id))




from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.validators import InputRequired, Email, Length

### Flask_Login class ###

class LoginForm(FlaskForm):
    """Created for use with flask_login"""

    caregiver_email = StringField('caregiver_email', 
        validators=[InputRequired(), Length(min=4, max=50)])
    caregiver_password = PasswordField('caregiver_password', 
        validators=[InputRequired(), Length(min=8, max=30)])
    remember = BooleanField('Remember me')


#### End Flask_Login ###