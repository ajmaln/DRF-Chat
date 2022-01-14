def request_to_bot():
    pass
def request_to_human():
    pass
def handoff_checking(data, user_profile):
    # Section --------- Handoff

    # To Start the Handoff
    if data['message'] == 'human':
        user_profile.update(handoff_to="human")
        user_profile.update(api_sent="N")
        
        # Todo: Send a response to human 
    elif data['message'] == 'bot':
        user_profile.update(handoff_to="bot" )
        user_profile.update(api_sent="N")
        # Todo: Send a response to bot
        
    # section : handoff running 
    x = user_profile[0]
    if x.get_handoff_to in ['bot', 'human'] and x.api_sent == 'N': # if api_sent == Y--> it will skip the handoff section
        if x.get_handoff_to == 'human':
            # user_profile.update(api_sent="Y")
            # request_to_human() # API
            return 'agent'
            # Cancel to sent the message to the bot 
        if  x.get_handoff_to == 'bot':
            user_profile.update(api_sent="Y")
            return "rasa-bot"
            request_to_bot() # API 

    
def receiver_checking(data, user_profile):
    # Section --------- Handoff

    # To Start the Handoff
    if data['message'] == 'human':
        user_profile.update(handoff_to="human")
        user_profile.update(api_sent="N")
        
        # Todo: Send a response to human 
    elif data['message'] == 'bot':
        user_profile.update(handoff_to="bot" )
        user_profile.update(api_sent="N")
        # Todo: Send a response to bot
        
    # section : handoff running 
    x = user_profile[0]
    if x.get_handoff_to in ['bot', 'human'] and x.api_sent == 'N': # if api_sent == Y--> it will skip the handoff section
        if x.get_handoff_to == 'human':
            return 'agent'
        if  x.get_handoff_to == 'bot':
            return "rasa-bot"



