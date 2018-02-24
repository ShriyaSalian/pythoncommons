import os
import sys
import fileinput
"""
The module should write a simple properties file from a dictionary of key-value
pairs. Each property will be written on a separate line. properties will be
specified as key = value and the file will be saved at the given location.
"""


def key_value_pair_to_string(key, value):
    value_string = ",".join(value)
    property_string = key + " = " + value_string + '\n'
    return property_string


def write_dictionary_to_file(filename, dictionary, mode="w+"):
    with open(filename, mode) as f:
        for key, value in dictionary.items():
            property_line = key_value_pair_to_string(key, value)
            f.write(property_line)


def write_dictionary_to_makefile(makefile, dictionary, step="#setenv", export=True):
    for line in fileinput.input(makefile, inplace=1):
        if line.startswith(step):
            sys.stdout.write(line)
            for key, value in dictionary.items():
                property_line = key_value_pair_to_string(key, value)
                property_line = property_line.replace(" = ", "=")
                if export:
                    property_line = "export " + property_line
                sys.stdout.write(property_line)
        else:
            sys.stdout.write(line)


def write_dictionary_to_env_vars(dictionary, format="UNIX"):
    for key, value in dictionary.items():
        os.environ[str(key)] = str(value)


if __name__ == '__main__':
    print('Main method of property_writer sub module')
