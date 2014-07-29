

import json
from urllib2 import urlopen,Request
from uuid import uuid4 as get_guid
# from datetime import datetime as DT
# THE_PAST = DT(2014,1,2,12,30,0).isoformat()

BASE_URL = 'http://0.0.0.0:8080'

def post_json(all_data,p_url):
    json_data = json.dumps(all_data)
    headers = {'Content-type': 'application/json'}
    req = Request(p_url, json_data, headers)
    f = urlopen(req)
    response = f.read()
    f.close()
    return response

def new_pdf(show_post=False,show_resp=False):
    p_url = BASE_URL+'/test/'
    print '\t\tnew PDF','\n\t\t\tURL:',p_url

    guid = str(get_guid()).upper().replace('-','')
    incl_chars = set('ACEFGHJKLNPSTXZ347')
    order_tag = ''.join(c for c in guid if c in incl_chars)[:4]

    data = [{   "guid"          :   guid,
                "order_tag"     :   order_tag[:4],
                "QR_url"        :   order_tag[:4],
                "printer_id"    :   "Printer_"+guid[12:16],
                "machine_id"    :   "Machine_"+guid[4:8],
                "doc_name"      :   "Doc_"+guid[8:12],
            }]

    if show_post == True:
        print '\t\t\tJSON Posted:\n'
        print json.dumps(data, indent=4, sort_keys=True)

    resp = post_json(data,p_url)
    parsed = json.loads(resp)
    if show_resp == True:
        print '\t\t\tServer Response:\n'
        print json.dumps(parsed, indent=4, sort_keys=True)
    print '\n\t\t\t--> SUCCESS\n'
    return resp


import urllib2
import poster.encode
import poster.streaminghttp

def upload_pdf(uploadfile,upload_file_url,show_post=False,show_resp=False):
    print '\t\tupload_pdf -->',uploadfile,'\n\n\t\t\tURL:',upload_file_url

    opener = poster.streaminghttp.register_openers()

    params = {'local_document': open(uploadfile,'rb'), 'name': 'test_unit_1'}
    datagen, headers = poster.encode.multipart_encode(params)
    R = urllib2.Request(upload_file_url, datagen, headers)
    if show_resp == True:
        print '\t\t\tURL Post Request:\n'
        print '\t\t\tHeaders:\n\n\t\t\t\t',R.headers,'\n\n'
        print '\t\t\tTotal Size:\n\n\t\t\t\t',R.data.total,'\n\n'

    response = opener.open(R)

    if show_post == True:
        # parsed = json.loads(response)
        print '\t\t\tServer Response:\n'
        print response.read()
        # print json.dumps(parsed, indent=4, sort_keys=True)


    print '\n\t\t\t--> SUCCESS\n'
    return



print '\n\tTesting...\n'
print '\tBase URL:',BASE_URL,'\n'

uploadfile='/Users/admin/Desktop/test.pdf'
upload_file_url='http://aporo.ngrok.com'
upload_pdf(uploadfile,upload_file_url,show_post=True,show_resp=True)
# new_pdf(show_post=True,show_resp=True)

print '\n\tTesting COMPLETE\n'

