from behave import *
from hamcrest import assert_that, equal_to, is_not
import requests
from sys import path as py_path
py_path.append('/Users/admin/SERVER3/aprinto')

# test_url = '192.168.3.52'
# BASE_URL = 'http://'+test_url+':8088'

@given('"{page_title}" is live and we access "{webpage}"')
def step_impl(context,page_title,webpage):
    context.url             =   webpage
    assert True is True

@then('the page should start loading within "{response_time}" seconds')
def step_impl(context,response_time):
    headers                 =   {'Content-type': 'text/html; charset=UTF-8'}
    data                    =   {'headers'  :   headers,
                                 'timeout'  :   float(response_time)}
    try:
        req                 =   requests.request('GET',context.url,**data)
        context.timeout     =   False
        context.resp_code   =   req.status_code
        context.resp_msg    =   req.reason
    except requests.Timeout:
        context.timeout     =   True
    assert_that( context.timeout,   equal_to(False) )

@then('the response message should be "{msg}" with response code "{code}"')
def step_impl(context,msg,code):
    assert_that( context.resp_code, equal_to(int(code)), str(context.resp_code) )
    assert_that( context.resp_msg,  equal_to(msg),       str(context.resp_msg)  )