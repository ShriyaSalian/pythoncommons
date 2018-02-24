from collections import namedtuple
from .general_utils import translate_delimiter, get_timestamp


def get_name(named_tuple):
    return "".join((type(named_tuple).__name__).split())


def get_string_lengths(start_positions, last_unlimited=True):
    string_lengths = []
    for i in range(0, len(start_positions) - 1):
        string_lengths.append(int(start_positions[i + 1]) - int(start_positions[i]))
    if last_unlimited:
        string_lengths.append(None)
    return string_lengths


def tuple_to_fixed_string(record, fields):
    """This function should turn a named tuple record into concatenated string
    with each element of the tuple either truncated or padded depending
    on its associated length.
    """
    file_string = ''
    for field in fields:
        if fields.index(field) > 0:
            start_end_difference = int(field[1]) - int(fields[fields.index(field) - 1][2])
            if start_end_difference > 0:
                file_string += ' ' * start_end_difference
        field_length = int(field[2]) - int(field[1])
        if len(str(getattr(record, field[0]))) > field_length:
            file_string += str(getattr(record, field[0]))[:field_length]
        else:
            if field[3] == 'left':
                file_string += str(getattr(record, field[0])).ljust(field_length)
            elif field[3] == 'right':
                file_string += str(getattr(record, field[0])).rjust(field_length)
    file_string += '\n'
    return file_string


def tuple_to_delimited_string(record, fields, delimiter):
    file_string = ''
    for field in fields:
        file_string += str(getattr(record, field))
        file_string += delimiter
    file_string += '\n'
    return file_string


def write_fixed_length_strings(file_name, records, fields):
    """Should write fixed length strings to the specified file.
    """
    with open(file_name, "a+") as open_file:
        for record in records:
            open_file.write(tuple_to_fixed_string(record, fields))


def write_delimited_strings(file_name, delimiter, records, fields):
    with open(file_name, "a+") as open_file:
        for record in records:
            open_file.write(tuple_to_delimited_string(record, fields, delimiter))


def write_records(records, properties=None):
    """This method takes a list of named tuple records and a properties file and
    produces an output file containing the records. The properties that are necessary
    are: field_names, and either field_start_positions or a field_separator.
    Optionally, an output file should be specified.
    """
    try:
        file_name = properties['output_file'][0]
    except:
        file_name = get_name(records[0]) + '_' + get_timestamp()
    try:
        fields = properties['field_names']
    except:
        fields = records[0]._fields
    try:
        fields = list(zip(fields, properties['field_start_positions'],
                     properties['field_end_positions'], properties['field_justify']))
        write_fixed_length_strings(file_name, records, fields)
    except:
        print('Trying to write records as delimited strings.')
        delimiter = translate_delimiter(properties['field_separator'][0])
        print(delimiter, ' (delimiter)')
        write_delimited_strings(file_name, delimiter, records, fields)
    return True


if __name__ == '__main__':
    """Executing the main method of record_writer
    """
    Point = namedtuple('Point', ['x', 'y', 'z'])
    a = Point(12352362362, 2, 3500)
    b = Point(3, 4, 7000)
    c = Point(5, 6, 10500)
    d = [a, b, c]
    properties = {}
    properties['field_start_positions'] = [0, 5, 10]
    properties['field_separator'] = ['tab']
    properties['field_names'] = ['z', 'y', 'x']
    print('Executing the direct method of the record writer module with test data.')
    write_records(d, properties)
