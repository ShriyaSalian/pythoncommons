from pymongo import MongoClient, GEOSPHERE
from bson.son import SON
from bson import ObjectId
import json_utils
import record_reader_utils


def unload_cursor(cursor):
    """Unloads a cursor and returns the collection of things it contains.
    """
    try:
        return [record for record in cursor]
    except:
        return "Could not unload the cursor"


def ensure_objectid(id_string):
    """Converts a string to a mongo objectId if it isn't, returning the objectId.
    """
    if type(id_string) not in [ObjectId]:
        id_string = ObjectId(id_string)
    return id_string


def make_single_field_argument(key, value, arg_type='equals'):
    """Creates and returns a single field argument for use in
    filtering a mongo collection.
    """
    if arg_type == 'equals':
        return {key: value}
    elif arg_type == 'not_equals':
        return {key: {'$ne': value}}


def make_sort_argument(key, order='ascending'):
    """Creates a single sort argument for sorting a mongodb search. Can specify
    a sort order of ascending or descending (defaults to ascending). Returns the
    sort argument.
    """
    if order == 'ascending':
        return (key, 1)
    elif order == 'descending':
        return (key, -1)


def make_update_argument(key, value, key_type='string'):
    """Makes a single new update argument for a mongo datbase. Can pass in parameter
    type to handle making different types of updates (string, datetime, etc.)
    ** Currently only handles string updates **
    """
    if key_type == 'string':
        return {'$set': {key: value}}


def make_spatial_near_argument(key, longitude, latitude, max_distance=None):
    """Creates and returns a single field argument based on a GEOSPHERE search.
    Allows for an optional max_distance(defaults to None)
    """
    if max_distance:
        argument = {key: {'$near': SON([('$geometry', SON([('type', 'Point'),
                    ('coordinates', [longitude, latitude])])), ('$maxDistance', max_distance)])}}
    else:
        argument = {key: {'$near': SON([('$geometry', SON([('type', 'Point'),
                    ('coordinates', [longitude, latitude])]))])}}
    return argument


def make_spatial_within_argument(key, coordinates, poly_type="Polygon"):
    """Creates and returns a single field argument based on a GEOSPHERE search.
    The argument can be used to find all points within the specified polygon.
    """
    argument = {key: {'$geoWithin': SON([('$geometry', SON([('type', poly_type),
                ('coordinates', coordinates)]))])}}
    return argument


def merge_update_args(update_list):
    """Merges a list of update arguments into a single update. Returns the new
    update dictionary.
    """
    master_update = {'$set': {}}
    for update in update_list:
        for key in list(update['$set'].keys()):
            master_update['$set'][key] = update['$set'][key]
    return master_update


def mongo_get_connection(db_name, connect_string=None):
    """ Connects to a specified mongodb database. Optional connection string,
    otherwise connects on localhost at 27017.
    """
    try:
        if connect_string:
            client = MongoClient(connect_string)
        else:
            client = MongoClient()
        return client[db_name]
    except:
        return "Cannot make mongodb connection with specified parameters."


def mongo_get_collection(connection, collection_name):
    """ Returns a mongo collection object for a specified connection.
    """
    try:
        return connection[collection_name]
    except:
        return "Cannot retrieve {c} collection on specified connection.".format(c=collection_name)


def mongo_insert_one(collection, record, make_serial=True):
    """ Inserts a single python object into a given collection. Default is to serialize
    the object before insert.
    """
    try:
        if make_serial:
            record = json_utils.serialize(record)
        result = collection.insert_one(record)
        return result.inserted_id
    except Exception as inst:
        print('Insert failure for {0}'.format(record))
        return "Cannot insert record into specified collection."


def mongo_replace_one(collection, record, argument):
    """ Replaces a single object in the collection.
    """
    try:
        return collection.replace_one(argument, record)
    except:
        print('Could not replace record')
        return False


def mongo_remove_one(collection, record):
    """ Removes a single specified record from the specified collection, using
    the given record (Argument). For example, the record could be an entire record,
    just an id, or another key value argument. This will remove the first matching
    record with the given argument. Returns the number of records removed.
    """
    try:
        deletion = collection.delete_one(record)
        return deletion.deleted_count
    except:
        return 0


def mongo_remove_many(collection, record):
    """ Removes all documents in the given collection with the given record (argument).
    For example, the record could be an entire record,
    just an id, or another key value argument. This will remove all matching
    records with the given argument.
    """
    try:
        deletion = collection.delete_many(record)
        return deletion.deleted_count
    except:
        return 0


def mongo_update_one(collection, argument, update):
    """Updates a single record in the mongodb. Returns the updated record.
    """
    try:
        return collection.update_one(argument, update, upsert=False)
    except:
        return None


def mongo_insert_many(collection, records, make_serial=True):
    """ Inserts an array of python objects into a given collection. Default is to serialize
    the objects before insert.
    """
    try:
        if make_serial:
            result = collection.insert_many(list(map(json_utils.serialize, records)))
        else:
            result = collection.insert_many(records)
        return result.inserted_ids
    except:
        return "Cannot insert records into specified collection."


def mongo_find_records(collection, argument=None, sort=None, named_tuple=False):
    """ Finds all the records for the specified collection. Optionally serializes
    the collection into a list of named tuples (set named_tuple=True)
    """
    try:
        if named_tuple:
            nametuple_maker = record_reader.dict_to_named_tuple_closure(collection.name)
            if sort:
                return list(map(nametuple_maker, collection.find(argument).sort(sort)))
            return list(map(nametuple_maker, collection.find(argument)))
        else:
            if sort:
                return collection.find(argument).sort(sort)
            return collection.find(argument)
    except:
        return "Cannot return the documents for the specified collection."


def mongo_clear_collection(collection):
    """ Removes all documents from specified collection. Does not delete collection.
    """
    try:
        return collection.delete_many({})
    except:
        return "Cannot remove all the objects from the collection."


def mongo_remove_collection(collection):
    """ Removes all documents, indeces, and also removes collection itself.
    """
    try:
        return collection.drop()
    except:
        return "Cannot remove the specified collection."


def mongo_remove_database(database_name, connection_string=None):
    """ Removes the specified database.
    """
    try:
        connection = mongo_get_connection(database_name, connect_string=connection_string)
        connection.drop()
        return connection.drop()
    except:
        return "Cannot remove specified database."


def mongo_add_geojson_index(collection, field):
    """Adds a geojson index using GEOSPHERE to the specified field.
    Returns the new indexed field.
    """
    geo_index = collection.create_index([(field, GEOSPHERE)])
    return geo_index


if __name__ == '__main__':
    print('Please use db_utils module as method package.')
