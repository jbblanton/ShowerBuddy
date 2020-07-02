*READ ME*


Shower Buddy is a Flask web app that will guide a user with a cognitive impairment (from an intellectual or developmental disorder (I/DD), traumatic brain injury, or dementia, for example) through the process of taking a shower, enabling greater independence. 
A caregiver will create an account and enter basic information about the user to be stored in a database. Flask-SQLAlchemy simplifies storage and access to the PostgreSQL database. Caregivers can add additional users and routines as needed, or edit the existing routines. 
The front end is coded in JavaScript, with jQuery and AJAX transmitting data between the front and back ends. Integration of the Twilio API allows a user to press a “Help” button to alert the caregiver during the shower process.  
The site design is primarily achieved through usage of Bootstrap.

**************************************************
Current features:
- Account creation & storage
- Password hashing 
- Adding multiple users to a single account
- Editing existing users
- Twilio integrated alerts

Future features include: 
- Greater customization & personalization
- Refactoring onto a mobile app
- Integration of voice control
- Integration of physical buttons
- Integration of thermometer and alerts for water temperature


 **************************************************
 Steps: 
1. Source the secrets
2. Seed the database
3. Run!
