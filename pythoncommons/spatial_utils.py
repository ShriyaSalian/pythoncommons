# import shapefile (unavailable on server, look for alternatives)
import geojson
# dummy push 2


def make_point(x, y, z=None):
    if z:
        point = geojson.Point([x, y, z])
    else:
        point = geojson.Point([x, y])
    return point


def read_shapefile(path):
    """Reads and returns a shapefile at a given path.
    """
    shape = 'dummy'
    # shape = shapefile.Reader(path)
    return shape


if __name__ == '__main__':
    print("Please use as method package.")
