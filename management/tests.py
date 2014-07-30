

import json
from urllib2 import urlopen,Request
from uuid import uuid4 as get_guid
from aprinto.settings import BASE_PRINTER_URL,BASE_QR_URL,INCL_CHARS
# from datetime import datetime as DT
# THE_PAST = DT(2014,1,2,12,30,0).isoformat()

# def post_json(all_data,p_url):
#     json_data = json.dumps(all_data)
#     headers = {'Content-type': 'application/json'}
#     req = Request(p_url, json_data, headers)
#     f = urlopen(req)
#     response = f.read()
#     f.close()
#     return response

# def new_pdf(show_post=False,show_resp=False):
#     p_url = BASE_PRINTER_URL+'/test/'
#     print '\t\tnew PDF','\n\t\t\tURL:',p_url
#
#     guid = str(get_guid()).upper().replace('-','')
#     data = [{   "guid"          :   guid,
#                 "printer_id"    :   "Printer_"+guid[12:16],
#                 "machine_id"    :   "Machine_"+guid[4:8],
#                 "doc_name"      :   "Doc_"+guid[8:12],
#                 "doc_path"      :   "Doc_"+guid[8:12],
#             }]
#
#     if show_post == True:
#         print '\t\t\tJSON Posted:\n'
#         print json.dumps(data, indent=4, sort_keys=True)
#
#     resp = post_json(data,p_url)
#     parsed = json.loads(resp)
#     if show_resp == True:
#         print '\t\t\tServer Response:\n'
#         print json.dumps(parsed, indent=4, sort_keys=True)
#     print '\n\t\t\t--> SUCCESS\n'
#     return resp


import urllib2
import poster.encode
import poster.streaminghttp

def upload_pdf(uploadfile,upload_file_url,show_post=False,show_resp=False):
    print '\t\tupload_pdf -->',uploadfile,'\n\n\t\t\tURL:',upload_file_url

    opener = poster.streaminghttp.register_openers()

    # guid = str(get_guid()).upper().replace('-','')

    params = {'local_document': open(uploadfile,'rb'),
              'pdf_id' : get_guid(),
              'printer_id' : 'printer_id1',
              'machine_id' : 'machine_id1',
              'application_name' : 'application_name1',
              'doc_name' : 'test_unit_1'}

    datagen, headers = poster.encode.multipart_encode(params)
    R = urllib2.Request(upload_file_url, datagen, headers)
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
        # parsed = json.loads(response)
        print '\n\t\t\tServer Response:'
        print '\n\t\t\t\t',response.read(),'\n'
        # print json.dumps(parsed, indent=4, sort_keys=True)


    print '\n\t\t\t--> SUCCESS\n'
    return



print '\n\tTesting...\n'
print '\tBase URL:',BASE_PRINTER_URL,'\n'

# uploadfile='/Users/admin/Desktop/test.pdf'
uploadfile='/Users/sethchase/Desktop/test.pdf'
upload_file_url=BASE_PRINTER_URL
upload_pdf(uploadfile,upload_file_url,show_post=True,show_resp=True)
# new_pdf(show_post=True,show_resp=True)

print '\n\tTesting COMPLETE\n'

