# Webex-Bot-DNAC-Request

### Brief introduction:

This is a Webex Teams node.JS bot application that connect to DNAC and request information from DNAC. It features the [webex-node-bot-framework](https://github.com/webex/webex-bot-node-framework) that simplifies development for Webex Teams bots by abstractig away some of the complexity of the API calls and registering for events.  Some parts of the app are taken from on the old [sparkbotstarter](https://github.com/valgaze/sparkbotstarter) template created by Victor Algaze. 

## Prerequisites:

- [ ] node.js (minimum supported v8.0.0 & npm 2.14.12 and up)

- [ ] Sign up for Webex Teams (logged in with your web browser)


----

## Using guide:

1. Create a Webex Teams bot (save the API access token and username) https://developer.webex.com/my-apps/new/bot
		eg: API access token: MWIzMDY2NjctZDJjNi00ZjhhLWFjNzAtY2QwNzUwODhjMTQwOTM5ZjFjM2ItNzkz_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f
			Username: Alpha_Bot

2. Install nGrok, then connect and start it on your machine https://ngrok.com/download

3. Run nGrok on your machine to get a public ip address, `ngrok http 7001 --region=eu`
		eg: Public IP address: http://6547f98d60f7.eu.ngrok.io
			Port number: 7001

4. Edit  "config.json" with the following values:
		token: Set this to the token that you got in step 1
		port: Set this to the port number that you got in step 3
		webhookUrl: Set this to the public IP address that you got in step 3

5. Edit "index.js", correct object "tokenHeader" and "netDeviceHeader" with your DNAC URLs and authorization info. 


6. Create a space in Webex teams and add bot to the space

7. Run the Bot with `npm start`
	
