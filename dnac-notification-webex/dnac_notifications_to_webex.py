"""
This project creates communiction channel between WEBEX and DNAC.
From webex room, customer can send Event Notification requirements to BOT, then, BOT subscribes Event Notification to DNAC.
When there is new events like CPU outrage, DNAC will send notification to Webhook, then, BOT will transfer message to webex room.

Main functions:
1. In webex room, customer can send message including "Get subscriptions","Create subscriptions {EventID}", "Delete subscriptions {EventID}",
   "Show all Events Description" to BOT. Webex BOT will send requirements to its WEBEX_WEBHOOK_URL;
2. In WEBHOOK server, while receiving message from webex BOT, it can talk to DNAC based on message type;
3. In DNAC, when there is new event like CPU outrage, it will send notification information to its WEBHOOK server;
4. In WEBHOOK server, while receiving message from DNAC, it can transfer it to WEBEX room.
"""
import json
import requests
import env_dnac_webex
import api_dnac_webex
from requests.auth import HTTPBasicAuth
from flask import (Flask, request)

#Get variables from env_dnac_webex.py
WEBEX_URL = env_dnac_webex.WEBEX['WEBEX_URL']
WEBEX_TOKEN_BOT = env_dnac_webex.WEBEX['WEBEX_TOKEN_BOT']
WEBEX_ID_BOT = env_dnac_webex.WEBEX['WEBEX_ID_BOT']
WEBEX_ROOM_ID = env_dnac_webex.WEBEX['WEBEX_ROOM_ID']
WEBEX_WEBHOOK_URL = env_dnac_webex.WEBEX['WEBEX_WEBHOOK_URL']
DNAC_URL = env_dnac_webex.DNAC['DNAC_URL']
DNAC_PORT = env_dnac_webex.DNAC['DNAC_PORT']
DNAC_USER = env_dnac_webex.DNAC['DNAC_USER']
DNAC_PASSWORD = env_dnac_webex.DNAC['DNAC_PASSWORD']
DNAC_WEBHOOK_URL = env_dnac_webex.DNAC['DNAC_WEBHOOK_URL']
DNAC_TOKEN = env_dnac_webex.DNAC['DNAC_TOKEN']

app = Flask(__name__)

#handle message from webex room by BOT
@app.route("/webex-to-webhook", methods=["POST"])
def WebexInputAnalyse():
   if request.method == "POST":

### To get input information from webex, analyse it, then, process it according to different command.
       message_id = request.json["data"]["id"]
       url = "https://%s/v1/messages/%s"%(WEBEX_URL,message_id)
       payload = {}
       headers = {'Authorization': 'Bearer %s'%(WEBEX_TOKEN_BOT),'Content-Type': 'application/json'}

       response = requests.request("GET", url, headers=headers, data = payload)
       message = response.json()["text"].partition(" ")[2]

       if message.lower() == "help":
           message_out = "Please input:\\n \
           -------------\\n \
           1.  **Get subscriptions** : Get current Event Subscriptions;\\n \
           2.  **Create subscriptions {EventID}** : Create new Event Subscriptions;\\n \
           3.  **Delete subscriptions {EventID}** : Delete current Event Subscriptions;\\n \
           4.  **Show Events Description**"

