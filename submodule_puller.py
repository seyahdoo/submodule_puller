import subprocess
import os
from typing import List
import colorama
from colorama import Fore, Back, Style
import util

nothing_to_commit_msg = "nothing to commit, working tree clean"


def strip(l):
    return list(filter(None, l))


def run(cmd: List[str]) -> str:
    command_string: str = os.getcwd()
    command_string += "\\"
    for i in cmd:
        command_string += i
        command_string += " "
    print(f"{Fore.YELLOW}{command_string}{Style.RESET_ALL}")
    result_str: str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result_str)
    return result_str


def smart_pull_repo(repo_path: str):
    wd = os.getcwd()
    os.chdir(repo_path)

    # if change in repo, push to stash
    result_str = run(['git', 'status', '--ignore-submodules=all'])
    changes_exist = nothing_to_commit_msg not in result_str
    if changes_exist:
        run(['git', 'add', '.'])
        run(['git', 'stash'])

    # pull changes on repo
    run(['git', 'fetch'])
    run(['git', 'checkout', 'master'])
    run(['git', 'pull'])

    # get submodules
    result_str = run(['git', 'submodule'])
    submodules = strip(result_str.split('\n'))
    submodules = [strip(i.split(' '))[1] for i in submodules]

    # for each submodule
    for submodule in submodules:
        submodule_path = os.path.join(repo_path, submodule)
        smart_pull_repo(submodule_path)

    # commit submodule updates
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', 'submodule update'])

    # push submodule updates
    run(['git', 'push'])

    # if change in mother repo, pop from stash
    if changes_exist:
        run(['git', 'stash', 'pop'])

    # DONE
    os.chdir(wd)
    return


def do_process():
    colorama.init()
    path = util.get_application_path()
    for repo in os.listdir(path):
        repo_path = os.path.join(path, repo)
        if os.path.isdir(repo_path):
            smart_pull_repo(repo_path)

    print(f"{Fore.YELLOW}\n\nDONE! PRESS ENTER TO EXIT!\n{Style.RESET_ALL}")
    input()
    return


if __name__ == "__main__":
    do_process()
