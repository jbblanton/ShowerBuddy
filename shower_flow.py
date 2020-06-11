"""To Manage the State Machine"""

import timeit
# https://docs.python.org/3/library/timeit.html



## TO DO: Figure this part out! These should be separate functions called in
##    to the take_shower() action.

def create_shower_flow(flow_id):
    """Use this function to make a list of activities for a given user"""
    # Shower Flow = { step_num : 
    #                 activity_id:
    #                     activity_name:
    #                     description:
    #                     video:          }

    SELECT step_seq, activity_id FROM flows WHERE flow_id = flow_id
    => 1,2,3,4,5; 23, 24, 25, 16, 10


    activities = []

    return activities

def create_product_list(flow_id):
    """Use this to make a list of products needed during a given flow"""

    # Product = { product_id:
    #                 product_image:
    #                 product_name:
    #                 product_color_label:
    #             }

    products = []

    return products


def take_shower(flow_id):
    """Here is the actual shower flow. 

        'Activities' list will populate from the user's Flow.
        If statements control the order of the flow, and each activity is
        removed after completion. 
        Initial_rinse and Final_rinse are universal steps. """


    # With flow_id, get seq_step & that activity_id; 
    # With flow_id, get product_id

    # activities list = activity_names
    activities = create_shower_flow(flow_id)

    shower_active = True

    initial_rinse()

    while shower_active:

        if "shampoo" in activities:
            shampoo_hair(activity_id, product_id)
            activities.remove("shampoo")
            continue

        if "conditioner" in activities:
            condition_hair(activity_id, product_id)
            activities.remove("conditioner")
            continue

        if "bar soap" in activities:
            scrub_body_bar(activity_id, product_id)
            activities.remove("bar soap")
            continue

        if "liquid soap" in activities:
            scrub_body_liquid(activity_id, product_id)
            activities.remove("liquid soap")
            continue

        if "shave face" in activities:
            shave_face(activity_id, product_id)
            activities.remove("shave face")
            continue

        if "shave armpits" in activities:
            shave_armpits(activity_id, product_id)
            activities.remove("shave armpits")
            continue

        if "shave legs" in activities:
            shave_legs(activity_id, product_id)
            activities.remove("shave legs")
            continue

        shower_active = final_rinse()


####################### Activity Functions: ##################
def initial_rinse():
    """Get body and hair fully wet; Step #1 of ALL shower flows.
        ...
        ... 
        FUTURE FEATURE: have a version of initial_BODY_rinse for users
        who will not be washing their hair."""

        return True


def shampoo_hair(activity_id, product_id):
    """Shampoo hair"""

    # Declare state:
    print('<h2>Let\'s SHAMPOO our hair!</h2>')

    # Identify product:
    print('<img src="default_shampoo_bottle"></img> \
        <p>Get the shampoo and put some in your hand</p> \
        <img src="product in hand"></img>')

# How to start a timer?
# TO DO: Read docs on Timeit
    While time < 3 minutes:

    # Description of action:
        print('<p>Rub your hands together once and then put them on your head. Work the shampoo into your hair, rubbing your fingertips on your scalp.</p>')

    # Play video / gif of action:
        print('<video src="default_hair_lather"></video>')

    While time < 1.5 minutes:

    # Rinse hair:
        print('<p>Great! Now it\'s time to rinse your hair. Be sure to get all the shampoo out.</p>')
        print('<video src="generic rinse hair"></video>')

    print('<h2>Are you all done rinsing?</h2>')
        If <button> == False:
            Increment timer
        Else:
            exit and return to shower_flow

    return True


def condition_hair(activity_id):
    """Condition hair"""
    pass

def scrub_body_bar(activity_id):
    """Wash body with BAR SOAP"""
    pass

def scrub_body_liquid(activity_id):
    """Wash body with LIQUID SOAP"""
    pass

def shave_face():
    """Shave full face
        ...
        ...
        FUTURE FEATURE: Allow caregiver to call this action on it's own, 
            for those who do not shave their face in the shower."""
    pass

def shave_armpits():
    """Shave under arms"""
    pass

def shave_legs():
    """Shave legs"""
    pass

def final_rinse():
    """Final step in the flow and universal for ALL users.
        Completion of this function will mark shower_active as False 
        and exit the flow"""

    return False


>Start Shower<
    1. Start State: Initial Rinse
        Timer:
            "Next Step?"
                {Move to next State}
                If Shampoo == True
                    State 2
                Else If Condition == True
                    State 3
                Else:
                    State 4
            "More time?"
                {Increment timer}
                State 1
    2. State: Shampoo
        Timer:
            "Rinse your hair!"
            "Next Step?"
                {Move to next State}
                If Condition == True
                    State 3
                Else:
                    State 4
            "More time?"
                {Increment timer}
                State 2
    3. State: Condition
        Timer:
            "Rinse your hair!"
            "Next Step?"
                {Move to next State}
                State 4
            "More time?"
                {Increment timer}
                State 3
    4. State: Wash Body
        Timer:
            "Rinse your body!"
            "Next Step?"
                {Move to next State}
                If Shave Face == True
                    State 5
                Else If Shave armpits == True
                    State 6
                Else If Shave legs == True
                    State 7
                Else:
                    State 8 (final rinse)
            "More time?"
                {Increment timer}
                State 4
    5. State: Shave Face
        Timer:
            "Rinse your face!"
            "Next Step?"
                {Move to next State}
                If Shave armpits == True
                    State 6
                Else If Shave legs == True
                    State 7
                Else:
                    State 8 (final rinse)
            "More time?"
                {Increment timer}
                State 5
    6. State: Shave Armpits
        Timer:
            "Rinse your pits!"
            "Next Step?"
                {Move to next State}
                If Shave legs == True
                    State 7
                Else:
                    State 8 (final rinse)
            "More time?"
                {Increment timer}
                State 6
    7. State: Shave Legs
        Timer:
            "Rinse your Legs!"
            "Next Step?"
                {Move to next State}
                State 8 (final rinse)
            "More time?"
                {Increment timer}
                State 7
    8. State: Final Rinse
        Timer:
            "Rinse fully and make sure all the soaps are off!"
            "More time?"
                {Increment timer}
                State 8
            EXIT FLOW
            State: COMPLETE

At each transition, $get the <img> <video/gif> <instructions> for that step. Use default, unless there is an override for that user.
When new state:
    Declare state
    Show image
    Start timer
    Play video / gif

