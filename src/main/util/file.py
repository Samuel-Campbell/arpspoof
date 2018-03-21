import os
import joblib
import sys


class File:
    def __init__(self):
        pass

    @staticmethod
    def load_binary(directory, filename):
        """
        returns binarized model
        :param filename: name of file to load
        :return: None
        """
        try:
            print("Loading " + filename)
            root_directory = os.path.abspath(__file__ + "r/../../../")
            rel_path = r'data/' + directory + '/' + filename
            file_path = os.path.join(root_directory, rel_path)
            file = open(file_path, "rb")
            binary = joblib.load(file)
            print(filename + " is successfully loaded")
            return binary
        except BaseException:
            print('File not found')


    @staticmethod
    def save_binary(directory, filename, model):
        """
        saves a binary model
        :return: None
        """

        root_directory = os.path.abspath(__file__ + "r/../../../")
        if sys.platform == 'win32':
            bin_dir = 'data\\' + directory + '\\'
        else:
            bin_dir = r'data/' + directory + '/'
        file_path = os.path.join(root_directory, bin_dir)
        if not(os.path.isdir((file_path))):
            os.mkdir(file_path)
        bin_dir = bin_dir + filename
        file_path = os.path.join(root_directory, bin_dir)
        print("saving " + filename + " to: " + file_path)
        joblib.dump(model, file_path)
        print(filename + " saved to: " + file_path)
