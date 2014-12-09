import json
from urllib2 import urlopen,Request
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from uuid import uuid4 as get_guid
from datetime import datetime as DT

def post_json(all_data,p_url,show_post=False,show_resp=False):

    if show_post == True:
        print '\t\t\tJSON Posted:\n'
        print json.dumps(all_data, indent=4, sort_keys=True)

    json_data   = json.dumps(all_data)
    headers     = {'Content-type': 'application/json'}
    req         = Request(p_url, json_data, headers)
    f           = urlopen(req)
    response    = f.read()
    f.close()

    if show_resp == True:
        try:
            parsed = json.loads(response)
            print '\t\t\tServer Response:\n'
            print json.dumps(parsed, indent=4, sort_keys=True)
        except:
            print '\nNON-JSON RESPONE\n\n\t\t\tServer Response:\n'
            print response

    return response

def printer_driver_check_in(base_url,post_action='',show_info='',show_post=False,show_resp=False):
    p_url   = base_url+'/api/check/'
    if show_info == 'show_info': print '\n\t\tTEST #1: printer driver check-in',post_action,'\n\t\t\tURL:',p_url
    guid    = str(get_guid())
    data = [{
              'pdf2_id'                  : guid,
              'printer_id'              : 'printer_id1',
              'machine_id'              : '12c61d88-5d0c-44af-a5fc-734f6327e1ec',        # authenticated client
               #'machine_id'            : 'admin1',                                    # authenticated admin
              # 'machine_id'              : 'vendor1',
              'application_name'        : 'application_name1',
              'doc_name'                : 'test_%s'%(DT.strftime(DT.now(),'%Y_%m_%d at %H:%M:%S'))
            }]

    resp = post_json(data,p_url,show_post,show_resp)
    if show_info == 'show_info': print '\n\t\t\t--> #1 SUCCESS\n'
    return True,resp,guid

def upload_pdf(guid,uploadfile,upload_file_url,show_info='',show_post=False,show_resp=False):
    if show_info == 'show_info': print '\t\tTEST #2: upload_pdf -->',uploadfile,'\n\n\t\t\tURL:',upload_file_url
    opener  = register_openers()

    params  = { 'local_document'    : open(uploadfile,'rb'),
                'pdf_id'            : guid  }

    datagen, headers = multipart_encode(params)
    R       = Request(upload_file_url, datagen, headers)

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

    if show_info == 'show_info': print '\n\t\t\t--> #2 SUCCESS\n'
    return True

def upload_test(base_url,show_info=''):#uploadfile,upload_file_url,show_info=False):

    uploadfile          =   '/Users/admin/aprinto/mgmt/test.pdf'
    upload_file_url     =   base_url
    if show_info        ==  'show_info':
        print '\n\tTesting Printer Driver Target URLs and PDF Upload\n'
        print '\tBase URL:',base_url,'\n'

    status,resp,guid    = printer_driver_check_in(base_url=base_url,post_action='',show_info=show_info,
                                              show_post=show_info,show_resp=show_info)
    upload_pdf(guid,uploadfile,upload_file_url,show_info=show_info,show_post=show_info,show_resp=show_info)

    if show_info        ==  'show_info':   print '\n\tTesting COMPLETE\n'
    return True

from sys import argv
if __name__ == '__main__':
    """
    Tests for Aprinto Server.

    Usage:

        python ~/aprinto/mgmt/tests.py local upload

        python ~/aprinto/mgmt/tests.py production upload show_info

    """

    if len(argv)==1:
        test_server         =   'production'
        test_tag            =   'upload'
        show_info           =   ''
    else:
        test_server         =   argv[1]
        test_tag            =   argv[2]
        show_info           =   '' if len(argv)!=4 else argv[3]

    show_info               =   True if show_info=='show_info' else False
    SERVERS = {'dev'        :   'http://0.0.0.0:8080',
               'local'      :   'http://192.168.3.52:8088',
               'ec2'        :   'http://54.88.101.190',
               'production' :   'http://printer.aporodelivery.com',
               'app'        :   'http://app.aporodelivery.com',}

    base_url                =   SERVERS[test_server]
    if   test_tag           ==  'upload':   upload_test(base_url,show_info)
    elif test_tag           ==  'download': download_test(base_url,show_info)

    print 'Success -- %s'%DT.strftime(DT.now(),'%Y_%m_%d at %H:%M:%S')




