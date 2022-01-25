## Rasa part start 


# importing the requests library
import requests
  
from multiprocessing import Process
import sys
from chat.models import User


# api-endpoint
RASA_URL = "http://localhost:5001/webhooks/rest/webhook"
CHAT_SYSTEM_URL = "http://localhost:8100/api/messages/"


def extract_rasa_response(data):
    PARAMS =  {
            "sender": data["sender"],
            "message": data["message"]
        }
    r = requests.post(url = RASA_URL, json = PARAMS)
    print("*"*100, '\n')
    print(type(r.text), r.text)
    bot_result =  eval(r.text)
    return bot_result

def call_rasa_bot(data, user_profile):
    
    # first submit the message to fin-agent
    p1 = Process(target = requests.post(url = f'{CHAT_SYSTEM_URL}9/4',\
                json=data))
    # then post the response to RASA Webhook 
    bot_result = extract_rasa_response(data)
    
    
    # sending get request and saving the response as response object
    
    bot_data_list = []
   
    print(bot_result, type(bot_result))
    # r = [{"recipient_id":"test","text":"Can you please type your account number?"}]
    for item in bot_result:
        print(item)
        bot_data = {
            "sender": "fin-agent",
            "receiver": item["recipient_id"],
            "message": item["text"],
            "timestamp": "1234454"
        }
        user_id = int(User.objects.get(username=item["recipient_id"]).pk)

        # process_list.append(f"requests.post(url = f'{CHAT_SYSTEM_URL}4/{user_id}',\
        #         json=bot_data)")
        bot_data_list.append(bot_data)
    user_profile.update(api_sent="N")
    # p1.start()
    for item in bot_data_list:
        print(item)
        p = Process(target = requests.post(url = f'{CHAT_SYSTEM_URL}4/{user_id}',\
                 json=item))
        p.start()
    
    

## rasa end

