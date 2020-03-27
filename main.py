from sys import exit
from updater import update_app
from version import version
from submodule_puller import do_process

if __name__ == "__main__":

    # intro
    print("##########################################")
    print("##########################################")
    print("####                                  ####")
    print("####    SUBMODULE PULLER              ####")
    print("####                                  ####")
    print("####           created by seyahdoo    ####")
    print("####                                  ####")
    print("##########################################")
    print("##########################################")
    print()
    print("version = " + version)

    # Try to update self
    just_updated = update_app()

    # Do process
    do_process()
    exit(0)
