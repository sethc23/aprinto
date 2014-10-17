from os import path as os_path
from sys import path as sys_path
# from uuid import getnode as get_mac
#
# macs = {'Macbook':'105773427819682',
#         'MacBookPro':'117637351435',
#         'MBP2':'220083054034723'}
# this_mac = str(get_mac())
#
# print this_mac
#Calculate the path based on the location of the WSGI script.

f = __file__

#
#     project_space = '/Users/admin/django/Dropbox/aprinto/aprinto'    # os_path.dirname(f)
#     work_space = os_path.dirname(project_space)
#     virtual_env = os_path.join(work_space, 'bin/python2.6/site-packages')
#
# elif this_mac == macs['Macbook']:
#     project_space = '/Users/sethchase/Dropbox/BD_Scripts/django/Dropbox/aprinto/aprinto'    # os_path.dirname(f)
#     work_space = os_path.dirname(project_space)
#     virtual_env = os_path.join(work_space, 'ENV/lib/python2.7/site-packages')

project_space = os_path.dirname(f)
work_space = os_path.dirname(project_space)
virtual_env = os_path.join(work_space, 'ENV/lib/python2.7/site-packages')

sys_path.append(virtual_env)
sys_path.append(project_space)
sys_path.append(work_space)

from os import environ
project_name = project_space[project_space[:-1].rfind('/')+1:].strip('/')
environ['DJANGO_SETTINGS_MODULE'] = project_name+'.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()