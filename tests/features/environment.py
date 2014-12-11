# from distutils.util import strtobool as _bool
# import os
# BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "yes"))

def after_step(context, step):
    # if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
    if step.status == "failed":
        # import ipdb
        # ipdb.post_mortem(step.exc_traceback)

        from subprocess import Popen as sub_popen
        from subprocess import PIPE as sub_PIPE

        ft_name         =   context.scenario.feature.name
        scenario_type   =   context.scenario.keyword            # e.g., u'Scenario Outline'
        if ft_name == 'Verify Online Presence':
            active_outline  =   context.active_outline
            if context.timeout:
                msg         =   "Unit Test Failed: %s [%s] did not load in %s"%tuple(active_outline.cells)
            else:  msg      =   "Unit Test Failed: %s -- msg(%s),code(%s)"%(active_outline[0],context.resp_msg,context.resp_code)

            cmd             =   'echo "%s" | mail -s "Unit-Test Failure" 6174295700@vtext.com'%msg
            proc            =   sub_popen([''.join(cmd)], stdout=sub_PIPE, shell=True)
            (t, err)        =   proc.communicate()

        else:
            msg             =   'Unit Test Failed: %s'%ft_name
            cmd             =   'echo "%s" | mail -s "Unit-Test Failure" 6174295700@vtext.com'%msg
            proc            =   sub_popen([''.join(cmd)], stdout=sub_PIPE, shell=True)
            (t, err)        =   proc.communicate()


