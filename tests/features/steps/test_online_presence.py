from behave import *
from hamcrest import assert_that, equal_to, is_not
from sys import path as py_path
py_path.append('/Users/admin/SERVER3/aprinto')

import requests

test_url = '192.168.3.52'
BASE_URL = 'http://'+test_url+':8088'

class VisitWebpage(object):
    TITLE_TO_URL_MAP = {
        "Aporo"                     :   "http://printer.aporodelivery.com",
        "GnamGnam Home Page"        :   "http://www.gnamgnamapp.com/",
        "GnamGnam Join Us Page"     :   "http://www.gnamgnamapp.com/join/",
        "GnamGnam Admin Page"       :   "http://admin.gnamgnamapp.com/login",
    }
    TITLE_TO_RESPONSE_TIME_MAP = {
        "Aporo"                     :   "5.0",
        "GnamGnam Home Page"        :   "5.0",
        "GnamGnam Join Us Page"     :   "5.0",
        "GnamGnam Admin Page"       :   "5.0",
    }

    def __init__(self):
        self.page_title     =   None
        self.url            =   None
        self.timeout        =   None

    @classmethod
    def select_timeout_for(cls, page_title):
        return cls.TITLE_TO_RESPONSE_TIME_MAP.get(page_title, "DIRT")

    @classmethod
    def select_url_for(cls, page_title):
        return cls.TITLE_TO_URL_MAP.get(page_title, "DIRT")

    def add(self, page_title):
        self.page_title     =   page_title

    def get_url_and_timeout(self):
        self.url            =   self.select_url_for(self.page_title)
        self.timeout        =   self.select_timeout_for(self.page_title)

@given('"{page_title}" is live')
def step_impl(context,page_title):
    context.web_access      =   VisitWebpage()
    context.web_access.add(page_title)
    context.web_access.get_url_and_timeout()

@when('we access "{webpage}"')
def step_impl(context,webpage):
    headers                 =   {'Content-type': 'text/html; charset=UTF-8'}
    data                    =   {'headers'  :   headers,
                                 'timeout'  :   float(context.web_access.timeout)}
    try:
        req                 =   requests.request('GET',context.web_access.url,**data)
        context.timeout     =   False
        context.resp_code   =   req.status_code
        context.resp_msg    =   req.reason
    except requests.Timeout:
        context.timeout     =   True


@then('the page should start loading within "{text}" seconds')
def step_impl(context,text):
    assert_that( context.timeout,equal_to(False) )

@then('the response code should be "{text}"')
def step_impl(context,text):
    assert_that( context.resp_code,equal_to(int(text)), str(context.resp_code))

@then('the response message should be "{text}"')
def step_impl(context,text):
    context.resp_msg        =   text
