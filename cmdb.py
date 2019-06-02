import requests
import json
from html.parser import HTMLParser
import base64
from time import sleep


requests.packages.urllib3.disable_warnings() 


def findServerInfo(serverName, cmdbUrl='https://cmdbmbr.ru137.corpintra.net/src/jsonrpc.php', apiKey=b'bTlhR2g='):
    # findServerInfo('S137KX001', 'https://cmdbmbr.ru137.corpintra.net/src/jsonrpc.php', '')
    apiKey=base64.b64decode(apiKey).decode('utf-8')
    HOSTNAME=serverName # "S137KX001" # "s926a111" "S137KX001"S137FWP004
    CMDBURL=cmdbUrl # "https://cmdbmbr.ru137.corpintra.net/src/jsonrpc.php" 
    HEADERS={'content-type': 'application/json'}
    PAYLOAD={"version": "2.0","method": "idoit.search","params": {"q": HOSTNAME,"apikey":apiKey,"language": "en"},"id": 1}

    SERVEROWNERS=''
    WorkInstructionLink=''

    # for parsing a rest response
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            #print("Start tag:", tag)
            if tag == 'a':
                for attr in attrs:
                    self.link=attr
                    #print(" attr:", attr)


    # SMTP server 53.151.100.102
    parser = MyHTMLParser()
    r=requests.post(CMDBURL, data=json.dumps(PAYLOAD),headers=HEADERS,verify=False)
    if r.status_code==200:# checking cmdb server status
        for _ in r.json()['result']:
            if _['value']==HOSTNAME:
                documentId=_['documentId']
                ans=_
                # PAYLOAD={"version": "2.0","method": "cmdb.object.read","params": {"id": documentId,"apikey": apiKey,"language": "en"},"id": 1}
                PAYLOAD['method']="cmdb.object.read"
                PAYLOAD['params']={"id": documentId,"apikey": apiKey,"language": "en"}
                r=requests.post(CMDBURL, data=json.dumps(PAYLOAD),headers=HEADERS,verify=False)
                if r.status_code==200:
                    #PAYLOAD={"version": "2.0","method": "cmdb.category.read","params": {"objID": documentId,"category": "C__CATG__CONTACT","apikey": apiKey,"language": "en"},"id": 1}
                    PAYLOAD['method']="cmdb.category.read"
                    PAYLOAD['params']={"objID": documentId,"category": "C__CATG__CONTACT","apikey": apiKey,"language": "en"}
                    r=requests.post(CMDBURL, data=json.dumps(PAYLOAD),headers=HEADERS,verify=False)
                    if r.status_code==200: # search for server owner primary contact
                        for _ in r.json()['result']:
                            if _['primary']['value'] is '1':
                                try:
                                    SERVEROWNERS=_['contact']['email_address'] # mail
                                except KeyError: # TypeError
                                    #PAYLOAD={"version": "2.0","method": "cmdb.category.read","params":\
                                    #            {"objID": _['contact_object']['id'],"category": "C__CATG__MAIL_ADDRESSES","apikey": apiKey,"language": "en"},"id": 1}
                                    PAYLOAD['params']={"objID": _['contact_object']['id'],"category": "C__CATG__MAIL_ADDRESSES","apikey": apiKey,"language": "en"}
                                    r=requests.post(CMDBURL, data=json.dumps(PAYLOAD),headers=HEADERS,verify=False)
                                    SERVEROWNERS=r.json()['result'][0]['primary_mail']
                    #PAYLOAD={"version": "2.0","method": "cmdb.category.read","params":\
                    #            {"objID": documentId,"category": "C__CATG__CUSTOM_FIELDS_WORKINSTRUKTIONS","apikey": apiKey,"language": "en"},"id": 1}
                    PAYLOAD['params']={"objID": documentId,"category": "C__CATG__CUSTOM_FIELDS_WORKINSTRUKTIONS","apikey": apiKey,"language": "en"}
                    r=requests.post(CMDBURL, data=json.dumps(PAYLOAD),headers=HEADERS,verify=False)
                    if r.status_code==200: # search for workinstruction
                        if ('error' in r.json()) or (r.json()['result'] == []):
                            pass
                            # print('Not found workinstruction')
                        else:
                            WIUrl=r.json()['result'][0]['f_text_c_1431089687177']
                            WIDescr=r.json()['result'][0]['description']
                            if WIUrl=='' or WIUrl=='TBD' or WIDescr!='': # or WIUrl!='TBD'
                                WorkInstructionLink=WIDescr
                            else:
                                parser.feed(WIUrl)
                                WorkInstructionLink=parser.link[1]
                else:
                    print(r.status_code,'<- status code ',r.text)
                break
        try:
            ans
        except NameError:
            print("suitable hostname was not found ,'ans' variable was NOT defined")
    else:
        print(r.text)
    return SERVEROWNERS.replace(',',';'),WorkInstructionLink


def fakeFunction(serverName, cmdbUrl='https://cmdbmbr.ru137.corpintra.net/src/jsonrpc.php', apiKey=b'bTlhR2g='):
    sleep(1)
    return "Sleep","WorkInstruction"
