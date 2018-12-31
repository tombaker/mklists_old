import os

RULEFILE_NAME = ".rules"
LOCAL_RULEFILE_NAME = ".localrules"
CONFIGFILE_NAME = "mklists.yml"


def find_rootdir():

    while True:
        ls_cwd = os.listdir()
        if LOCAL_RULEFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
        elif RULEFILE_NAME in ls_cwd:
            os.chdir(os.pardir)
        else:
            break

    if CONFIGFILE_NAME in os.listdir():
        repo_rootdir = os.getcwd()
        os.chdir(os.pardir)
    else:
        repo_rootdir = None
        print(f"{CONFIGFILE_NAME} not found. This is not a repo.")

    print("repo_rootdir:", repo_rootdir)
