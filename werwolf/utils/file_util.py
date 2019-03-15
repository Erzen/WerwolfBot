import os.path as path
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

def save_object(obj, filename):
    file_path = "./pickleFiles/{}".format(filename)
    try:
        with open(file_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    except IOError:
        print("An Error occured during the writing of the File '{}'".format(file_path))

def load_object(filename):
    file_path = "./pickleFiles/{}".format(filename)
    if path.exists(file_path) and path.isfile(file_path) and path.getsize(file_path) > 0:
        try:
            with open(file_path, 'rb') as input:  # Overwrites any existing file.
                object = pickle.load(input)
            return object
        except IOError:
            print("An Error occured during the reading of the File '{}'".format(file_path))
    return None