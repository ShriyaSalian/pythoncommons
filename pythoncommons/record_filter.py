from random import sample as random_sample


class FilterStack(object):
    """ The FilterStack object class can represent a stack of FilterGroups that can
    be applied to records. Should be able to apply all of its filters in the stack
    to a given set of records and return intermediate or superimposed filters.
    """
    def __init__(self, name=None, description=None, filter_groups=[]):
        self.name = name
        self.description = description
        self.filter_groups = filter_groups

    def get_filter_types(self):
        pass

    def get_filter_names(self):
        pass

    def apply_filter_groups(self, records):
        pass


class FilterGroup(object):
    """ The FilterGroup object class is a direct container for DataFilters and
    should be directly contained by the FilterStack.
    """
    def __init__(self, name=None, description=None, operation='and', filters=[]):
        self.name = name
        self.description = description
        self.operation = operation
        self.filters = filters


class DataFilter(object):
    """ The DataFilter class is the base class for filter objects.
    A DataFilter should represent an arity one operation. To combine
    filters together into a condition, filters should be given to
    a FilterGroup object.
    """
    def __init__(self, name=None, description=None, filter_type=None):
        self.name = name
        self.description = description
        self.filter_type = filter_type


class RandomFilter(DataFilter):
    """
    This filter subclass handles grabbing n random elements (up to max_number)
    of an input list and produces the filtered result list.
    """
    def __init__(self, max_number=0):
        self.filter_type = "Random"
        self.max_number = max_number

    def filter_records(self, records):
        return random_sample(records, self.max_number)


class ValueFilter(DataFilter):
    """
    This filter subclass handles filtering a list for the specified value
    of a specified key. In this context, a key represents a property of an object.
    """
    def __init__(self, key=None, value=None, comparison="equal"):
        self.filter_type = "Value"
        self.key = key
        self.value = value
        self.comparison = comparison


def get_possible_keys(record):
    try:
        return record._fields
    except:
        try:
            return record[0]._fields
        except:
            return None


def get_unique_values(key, records):
    return list(set())


if __name__ == '__main__':
    print('this is currently not working.')
    filter_stack = FilterStack()
