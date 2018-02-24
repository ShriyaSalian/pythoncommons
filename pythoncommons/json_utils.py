import simplejson as json
from collections import namedtuple


def serialize(thing, thing_type='namedtuple'):
    try:
        if thing_type == 'namedtuple':
            json_string = json.dumps(thing, namedtuple_as_object=True, use_decimal=True)
            return json.loads(json_string)
        else:
            return json.dumps(thing)
    except:
        return "Cannot serialize passed object."


def json_object_hook(d):
    return namedtuple('X', list(d.keys()))(*list(d.values()))


def deserialize(thing, thing_type='namedtuple'):
    try:
        if thing_type == 'namedtuple':
            return json.loads(thing, object_hook=json_object_hook)
        else:
            return json.loads(thing)
    except:
        return "Cannot deserialize passed json string"


if __name__ == '__main__':
    print("Main method of json_utils.")
