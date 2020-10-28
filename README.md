# GVE AlphaGo —— Smart Assistance of Network Administrator

## Introduction

This is the project created by GVE AlphaGo team.

Our project aims to provide customization of network visibility through a friendly interactive interface - Webex Teams bots who are able to connect to DNAC, push notification and retrieve information from DNAC. Instead of grabbing and filtering unrelated information from DNAC Dashboard manually, *Smart Assistance of Network Administrator* offers a more convenient and flexible approach to access data no matter where you are or which device you utilize.

This is the example code using Northbound APIs to accomplish the network visibility. Main functions are composed of two coding sections: Initiative notification from DNAC platform is delivered by Python after users select the needed event subscriptions. On the other hand, users are also capable of querying information from DNAC by communicating with our Webex Teams node.JS bot.

## Team Member

- Jianteng Gao
- Lina Su
- Yunqian Xia
- Yecheng Song

## Use Case Description

Network admin often tired to use the DNAC dashboard to see the basic information about network environment. Usually what they need is only part of the information, not all of the information provided by DNAC. Therefore we develop a webex bot app to help simplify this process. Network administrator only need to input what they want to know and then the information can be displayed in Webex Teams chat space. Furthermore, if there are some critical issues happen, it will also push notification to webex bot or email and IT staff can be informed as soon as possible.

## ScreenShot from the project 
 
![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture1.png)

![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture2.png)

![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture3.png)

![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture4.png)

![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture5.png)

## Topology 

DNAC-notification-to-Webex process
![image](https://github.com/GVE-AlphaGo/GVE-AlphaGo-Project/blob/main/images/Picture6.png)
 
 
## Prerequisites

•	 node.js (minimum supported v8.0.0 & npm 2.14.12 and up)

•	 Sign up for Webex Teams (logged in with your web browser)

•	DNA Center: Version 2.1.2.0

•	Python 3.8.1

•	nGrok

 
## Installation & Configuration 

This Example Code is composed of 2 modules, each module can be used independently. you can choose the module that you want to demo.

### Module 1 : Webex-Bot-DNAC-Request

This is a Webex Teams node.JS bot application that connect to DNAC and request information from DNAC. It features the webex-node-bot-framework that simplifies development for Webex Teams bots by abstractig away some of the complexity of the API calls and registering for events. Some parts of the app are taken from on the old sparkbotstarter template created by Victor Algaze.

1.	Create a Webex Teams bot (save the API access token and username) https://developer.webex.com/my-apps/new/bot eg: API access token: MWIzMDY2NjctZDJjNi00ZjhhLWFjNzAtY2QwNzUwODhjMTQwOTM5ZjFjM2ItNzkz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f Username: Alpha_Bot

2.	Install nGrok, then connect and start it on your machine https://ngrok.com/download

3.	Run nGrok on your machine to get a public ip address, "ngrok http 7001 --region=eu" eg: Public IP address: http://6547f98d60f7.eu.ngrok.io Port number: 7001

4.	Edit "config.json" with the following values: token: Set this to the token that you got in step 1 port: Set this to the port number that you got in step 3 webhookUrl: Set this to the public IP address that you got in step 3

5.	Edit "index.js", correct object "tokenHeader" and "netDeviceHeader" with your DNAC URLs and authorization info.

6.	Create a space in Webex teams and add bot to the space

7.	Run the Bot with "npm start"

### Module 2:  DNAC_notification_to_WEBEX

This module mainly focus on how to push notification from DNAC dashboard to Webex Teams. 
On Webex Teams, after input "GO_Bot help", there will be four functions: 

* Get subscriptions : Get current Event Subscriptions;

* Create subscriptions {EventID} : Create new Event Subscriptions;

* Delete subscriptions {EventID} : Delete current Event Subscriptions;

* Show Events Description

Steps to get the Webex BOT working with DNAC

For Webex Teams, create a Webex Teams bot (save the API access token and username): https://developer.webex.com/my-apps/new/bot. 
On Webex Teams, create a team /space, save the ROOM ID;

1.	For your PC, Sign up for nGrok, then connect and start it on your machine (save the port number and public web address: https://ngrok.com/download After installing ngrok, run it on your local machine to get a public ip address, eg ./ngrok http https://localhost:5000 -host-header="localhost:5000" --region=eu. Copy the ip address displayed in the ngrok window, ie: : https://01b836a0e476.eu.ngrok.io

2.	For DNA center, need to create new instance for Webhook. Try to get its instanceId from POSTMAN;

* Not found DNAC API interface to create instance for Webhook. So, need to manually create it.

* While creating events subscriptions by DNAC API, need to input Webhook "instanceId", so, need to get it in advance.

3.	There are four files to be used:

* env_dnac_webex.py Environment variables. WEBEX_TOKEN_BOT and DNAC_PASSWORD value is stored in system OS env. WEBEX_WEBHOOK_URL is ngrok + 'webex-to-webhook'. DNAC_WEBHOOK_URL with above ngrok doesn't work perhaps due to the block on cisco device. Here, use the private IP address.DNAC_Endpoint_instanceId is the webhook instanceId. It's manullay created on DNAC. Not found corresponding DNAC API.

* api_dnac_webex.py Define all related modules to talk with Webex and DNAC API interface.

* dnac_events_id_name.json Includes almost all DNAC EventsId and its NAME for customer reference. It's generated by DNAC API interface.

* dnac_notifications_to_webex.py Main procedure. Use python flask as server.

## Demo Video 
https://youtu.be/JtuGCaeahSM


