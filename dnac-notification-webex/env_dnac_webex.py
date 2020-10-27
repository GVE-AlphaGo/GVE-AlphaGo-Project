
"""
Functions: Define envrionment variables of WEBEX and DNAC.
Notes: Need to export "WEBEX_TOKEN_BOT" and "DNAC_PASSWORD" in enviroment.
"""
import os

WEBEX = {
  "WEBEX_URL" : "webexapis.com",
  "WEBEX_TOKEN_BOT" : os.environ["WEBEX_TOKEN_BOT"],
  "WEBEX_ID_BOT" : "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9iNWZhZmVhNi0xOWNhLTQ5OTQtYThhOC00MmE0NmM5OTIzNWQ",
  "WEBEX_ROOM_ID" : "Y2lzY29zcGFyazovL3VzL1JPT00vNTU1NTY3YjAtMDk1Ni0xMWViLWE1OTEtMDlkYWE3YjYxNTkz", #ROOM: GVE Alpha test
#  "WEBEX_ROOM_ID" : "Y2lzY29zcGFyazovL3VzL1JPT00vNjU5MzZkOTAtMDc3OS0xMWViLWFjYjQtZjljMzgzY2Y5ZDBm", #ROOM: GVE-innovation-test
  "WEBEX_WEBHOOK_URL" : "https://06f729f770d0.eu.ngrok.io/webex-to-webhook"
}

DNAC = {
  "DNAC_URL" : "10.75.53.95",
  "DNAC_PORT" : 8888,
  "DNAC_USER" : "admin",
  "DNAC_PASSWORD" : os.environ["DNAC_PASSWORD"],
  "DNAC_TOKEN" : "",
  "DNAC_WEBHOOK_URL" : "https://10.79.100.162/dnac-to-webhook",
  "DNAC_Endpoint_instanceId": "bdffecad-bbb5-40c5-90fa-096c0175d923"
}
