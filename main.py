# import functions_framework
import gits
import runcheck
import os

USE_DEV_ACCOUNTS = True
USE_DEV_FABRIC = False

# @functions_framework.http

def gitcheck_full(request):
    
    test = gits.git_test()
    final_object = ''
    # final_object = runcheck(USE_DEV_ACCOUNTS, USE_DEV_FABRIC)

    if not final_object == '':
        return final_object
    else:
        return test

# gitcheck_full()
gits.reset_git_test()