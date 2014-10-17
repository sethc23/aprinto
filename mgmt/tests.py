from sys import argv
import json
from urllib2 import urlopen,Request
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from uuid import uuid4 as get_guid
from datetime import datetime as DT
from uuid import getnode as get_mac

macs = {'Macbook':'105773427819682',
        'MacBookPro':'117637351435',}

this_mac = str(get_mac())

def post_json(all_data,p_url,show_post=False,show_resp=False):

    if show_post == True:
        print '\t\t\tJSON Posted:\n'
        print json.dumps(all_data, indent=4, sort_keys=True)

    json_data = json.dumps(all_data)
    headers = {'Content-type': 'application/json'}
    req = Request(p_url, json_data, headers)
    f = urlopen(req)
    response = f.read()
    f.close()

    if show_resp == True:
        parsed = json.loads(response)
        print '\t\t\tServer Response:\n'
        print json.dumps(parsed, indent=4, sort_keys=True)

    return response

def check(post_action='',show_post=False,show_resp=False):
    p_url = BASE_URL+'/api/check/'
    print '\n\t\tTEST: check',post_action,'\n\t\t\tURL:',p_url
    guid = str(get_guid())
    data = [{
              'pdf_id' : guid,
              'printer_id' : 'printer_id1',
              'machine_id' : 'machine_id1',
              'application_name' : 'application_name1',
              'doc_name' : 'test_unit_1'
            }]

    resp = post_json(data,p_url,show_post,show_resp)
    print '\n\t\t\t--> SUCCESS\n'
    return guid

def upload_pdf(guid,uploadfile,upload_file_url,show_post=False,show_resp=False):
    print '\t\tTEST: upload_pdf -->',uploadfile,'\n\n\t\t\tURL:',upload_file_url
    opener = register_openers()

    params = {'local_document': open(uploadfile,'rb'),
              'pdf_id' : guid}

    datagen, headers = multipart_encode(params)
    R = Request(upload_file_url, datagen, headers)

    if show_resp == True:
        print '\n\n\t\t\tURL Post Request:'
        print '\n\t\t\t\tHeaders:'
        print '\n\t\t\t\t\t',R.headers,'\n'
        print '\n\t\t\t\tParams:'
        print '\n\t\t\t\t\t',params,'\n'
        print '\t\t\t\tTotal Size:'
        print '\n\t\t\t\t\t',R.data.total,'\n'

    response = opener.open(R)

    if show_post == True:
        print '\n\t\t\tServer Response:'
        print '\n\t\t\t\t',response.read(),'\n'

    print '\n\t\t\t--> SUCCESS\n'
    return

if __name__ == '__main__':
    try:
        test_server = argv[1]
    except:
        # test_server = 'dj_dev'
        test_server = 'local'
        # test_server = 'ec2'

    THE_PAST = DT(2014,1,2,12,30,0).isoformat()

    SERVERS = {'dev'    :   'http://0.0.0.0:8080',
               'local'  :   'http://0.0.0.0',
               'ec2'    :   'http://54.191.47.76',
               'ec3'    :   'http://54.186.48.182',
               'printer':   'http://printer.aporodelivery.com',
               'app'    :   'http://app.aporodelivery.com',}

    BASE_URL = SERVERS[test_server]

    print '\n\tTesting "'+test_server+'"...\n'
    print '\tBase URL:',BASE_URL,'\n'

    guid = check(post_action='',show_post=True,show_resp=True)
    if this_mac == macs['Macbook']: uploadfile='/Users/sethchase/Desktop/test.pdf'
    if this_mac == macs['MacBookPro']: uploadfile='/Users/admin/Desktop/test.pdf'

    upload_file_url=BASE_URL
    upload_pdf(guid,uploadfile,upload_file_url,show_post=True,show_resp=True)

    print '\n\tTesting COMPLETE\n'

