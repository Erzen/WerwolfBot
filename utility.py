import os.path as path
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

def save_object(obj, filename):
    try:
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    except IOError:
        print("An Error occured during the writing of the File '{}'".format(filename))

def load_object(filename):
    if path.exists(filename) and path.isfile(filename) and path.getsize(filename) > 0:
        try:
            with open(filename, 'rb') as input:  # Overwrites any existing file.
                object = pickle.load(input)
            return object
        except IOError:
            print("An Error occured during the reading of the File '{}'".format(filename))
    return None