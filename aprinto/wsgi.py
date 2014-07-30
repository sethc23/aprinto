from os import path as os_path
from sys import path as sys_path
from uuid import getnode as get_mac

macs = {'Macbook':'105773427819682',
            'MacBookPro':'117637351435',}
this_mac = get_mac()

#Calculate the path based on the location of the WSGI script.

f = __file__

project_space = '/Users/sethchase/Dropbox/BD_Scripts/django/Dropbox/aprinto/aprinto'    # os_path.dirname(f)
work_space = os_path.dirname(project_space)

if str(this_mac)==macs['Macbook']:
    virtual_env = os_path.join(work_space, 'ENV/lib/python2.7/site-packages')
elif str(this_mac)==macs['MacBookPro']:
    virtual_env = os_path.join(work_space, 'bin/python2.6/site-packages')

sys_path.append(virtual_env)
sys_path.append(project_space)
sys_path.append(work_space)

from os import environ
project_name = project_space[project_space[:-1].rfind('/')+1:].strip('/')
environ['DJANGO_SETTINGS_MODULE'] = project_name+'.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()