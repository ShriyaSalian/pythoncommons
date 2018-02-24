from datetime import datetime
import property_reader_utils
import os
import inspect
import random
import string
from operator import itemgetter
import re


def flatten(value, flat):
    for v in value:
        if type(v) is list:
            flatten(v, flat)
        else:
            flat.append(v)
    return flat


def replace_cross_reference_closure(dictionary):

    def cross_referenced_target(target):
        if type(target) in [list]:
            if len(target) == 2:
                if type(target[0]) in [str, str]:
                    if type(target[1]) in [list]:
                        return True
        return False

    def replace_cross_reference(key):
        if cross_referenced_target(dictionary[key]):
            dictionary[key] = dictionary[key][0]
        return

    return replace_cross_reference


def get_full_path_for_dictionary_key_closure(dictionary):

    def cross_referenced_target(target):
        if type(target) in [list]:
            if len(target) == 2:
                if type(target[0]) in [str, str]:
                    if type(target[1]) in [list]:
                        return True
        return False

    def get_valid_target(target):
        if not target or type(target) not in [str, str]:
            if cross_referenced_target(target):
                return target
            else:
                return 'None'
        return target

    def get_valid_keywords(target):
        if cross_referenced_target(target):
            keywords = re.findall(r'{([^{}]*)}', target[0])
            return [keyword for keyword in keywords if keyword not in target[1]]
        return re.findall(r'{([^{}]*)}', target)

    def get_full_path_for_dictionary_key(key):
        """Returns the directory in which to look for structures for the given profile,
        filling in path keywords as necessary.
        """
        target = dictionary[key]
        target = get_valid_target(target)
        keywords = get_valid_keywords(target)
        if not keywords:
            return dictionary
        else:
            replacer = replace_method_closure(target, dictionary)
            target = list(map(replacer, keywords))[0]
            dictionary[key] = target
            get_full_path_for_dictionary_key(key)

    return get_full_path_for_dictionary_key


def replace_method_closure(target, dictionary):

    def cross_referenced_target(target):
        if type(target) in [list]:
            if len(target) == 2:
                if type(target[0]) in [str, str]:
                    if type(target[1]) in [list]:
                        return True
        return False

    def valid_replacement(target, keyword):
        if cross_referenced_target(target):
            target_string = target[0]
            if cross_referenced_target(dictionary[keyword]):
                if target_string in dictionary[keyword][0] or target[0] in dictionary[keyword][1]:
                    return False
                else:
                    return True
            else:
                if target_string in dictionary[keyword]:
                    return False
                else:
                    return True
        else:
            target_string = target
            if cross_referenced_target(dictionary[keyword]):
                if target_string in dictionary[keyword][0] or target in dictionary[keyword][1]:
                    return False
                else:
                    return True
            else:
                if target_string in dictionary[keyword]:
                    return False
                else:
                    return True

    def replace_method(keyword):
        if valid_replacement(target, keyword):
            if cross_referenced_target(target):
                if cross_referenced_target(dictionary[keyword]):
                    target[0] = target[0].replace('{' + keyword + '}', dictionary[keyword][0])
                else:
                    target[0] = target[0].replace('{' + keyword + '}', dictionary[keyword])
                return target
            else:
                if cross_referenced_target(dictionary[keyword]):
                    return target.replace('{' + keyword + '}', dictionary[keyword][0])
                else:
                    return target.replace('{' + keyword + '}', dictionary[keyword])
        else:
            if cross_referenced_target(target):
                target[1].append(keyword)
                return target
            else:
                return [target, [keyword]]

    return replace_method


def get_fully_qualified_dictionary_values(dictionary):
    value_replacer = get_full_path_for_dictionary_key_closure(dictionary)
    list(map(value_replacer, list(dictionary.keys())))
    cross_reference_replacer = replace_cross_reference_closure(dictionary)
    list(map(cross_reference_replacer, list(dictionary.keys())))


def sort_dictionary_list_on_key(dictionary_list, sort_key):
    """Pass in a list of dictionaries, a key to sort on, and an optional order,
    and this will return the sorted list of dictionaries.
    """
    sorted_list = sorted(dictionary_list, key=itemgetter(sort_key))
    return sorted_list


def get_random_string(letters=True, numbers=False, length=10):
    """Returns a string of specified length, with letters and/or numbers as specified.
    Defaults to return a random string of length 10 with only letters.
    """
    if letters and numbers:
        return_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
    elif letters:
        return_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(length))
    elif numbers:
        return_string = ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))
    return return_string


