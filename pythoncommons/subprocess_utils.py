import subprocess
import shlex
from . import utils

# globals
git_return_status_dictionary = {0: True,
                                128: False
                                }


def get_Popen_output(string, cwd=None):
    """Generic function to return the subprocess.Popen output or error
    for the given string.
    """
    args = shlex.split(string)
    output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd).communicate()
    if output:
        return output.rstrip()
    return error


def run_subprocess(string):
    """Uses the python 3 subprocess.run to run the command passed in as a string.
    Returns a CompletedProcess object, containing args and a return code.
    """
    args = shlex.split(string)
    return subprocess.run(args)


def call_Popen(string, directory=None):
    """Generic function to call a shell command using a new shell
    for the given string. If a directory is given, runs in given directory.
    """
    args = shlex.split(string)
    if directory:
        subprocess.Popen(args, cwd=directory)
    else:
        subprocess.Popen(args)
    return


def clean_directory(directory):
    """Recursively removes the specified directory. This method should only be used
    when the user is sure the directory is safe for removal via some other function
    call.
    """
    remove_string = "rm -rf {directory}".format(directory=directory)
    status = subprocess.call(remove_string, shell=True)
    return status


def git_get_local_hash(directory):
    """Returns the full git hash of the git repository at the specified filesystem
    location
    """
    git_string = 'git -C {directory} rev-parse HEAD'.format(directory=directory)
    output = get_Popen_output(git_string)
    return output


def git_get_remote_hash(directory, repository, branch='master'):
    """Returns the full git hash of the remote repository for the specified local
    repository, optionally specifying the branch (defaults to master)
    """
    git_string = 'git -C {directory} ls-remote {repository} {branch}'.format(directory=directory,
                                                                             repository=repository,
                                                                             branch=branch)
    output = get_Popen_output(git_string)
    output_list = output.split()
    output = output_list[0]
    return output


def git_change_branch(directory, branch='master'):
    """Changes the repository to the specified branch (uses checkout). Does
    not create a new branch. Defaults to changing to master branch.
    """
    git_string = 'git -C {directory} checkout {branch}'.format(directory=directory,
                                                               branch=branch)
    output = get_Popen_output(git_string)
    return output


def git_remove_branch(directory, branch, switch_branch='master', delete_origin=False):
    """Removes a specified local branch and switches to the master branch. Optionally
    switches to a specified branch, optionally deletes the removed branch on the origin.
    Returns the new current branch name. Method prevents removing master.
    """
    if branch == 'master':
        return False
    successful_switch = git_change_branch(directory, switch_branch)
    if successful_switch:
        git_string = 'git -C {directory} branch -d {branch}'.format(directory=directory,
                                                                    branch=branch)
        output = get_Popen_output(git_string)
        if output:
            if delete_origin:
                git_string = 'git -C {directory} push origin --delete {branch}'.format(directory=directory,
                                                                                       branch=branch)
                output = get_Popen_output(git_string)
            return branch
    return False


def git_create_branch(directory, git_hash, branch=None, checkout=True):
    """Creates a new branch based on a given hash. Optionally allows for specifiying
    branch name, but will generate a random branch name if none specified. Optionally
    allows to create branch without checking it out.
    """
    if not branch:
        branch = utils.get_random_string()
    if checkout:
        git_string = 'git -C {directory} checkout -b {branch} {git_hash}'.format(directory=directory,
                                                                                 git_hash=git_hash,
                                                                                 branch=branch)
    else:
        git_string = 'git -C {directory} branch {branch} {git_hash}'.format(directory=directory,
                                                                            git_hash=git_hash,
                                                                            branch=branch)
    output = get_Popen_output(git_string)
    if output:
        return branch
    return False


def git_get_local_branch_name(directory):
    """Returns the current branch name of the git repository at the specified filesystem
    location.
    """
    git_string = 'git -C {directory} rev-parse --abbrev-ref HEAD'.format(directory=directory)
    output = get_Popen_output(git_string)
    return output


def check_correct_git_repository(repository, directory, check_string="Fetch URL:"):
    """Checks the repository directory against the remote repository to see if
    the directory is actually a child of the remote. Returns either true or false.
    """
    git_string = 'git -C {directory} remote show origin -n'.format(directory=directory)
    args = shlex.split(git_string)
    output, error = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    repository_info = output.splitlines()
    for info_line in repository_info:
        if check_string in info_line:
            git_url = info_line.lstrip(check_string).strip()
            if git_url == repository:
                return True
    return False


def pull_git_repository(name, repository, directory):
    """Pulls the repository to be up to date with the remote.
    """
    target = '{directory}/{name}'.format(directory=directory,
                                         name=name)
    git_string = "git -C {directory} pull".format(directory=target)
    output = get_Popen_output(git_string)
    if output:
        current_hash = git_get_local_hash(target)
        current_branch = git_get_local_branch_name(target)
        return {'hash': current_hash,
                'branch': current_branch,
                'success': True,
                'name': name,
                'repository': repository,
                'vcs_type': 'git'
                }
    return {'success': False,
            'name': name
            }


def clone_git_repository(repository, target_name, target_directory, overwrite=True):
    """Clones the target repository into the target directory using the given name.
    The method will fail if the directory is not already empty. If overwrite is true,
    however, the directory will be checked to make sure it is already a proper repository
    and, if so, will be overwritten. Returns the status of effort.
    """
    target = '{directory}/{name}'.format(directory=target_directory,
                                         name=target_name)
    if overwrite:
        if check_correct_git_repository(repository, target):
            clean_directory(target)
    git_string = "git clone {repository} {target}".format(repository=repository,
                                                          target=target)
    status = subprocess.call(git_string, shell=True)
    return_status = git_return_status_dictionary[status]
    if return_status:
        current_hash = git_get_local_hash(target)
        current_branch = git_get_local_branch_name(target)
        return {'hash': current_hash,
                'branch': current_branch,
                'success': True,
                'name': target_name,
                'repository': repository,
                'vcs_type': 'git'
                }
    return {'success': False,
            'name': target_name
            }


if __name__ == '__main__':
    print("No main method of vcs_utils. Please use as method package.")