#           message_out = "Please input:\\n1. \\\"**Get subscriptions**\\\" : Get current Event Subscriptions;\\n2. \\\"**Create subscriptions {EventID}**\\\" : Create new Event Subscriptions;\\n3. \\\"**Delete subscriptions {EventID}**\\\" : Delete current Event Subscriptions;\\n4. \\\"**Show Events Description**\\\""
           api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,message_out)

       elif message == "Get subscriptions":
           response = api_dnac_webex.GetEventSubscriptions()
           EventIdSub = []
           for EventId in response:
               EventIdSub.append(EventId["filter"]["eventIds"][0])

           api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"Subscribed EventId: **%s**"%(EventIdSub))

       elif "Create subscriptions" in message:
           eventId = message.split()[2]

           events_file = "dnac_events_id_name.json"
           with open(events_file) as f:
               events_data = json.load(f)

           if events_data.__contains__(eventId):    #Check whether evntId is valid.
               status_code, statusUri = api_dnac_webex.CreateEventSubscriptions(DNAC_WEBHOOK_URL,eventId)
               print(status_code,statusUri)
               if status_code == 200:
                   api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is successfully subscribed."%(eventId))
               elif status_code == 202:    #202 is for asynchronous process. DNAC always return 202.
                   api_status_id = statusUri["statusUri"].split("/")[7]    #Get the returned api-status task ID.
                   response = api_dnac_webex.CheckNotificationAPIStatus(api_status_id)    #Then check whether the task is finished.
                   print(response["apiStatus"])
                   if response["apiStatus"] == "SUCCESS":
                      api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is successfully subscribed."%(eventId))
                   else:
                      api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"Failed, please manually subscribe **%s** notification on DNAC GUI."%(eventId))
               else:
                   api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"Failed, please manually subscribe **%s** notification on DNAC GUI."%(eventId))
           else:
               api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is not valid. Please input valid eventId"%(eventId))

       elif "Delete subscriptions" in message:
           eventId = message.split()[2]

           events_file = "dnac_events_id_name.json"
           with open(events_file) as f:
               events_data = json.load(f)

           if events_data.__contains__(eventId):    #To check input first, if EventId is not valid, do nothing.
               status_code = api_dnac_webex.DeleteEventSubscriptions(eventId)
               if status_code == 200 or status_code == 204 or status_code == 202:    #After deleting, DNAC response with 200/202/204.
                   api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is deleted."%(eventId))
               elif status_code == 1000:    #
                   api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is not subscribed."%(eventId))
               else:
                   api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is not deleted."%(eventId))
           else:
               api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,"**%s** is not valid. Please input valid eventId"%(eventId))

       elif message == "Show Events Description":
            events_file = "dnac_events_id_name.json"     #This file stored almost all eventsId and its name for customer reference.
            with open(events_file) as f:
                events_data = f.read()    #Use read() but not json.load() because when there is "\", json.load() runs wrong.
            events = eval(repr(events_data).replace("\\\\","*"))    # Replace "\" in file to "*" because something is wrong to handle "\".
            events_dict = json.loads(events)
            message = {}
            for key,value in events_dict.items():
                key = "**"+key+"**"    # Add "**" to show BOLD text in webex room
                message[key] = value + "\\\n"
            api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,message)

   else:
       return "Please use POST method"

#handle event notification message from DNAC, then, sent it to webex room.
@app.route("/dnac-to-webhook", methods=["POST"])
def TransferToWebex():
    data = request.json
    issueTitle = data["details"]["Type"] + " " + data["details"]["Device"]
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]
    message = "**Warning Severity** %s (%s)! %s - %s" % (issueSeverity,issuePriority,issueTitle,issueSummary)

    api_dnac_webex.SendMessageToWebexRoom(WEBEX_ROOM_ID,message)

#Main procedure
if __name__ == '__main__':
    response_webex = api_dnac_webex.GetWebexWebhook()  #Check whether Webex Webhook exists

    Is_WebexWebhook = False
    for webhook_webex in response_webex["items"]:
        if webhook_webex["targetUrl"] == WEBEX_WEBHOOK_URL and webhook_webex["filter"] == "roomId=%s&mentionedPeople=%s"%(WEBEX_ROOM_ID,WEBEX_ID_BOT):
            Is_WebexWebhook = True
            break
    if not(Is_WebexWebhook): api_dnac_webex.CreateWebexWebhook() #If no webhook on webex, create new on. Otherwise, do nothing.

    DNAC_TOKEN = api_dnac_webex.GetDnacAuthToken() # Before service run, get DNAC token first. it's global variable for later use. If expired, API will update later.

    app.run(host="0.0.0.0", port=5000, ssl_context='adhoc', debug = True)    #Start flask HTTPS service
