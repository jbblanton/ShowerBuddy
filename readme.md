*READ ME*


This is a webapp designed to enable those with intellectual or developmental disabiliies (aka: I/DD) to shower independently. 
A "caregiver" (parent, live-in, AFL, staff, etc.) will create an account and set up a shower routine for a person, "user".
When it's time for a shower, the caregiver will select an associated user and start a shower routine that will play through a timed sequence.

**************************************************

Future features include: 
- Refactoring onto a mobile app (undecided at this time) to allow actual usage 
- Integration of voice control
- Integration of physical buttons
- Integration of thermometer and alerts for water temperature
- Tintegration of Twilio for the purpose of alerting the caregiver to an SOS or error
- Greater customization (expressed in many ways)



 **************************************************
 Steps: 
1. Seed the database
2. Confirm things in $psql testing
3. Run!


Notes: 
Currently working on branch <nologin> due to difficulties with Flask_login; Hope to revisit and merge in the next week.