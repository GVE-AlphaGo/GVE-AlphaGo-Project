"""
Functions: Define modules to interoperate with WEBEX and DNAC.
"""
import json
import requests
import env_dnac_webex
from requests.auth import HTTPBasicAuth

WEBEX_URL = env_dnac_webex.WEBEX['WEBEX_URL']
WEBEX_TOKEN_BOT = env_dnac_webex.WEBEX['WEBEX_TOKEN_BOT'] #DNAC_Bot Token
WEBEX_ID_BOT = env_dnac_webex.WEBEX['WEBEX_ID_BOT'] #DNAC_Bot ID
WEBEX_ROOM_ID = env_dnac_webex.WEBEX['WEBEX_ROOM_ID'] #GVE-innovation-project rooms id
WEBEX_WEBHOOK_URL = env_dnac_webex.WEBEX['WEBEX_WEBHOOK_URL']
DNAC_URL = env_dnac_webex.DNAC['DNAC_URL']
DNAC_PORT = env_dnac_webex.DNAC['DNAC_PORT']
DNAC_USER = env_dnac_webex.DNAC['DNAC_USER']
DNAC_PASSWORD = env_dnac_webex.DNAC['DNAC_PASSWORD']
DNAC_WEBHOOK_URL = env_dnac_webex.DNAC['DNAC_WEBHOOK_URL']
DNAC_TOKEN = env_dnac_webex.DNAC['DNAC_TOKEN']
DNAC_Endpoint_instanceId = env_dnac_webex.DNAC['DNAC_Endpoint_instanceId']

#GET webex webhooks detais. In main function, if exists, then do nothing, otherwise to create the webhook.
def GetWebexWebhook():
    url = "https://%s/v1/webhooks"%(WEBEX_URL)
    headers = {
      'Authorization': 'Bearer %s'%(WEBEX_TOKEN_BOT),
      'Content-Type': 'application/json'
    }
    payload = None

    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()

#Create webex webhook, define filter of roomid and message sent to the BOT.
def CreateWebexWebhook():
    url = "https://%s/v1/webhooks"%(WEBEX_URL)
    headers = {
      'Authorization': 'Bearer %s'%(WEBEX_TOKEN_BOT),
      'Content-Type': 'application/json'
    }
    payload = '''{
        "name": "Webex Webhook",
        "targetUrl": "%s",
        "resource": "messages",
        "event": "created",
        "filter": "roomId=%s&mentionedPeople=me"
      }'''%(WEBEX_WEBHOOK_URL,WEBEX_ROOM_ID)

    response = requests.request("POST", url, headers=headers, data = payload)
    return response.json()

