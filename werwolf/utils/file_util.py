import logging
import os.path as path

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

logger = logging.getLogger(__name__)


def save_object(obj, filename):
    file_path = "./pickleFiles/{}".format(filename)
    try:
        with open(file_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print("An Error occured during the writing of the File '{}'".format(file_path))
        logger.exception(e)

def load_object(filename):
    file_path = "./pickleFiles/{}".format(filename)
    if path.exists(file_path) and path.isfile(file_path) and path.getsize(file_path) > 0:
        try:
            with open(file_path, 'rb') as input:  # Overwrites any existing file.
                object = pickle.load(input)
            return object
        except IOError as e:
            print("An Error occured during the reading of the File '{}'".format(file_path))
            logger.exception(e)
    return None