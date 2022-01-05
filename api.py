import requests

body = {"sender": "test", "message": "hi"}
try:
    # Create a new resource
    rasa_response = requests.post('http://10.100.14.175:5001/webhooks/rest/webhook',\
        json = {"sender": "test", "message": "I want to see my account balance"}, \
    )
    print(rasa_response.text)
    print(rasa_response)

except Exception as e:
    print(e)


 