###Get DNAC token
def GetDnacAuthToken():
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """
    login_url = "https://{0}:{1}/dna/system/api/v1/auth/token".format(DNAC_URL, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return token

#Create event subscriptions on DNAC.
def CreateEventSubscriptions(webhookURL,eventID):
    global DNAC_TOKEN
    token = DNAC_TOKEN
    url = "https://{0}:{1}/dna/intent/api/v1/event/subscription".format(DNAC_URL,DNAC_PORT)

    payload = '''[
      {
        "name": "Event_%s",
        "subscriptionEndpoints": [
            {
                "instanceId": "%s",
                "subscriptionDetails": {
                    "name": "Event_%s",
                    "url": "%s",
                    "method": "POST",
                    "connectorType": "REST"
                }
            }
        ],
        "filter": { "eventIds": ["%s"] }
      }
    ]'''%(eventID,DNAC_Endpoint_instanceId,eventID,webhookURL,eventID)

#If the current token is still valid, then, not need to do GetDnacAuthToken, otherwise, to
#get new token, and update the global TOKEN value.
    i = 1
    while i == 1:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-token" : token
        }

        response = requests.request('POST', url, headers=headers, data=payload, verify=False)
        if response.status_code == 401:
            token = GetDnacAuthToken()
            DNAC_TOKEN = token
        else:
            i = 0

    return response.status_code,response.json()

def CheckNotificationAPIStatus(api_status_id):
    global DNAC_TOKEN
    token = DNAC_TOKEN
    url = "https://{0}:{1}/dna/intent/api/v1/event/api-status/{2}".format(DNAC_URL,DNAC_PORT,api_status_id)

    payload = None

#If the current token is still valid, then, not need to do GetDnacAuthToken, otherwise, to
#get new token, and update the global TOKEN value.
    i = 1
    while i == 1:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-token" : token
        }

        response = requests.request('GET', url, headers=headers, data=payload, verify=False)
        if response.status_code == 401:
            token = GetDnacAuthToken()
            DNAC_TOKEN = token
        else:
            i = 0

    return response.json()

#Get DNAC event subscriptions information.
def GetEventSubscriptions():
    global DNAC_TOKEN
    token = DNAC_TOKEN
    url = "https://{0}:{1}/dna/intent/api/v1/event/subscription".format(DNAC_URL,DNAC_PORT)
    payload = None

    i = 1
    while i == 1:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-token" : token
        }

        response = requests.request('GET', url, headers=headers, data=payload, verify=False)
        if response.status_code == 401:
            token = GetDnacAuthToken()
            DNAC_TOKEN = token
        else:
            i = 0

    return response.json()

#Get DNAC event subscriptions information.
def GetEventSubscriptionsByID(eventId):
    global DNAC_TOKEN
    token = DNAC_TOKEN
    url = "https://{0}:{1}/dna/intent/api/v1/event/subscription?eventIds={2}".format(DNAC_URL,DNAC_PORT,eventId)
    payload = None

    i = 1
    while i == 1:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-token" : token
        }

        response = requests.request('GET', url, headers=headers, data=payload, verify=False)
        if response.status_code == 401:
            token = GetDnacAuthToken()
            DNAC_TOKEN = token
        else:
            i = 0

    return response.json()

#Delete subscriptions. Before deletion, check whether the event subscription exist.
def DeleteEventSubscriptions(eventId):
    global DNAC_TOKEN
    token = DNAC_TOKEN
    response = GetEventSubscriptionsByID(eventId)
    if response == []:
        return 1000

    subscriptionId = response[0]["subscriptionId"]
    url = "https://{0}:{1}/dna/intent/api/v1/event/subscription?subscriptions={2}".format(DNAC_URL,DNAC_PORT,subscriptionId)
    payload = None

    i = 1
    while i == 1:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-token" : token
        }

        response = requests.request('DELETE', url, headers=headers, data=payload, verify=False)
        if response.status_code == 401:
            token = GetDnacAuthToken()
            DNAC_TOKEN = token
        else:
            i = 0

    return response.status_code

#Send message to webex room.
def  SendMessageToWebexRoom(roomid,message):
    url = "https://%s/v1/messages"%(WEBEX_URL)
    payload = '''
      {
        "roomId": "%s",
        "markdown": "%s"
      }
    '''%(roomid,message)
#    "{\n  \"roomId\": {roomid},\n  \"text\": {message}\n}".format(roomid=roomid,message=message)
    headers = {
      'Authorization': 'Bearer %s'%(WEBEX_TOKEN_BOT),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)

#Get all current evnets from DNAC. Do it before app runs.
def GetAllEventsId_to_file():
        global DNAC_TOKEN
        token = DNAC_TOKEN
        tags = ["ASSURANCE","License%20Management","CIMC","ITSM","ISE_ERS","IPAM","DR"]
        eventsId_all = {}

        for tag in tags:
            url = "https://{0}:{1}/dna/intent/api/v1/events?tags={2}&limit=200".format(DNAC_URL,DNAC_PORT,tag)
            payload = None

            k = 1
            while k == 1:
                headers = {
                  "Content-Type": "application/json",
                  "Accept": "application/json",
                  "X-auth-token" : token
                }
            response = requests.request('GET', url, headers=headers, data=payload, verify=False)
            if response.status_code == 401:
                token = GetDnacAuthToken()
                DNAC_TOKEN = token
            else:
                k = 0

            for i in range(len(response.json())):
               key1 = response.json()[i]["eventId"]
               value1 = response.json()[i]["name"]
               eventsId_all[key1] = value1

        json = json.dumps(eventsId_all)
        f = open("dnac_events_id_name.json","w")
        f.write(json)
        f.close()
