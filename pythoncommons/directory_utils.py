import os
import sys
import shutil
from . import property_reader

"""
The purpose of this module is to copy the directory structure of a
source path into a target path, while following any rules given, such as
rules about ignored directories or file types.
"""


def item_not_in_list(item, filter_list):
    return item not in filter_list


def item_in_list(item, filter_list):
    return item in filter_list


def item_extension_check(extensions, wants_ends_with=False):

    def item_not_ends_with(item):
        for extension in extensions:
            if item.endswith(extension):
                return False
        return True

    def item_ends_with(item):
        for extension in extensions:
            if item.endswith(extension):
                return True
        return False

    if wants_ends_with:
        return item_ends_with

    return item_not_ends_with


def remove_directory(path):
    """ Removes a directory recursively if it exists by specifying
    the path.
    """
    if os.path.isdir(path):
        shutil.rmtree(path)


def copy_files(source_path, target_path, file_list):
    for copy_file in file_list:
        try:
            source = source_path + "/" + copy_file
            target = target_path + "/" + copy_file
            shutil.copy(source, target)
        except:
            print('failed copying ', target)


def argument_property_check(properties):
    default_properties = {}
    default_properties['source_path'] = [os.getcwd()]
    default_properties['target_path'] = [os.getcwd() + "/copy"]
    default_properties['remove_target_path'] = [False]
    default_properties['data_directories'] = []
    default_properties['ignored_extensions'] = []
    default_properties['ignored_directories'] = []

    if type(properties) is dict:
        passed_keys = list(properties.keys())
        for key, value in default_properties.items():
            if key not in passed_keys:
                properties[key] = value
    else:
        properties = default_properties
    return properties


def get_immediate_subdirectories(parent):
    return [os.path.join(parent, child) for child in os.listdir(parent)
            if os.path.isdir(os.path.join(parent, child))]


def pattern_match_closure(properties):

    properties = properties

    def pattern_match(text):
        condition_match = False
        if 'starts_with' in properties:
            condition_match = True
            if not text.startswith(properties['starts_with'][0]):
                return False
        if 'ends_with' in properties:
            condition_match = True
            if not text.endswith(properties['ends_with'][0]):
                return False
        if 'contains' in properties:
            condition_match = True
            if text.count(properties['contains'][0]) == 0:
                return False
        if 'not_contains' in properties:
            condition_match = True
            if text.count(properties['not_contains'][0]) > 0:
                return False
        return condition_match

    return pattern_match


def full_path_closure(parent):

    parent = parent

    def full_path(file_name):
        if parent.endswith("/"):
            return parent + file_name
        else:
            return parent + "/" + file_name

    return full_path


def get_directory_exists(directory):
    """Checks the passed directory to see if it exists. If it does, this method
    returns True. If the directory does not exist, this method returns False.
    """
    directory_exists = os.path.isdir(directory)
    return directory_exists


def get_matching_files(properties):
    """Walks a specified path and finds files that match the pattern.
    The passed properties file must contain a source_path, and will look for files
    that match the pattern starts_with, ends_with, or contains. The function will
    attempt to read a properties file or can take a dictionary with k,v pairs.
    """
    if type(properties) is not dict:
        try:
            properties = property_reader.make_dictionary(properties)
        except:
            return None
    try:
        pattern_matcher = pattern_match_closure(properties)
        return_files = []
        for parent, children, files in os.walk(properties['source_path'][0]):
            get_full_path = full_path_closure(parent)
            match_files = [item for item in files if pattern_matcher(item)]
            return_files += list(map(get_full_path, match_files))
        return return_files
    except:
        return None


def copy_directory_tree(properties):
    """ Copies the source data directory into a
    specified copy data directory.
    """

    properties = argument_property_check(properties)

    if properties['remove_target_path']:
        remove_directory(properties['target_path'][0])

    check_file_extension = item_extension_check(properties['ignored_extensions'])

    for parent, children, files in os.walk(properties['source_path'][0]):
        full_target_path = parent.replace(properties['source_path'][0],
                                          properties['target_path'][0], 1)
        os.mkdir(full_target_path)
        children[:] = [item for item in children if item_not_in_list(item,
                                              properties['ignored_directories']
                                              )]
        current_directory = parent.split("/")[-1]

        if current_directory not in properties['data_directories']:
            files[:] = [item for item in files if check_file_extension(item)]
            copy_files(parent, full_target_path, files)


if __name__ == '__main__':
    """
    Command line run of the module.
    """
    remove_directory(sys.argv[2])
    copy_directory_tree(sys.argv[1], sys.argv[2])
