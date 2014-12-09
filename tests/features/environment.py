# from distutils.util import strtobool as _bool
# import os
# BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "yes"))

def after_step(context, step):
    # if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
    if step.status == "failed":
        from subprocess import Popen as sub_popen
        from subprocess import PIPE as sub_PIPE
        cmd             =   'echo "%s" | mail -s "Unit-Test Failure" 6174295700@vtext.com'%context.scenario
        proc            =   sub_popen([''.join(cmd)], stdout=sub_PIPE, shell=True)
        (t, err)        =   proc.communicate()

        # import ipdb
        # ipdb.post_mortem(step.exc_traceback)