import os

RULEFILE_NAME = ".rules"
CONFIGFILE_NAME = "mklists.yml"


def goto_repo_rootdir():
    if CONFIGFILE_NAME in os.listdir(os.getcwd()):
        set_repo_rootdir()
    if RULEFILE_NAME in os.listdir(os.getcwd()):
        print(f"Found: {os.path.join(os.getcwd(), '.rules')}")
        print(f"In: {os.getcwd()}")
        os.chdir(os.pardir)
        if CONFIGFILE_NAME in os.listdir(os.getcwd()):
            set_repo_rootdir()


def set_repo_rootdir():
    REPO_ROOTDIR = os.getcwd()
    print(f"Root directory: {REPO_ROOTDIR}")
