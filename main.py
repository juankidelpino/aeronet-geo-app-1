import coms
import runcheck
import os
import pickle
import helpers

# MAIN -> RUNCHECK -> LOAD_FILES -> RUNCHECK -> MAIN(final_object)

USE_DEV_ACCOUNTS = True
USE_DEV_FABRIC = False


def gitcheck_full(request):
    
    test = coms.git_test()
    return test
# gitcheck_full()
# gits.reset_git_test()


def update_accounts(request):
    final_object = runcheck.runcheck(USE_DEV_ACCOUNTS, USE_DEV_FABRIC)
    print(final_object)
    return final_object

update_accounts('')