from collections import namedtuple
from pythoncommons.property_reader_utils import make_dictionary
from pythoncommons.general_utils import translate_delimiter
from pythoncommons.directory_utils import get_matching_files
import csv
import decimal
import sys

"""
The set of tools used for interaction with metadata files.
There should be tools to read a metadata file and to create a metadata file.
There should also be methods to read a set of stations, access the correct
metadata file, and create a new metadata file from that station list.
"""


def type_changer(fields):
    """Closure function for changing an objects type
    """
    type_dictionary = {"integer": int, "float": float, "string": str, "list": list}

    def parse_input(value, field_type):
        if field_type == "decimal":
            try:
                decimal.getcontext().prec = len(value.split(".")[1])
            except:
                decimal.getcontext().prec = 4
            return decimal.Decimal(value)
        else:
            return type_dictionary[field_type](value)

    return parse_input


def make_named_tuple(name, argument_list):
    return namedtuple(name, argument_list)


def dictionary_converter_tool(named_tuple):
    def dictionary_converter(dictionary):
        return named_tuple(**dictionary)
    return dictionary_converter


def record_dictionary(fields):
    """Closure function for creating a dictionary
    of objects. Closure takes a list of field tuples as
    (field_name, field_type). Inner function uses this
    to turn the record into a dictionary.
    """
    change_type = type_changer(fields)

    def get_value(record, index, field_type):
        try:
            return change_type(record[index], field_type)
        except:
            return None

    def make_record_dictionary(record):
        return {field[0]: get_value(record, fields.index(field), field[1]) for field in fields}
    return make_record_dictionary


def read_records_from_directory(type_name, fields, records_extension, records_directory,
                                slices=[], field_separator=None, keyword_converter=None):
    properties = {"source_path": [records_directory],
                  "ends_with": [records_extension]}
    record_files = get_matching_files(properties)
    records = []
    for record_file in record_files:
        records += read_records(type_name, fields, record_file, slices,
                                field_separator, keyword_converter)
    return records


def read_records(type_name, fields, record_file, slices=[], field_separator=None,
                 keyword_converter=None):
    dictionary_maker = record_dictionary(fields)
    named_tuple = make_named_tuple(type_name, list(zip(*fields))[0])
    dictionary_converter = dictionary_converter_tool(named_tuple)
    with open(record_file, 'rt') as records:
        if slices:
            record_slicer = slicer(slices)
            sliced_records = list(map(record_slicer, records))
        elif field_separator:
            sliced_records = [record for record in csv.reader(records, delimiter=field_separator)]
    dictionary_list = list(map(dictionary_maker, sliced_records))
    if keyword_converter:
        dictionary_list = [keyword_converter(dictionary) for dictionary in dictionary_list]
    named_tuples = list(map(dictionary_converter, dictionary_list))
    return named_tuples


def make_intervals(positions):
    intervals = []
    for i in range(len(positions) - 1):
        intervals.append((positions[i], positions[i + 1]))
    intervals.append((positions[-1], -1))
    return intervals


def make_slices(intervals):
    return [slice(*interval) for interval in intervals]


def slicer(slices):
    """Closure function for the slice string function.
    """
    def slice_string(record):
        return [record[interval].strip() for interval in slices]
    return slice_string


def strings_to_ints(string_list):
    return [int(item) for item in string_list]


def make_tuple_dictionary(tuple_list):
    return {record[0]: record[1] for record in tuple_list}


def dict_to_named_tuple_closure(name):
    def dict_to_named_tuple(dictionary):
        dictionary.pop("_id", None)
        return namedtuple(name, list(dictionary.keys()))(**dictionary)
    return dict_to_named_tuple


def get_records_as_tuples(properties, source='property_file'):
    """Reads a properties dictionary and turns the records into
    named tuples of the type passed.
    """
    try:
        records_file = properties['records_file'][0]
    except:
        records_file = None
    try:
        records_directory = properties['records_directory'][0]
    except:
        records_directory = None
    try:
        records_extension = properties['records_extension'][0]
    except:
        records_extension = None
    try:
        type_name = properties['type_name'][0]
    except KeyError:
        type_name = 'Object'
    try:
        slices = make_slices(make_intervals(strings_to_ints(properties['field_start_positions'])))
    except KeyError:
        slices = None
    try:
        keyword_converter = properties['keyword_converter']
    except:
        'cannot set keyword converter'
        keyword_converter = None
    try:
        field_separator = translate_delimiter(properties['field_separator'][0])
    except KeyError:
        field_separator = None
    try:
        field_types = list(zip(properties['field_names'], properties['field_types']))
    except:
        field_types = [(field_name, 'string') for field_name in properties['field_names']]
    if records_directory:
        records = read_records_from_directory(type_name, field_types, records_extension,
                                              records_directory, slices, field_separator,
                                              keyword_converter)
    else:
        records = read_records(type_name, field_types, records_file, slices, field_separator,
                               keyword_converter)
    return records


def get_records_from_file(variables):
    """Accepts a dictionary containing a fields parameter as a list of field
    dictionaries ([f1,f2,f3] where f1 has at least a name and type and can possibly
    have other instructions), a file path, and optionally a field separator,
    and returns the records from the file.
    """
    fields = variables['fields']
    field_types = [(field['name'], field['type']) for field in fields]
    path = variables['path']
    separator = None
    if 'separator' in list(variables.keys()):
        separator = translate_delimiter(variables['separator'])
    slices = None
    if 'start_position' in list(fields[0].keys()):
        start_positions = [field['start_position'] for field in fields]
        slices = make_slices(make_intervals(strings_to_ints(start_positions)))
    records = read_records('Record', field_types, path, slices, separator)
    return list(map(named_tuple_to_dictionary, records))


def named_tuple_to_dictionary(named_tuple):
    """Changes a named tuple to its equivalent dictionary.
    """
    return named_tuple._asdict()


if __name__ == '__main__':
    print('Running direct method of record reader.')
    properties = make_dictionary(sys.argv[1])
    records = get_records_as_tuples(properties)
