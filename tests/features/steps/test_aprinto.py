from behave import *
from hamcrest import assert_that, equal_to, is_not
from sys import path as py_path
py_path.append('/Users/admin/SERVER3/aprinto')
from os import environ as os_environ
os_environ.setdefault("DJANGO_SETTINGS_MODULE", "aprinto.settings")

from uuid import uuid4 as get_guid
from urllib2 import urlopen,Request
import requests
from api.serializers import Initial_PDF_serializer
import pandas as pd
from sqlalchemy import create_engine

test_url = '192.168.3.52'
BASE_URL = 'http://'+test_url+':8088'

engine_url = 'postgresql://postgres:postgres@'+test_url+':8800/aprinto'
engine = create_engine(engine_url,encoding='utf-8',echo=False)

@given('data for posting to Aporo')
def step_impl(context):
    headers             =   {'Content-type' :   'application/json'}
    context.data        =   {'json':[{
                                  'pdf_id'              : str(get_guid()),
                                  'printer_id'          : 'printer_id1',
                                  'machine_id'          : 'vendor1',
                                  'application_name'    : 'application_name1',
                                  'doc_name'            : 'test_unit_1'
                                    }],
                             'headers'      :   headers}

@when('the data is valid')
def step_impl(context):
    t                       =   Initial_PDF_serializer(data=context.data['json'],many=True)
    assert_that(t.is_valid(),equal_to(True),str(context.data['json'][0])+'\n'+str(t.errors))

@when('the data is posted to Aporo')
def step_impl(context):
    p_url                   =   BASE_URL+'/api/check/'
    req                     =   requests.request('POST',p_url,**context.data)
    assert_that(req.reason,equal_to("CREATED"))
    context.req             =   req

@then('Aporo creates a New Order')
def step_impl(context):
    cnt                     = pd.read_sql("""   select count(*) c from aprinto_pdf
                                                where pdf_id = '%s'
                                          """%context.data['json'][0]['pdf_id'],engine).c[0]
    assert cnt is not 0

@then('Aporo returns an Order Tag, a Post Url, and QR code information')
def step_impl(context):
    T                       =   eval(context.req.content)
    assert_that( type(T),equal_to(dict),T)
    assert_that( (T.has_key('order_tag')==True and T['order_tag']!=''), equal_to(True))
    assert_that( (T.has_key('doc_post_url')==True and T['doc_post_url']!=''), equal_to(True))
    assert_that( (T.has_key('order_tag')==True and T['order_tag']!=''), equal_to(True))
    assert_that( (T.has_key('qr_code_x')==True
                  and T.has_key('qr_code_y')==True
                  and T.has_key('qr_code_scale')==True), equal_to(True))