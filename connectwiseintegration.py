import requests
import json
import datetime
import sys

COMPANY_ID = demisto.params()['COMPANY_ID']
APIKEY = demisto.params()['API_KEY']
URL = demisto.params()['URL']
headers = {
        'Authorization': "Basic {}".format(APIKEY),
        'clientId': "#ClientIDGeneratedInConnectWise#",
        "Content-Type":"application/json"
        }
payload = ''

if demisto.command() == 'Close_Ticket':
    path = "/v4_6_release/apis/3.0/service/tickets/"
    fullpath = URL + path
    ticket_num = demisto.args()['ticket_num']
    api_full_path = fullpath + "/" + ticket_num
    json1 = [{'op':'replace', 'path':'status', 'value':{'name':'Closed'}}]
    resp = requests.patch(api_full_path, json=json1, headers=headers)
    print('Updating Ticket....')
    resp = resp.json()
    demisto.results(resp)
    demisto.results("Ticket Closed In ConnectWise")
    sys.exit(0)

if demisto.command() == 'test-module':
    path = "/v4_6_release/apis/3.0/service/tickets/"
    fullpath = URL + path
    response = requests.post(fullpath, data=payload, headers=headers)
    demisto.results('ok')
    sys.exit(0)

if demisto.command() == 'Create_Ticket':
    # create ticket path

    path = "/v4_6_release/apis/3.0/service/tickets/"
    fullpath = URL + path
    ticket_name = demisto.args()['ticket_name']
    ticket_details = demisto.args()['ticket_details']
    connectwise_company_id = COMPANY_ID
    payload = " {\n\t\"summary\":\"DEMISTO ALERT: %s\",\n\t\"company\":{\"id\":%s}\n},\n\t\"initialDescription\":\"testinginitialdescriptionviademisto\"}" % (ticket_name,COMPANY_ID)
    response = requests.post(fullpath, data=payload, headers=headers)
    response = response.json()
    ## get ticket id from response Get comapany id and current time plus notes Before sending demisto results
    ticket_num = response['id']
    company_id = response['company']['id']
    now = datetime.datetime.now().isoformat()
    now = now[:-7]
    now = now + "Z"
    now = now.replace(".",":")
    ## below is notes that would go from demisto case into connectwise

    notes = 'created via demisto'
    ## adding response to war room

    demisto.results(response)
    demisto.results("Created Ticket...Adding Notes!")
    ########## adding notes to ticket that was created below

    notes_url = "/v4_6_release/apis/3.0/time/entries"
    updatepath = URL + notes_url
    ### time for ticket note entry

    payload2 = '''{\"timeStart\":\"%s\",
                          \"chargeToType\":\"ServiceTicket\",
                          \"chargeToId\":%s,
                          \"notes\":"%s" }''' % (now,ticket_num,ticket_details)

    time.sleep(1)
    response2 = requests.post(updatepath, data=payload2, headers=headers)
    #response2 = response.json()
    demisto.results(response2.json())
    demisto.results("Added Notes From Demisto Case To ConnectWise")
    sys.exit(0)

