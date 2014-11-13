
from os import environ as os_environ
from sys import argv as sys_argv

if __name__ == "__main__":
    os_environ.setdefault("DJANGO_SETTINGS_MODULE", "aprinto.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys_argv)