def remove_dictionary_keys(dictionary, remove_keys):
    for key in list(dictionary.keys()):
        if key in remove_keys:
            del dictionary[key]


def get_timestamp():
    return ".".join(str(datetime.now()).split())


def ensure_precision(value, precision):
    """Takes a value and a precision, decides if the value needs to be adjusted,
    and returns either the properly adjusted value or the original value.
    """
    if precision:
        precision = int(precision)
        split_value = str(value).split(".")
        adjust = precision - len(split_value[1])
        if adjust >= 0:
            split_value[1] += '0' * adjust
        else:
            split_value[1] = split_value[1][:precision]
        return ".".join(split_value)
    else:
        return value


def file_to_properties(extension, rel_exec_path='/src/main/processor',
                       rel_property_path='/properties/'):
    current_path = os.path.dirname(os.path.realpath(__file__))
    setup_file = current_path.replace(rel_exec_path, rel_property_path)
    setup_file += extension
    properties = property_reader.make_dictionary(setup_file)
    return properties


def get_random_coordinate():
    """Returns a random coordinate as a dictionary.
    Returns as dict(latitude:y,longitude:x).
    """
    coordinate = {}
    coordinate["latitude"] = 90.0 - random.random() * 180.0
    coordinate["longitude"] = 180 - random.random() * 360.0
    return coordinate


def get_random_integer(lb, ub):
    """Gets a random integer between lb and ub INCLUSIVE
    """
    return random.randint(lb, ub)


def get_month_for_index(i):
    month_dictionary = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return month_dictionary[i]


def get_index_for_month(month):
    month = month.upper()
    month_dictionary = {
        "JANUARY": 1,
        "FEBRUARY": 2,
        "MARCH": 3,
        "APRIL": 4,
        "MAY": 5,
        "JUNE": 6,
        "JULY": 7,
        "AUGUST": 8,
        "SEPTEMBER": 9,
        "OCTOBER": 10,
        "NOVEMBER": 11,
        "DECEMBER": 12
    }
    return month_dictionary[month]


def cur_date():
    """ Returns the current datetime stamp using datetime.datetime library.
    """
    return datetime.now()


def find_list_differences(list_one, list_two):
    """ Returns the unique differences between two lists.
    """
    return list(set(list_one) - set(list_two))


def add_string_to_list_elements(string, target_list, beginning=True):
    """ Adds a string to a target list, can specify an optional parameter to
    put it in front or behind.
    """
    if beginning:
        return [string + i for i in target_list]
    else:
        return [i + string for i in target_list]


def translate_delimiter(delimiter_string):
    """ Takes a descriptive string, like comma, and turns it into
    the thing it describes. comma -> ',' tab -> actual tab
    """
    delimiter_dictionary = {"comma": ',', "tab": '\t'}
    if delimiter_string.isalpha():
        try:
            return delimiter_dictionary[delimiter_string]
        except:
            return "    "
    elif delimiter_string.isspace():
        return delimiter_string
    else:
        return "    "


def merge_dicts(*dicts):
    """Merge an unlimited number of dictionaries together into one dictionary.
    Unpackages nested dictionaries.
    """
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


def merge_list_of_dicts(dict_list):
    """Merges dictionaries that are part of a list.
    Does not unpackage nested dictionaries.
    """
    result = {}
    for dictionary in dict_list:
        for key, value in dictionary.items():
            result[key] = value
    return result


def merge_lists(list_of_lists, nested=False):
    """Merges an arbitrary number of lists passed in. Handles the case where
    an individual list might be None. Returns the complete and flattened list.
    Optional nested parameter allows for recursively flattening nested lists.
    Defaults to false (only flattens 1 level of nesting.)
    """
    flat_list = []
    for l in list_of_lists:
        if l:
            flat_list += l
    return flat_list


def isnamedtupleinstance(x):
    """ Given an object, returns True if the object is a namedtuple,
    returns false if the object is not.
    """
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def clean_string(s):
    """ Remove all spaces around string and make the string uppercase.
    """
    return s.strip().upper()


def describe_class(C):
    """ Describes a class C by returning user defined functions and properties
    as strings.
    """
    attributes = inspect.getmembers(C, lambda a: not(inspect.isroutine(a)))
    return [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
