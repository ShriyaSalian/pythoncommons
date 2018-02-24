import sys

"""
The module should read a simple properties file into a dictionary of key-value
pairs. Reading line by line while ignoring comments. The comments character
can be specified - if no character is specified a default of # will be used.
The assignment character can be specified - if no character is specified, =
will be used by default.
"""


def open_file(filename):
    """
    Returns an opened file as a list of lines. [line1,line2,etc.]
    """
    with open(filename, 'rt') as property_file:
        return property_file.readlines()


def filter_comment(file_line, comment_char):
    """
    Checks to make sure the line is not blank and does not start with the
    comment marker.
    """
    return file_line.strip() and file_line.strip()[0] != comment_char


def make_property(file_line, assignment_char):
    """
    Returns a list pair [key,value] split on the assignment_char
    """
    line_as_list = file_line.split(assignment_char, 1)
    return [line.strip() for line in line_as_list]


def list_filter(list_char):
    """
    Closure function for looking for list qualified values of properties. the
    closure returns the main function which takes a two valued list type
    object, splits on the specified list_char, and returns the pair back as
    [string,list]
    """
    def filter_value(pair):
        pair[1] = pair[1].split(list_char)
        return pair
    return filter_value


def make_dictionary(filename, comment_char='#', assignment_char='=',
                    list_char=','):
    """ The main function for this module, the flow is
    1) open a file
    2) read the file and ignore comments
    3) write a dictionary of key value pairs as a python dictionary
    3a) Note: the output of this makes a dictionary as string:list
    so when using it, check for length 1 to look for property as string.
    """
    property_file = open_file(filename)
    property_strings = [line for line in property_file if filter_comment(line, comment_char)]
    property_list = [make_property(line, assignment_char)
                     for line in property_strings]
    value_to_list = list_filter(list_char)
    property_list = list(map(value_to_list, property_list))
    property_dictionary = lambda list_to_dictionary: dict(list_to_dictionary)
    return property_dictionary(property_list)


if __name__ == '__main__':
    """
    Command line run of the module.
    """
    print('Trying to read: ', sys.argv[1])
    make_dictionary(sys.argv[1])
