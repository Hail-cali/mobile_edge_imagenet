import matplotlib.pyplot as plt
import torch.utils.data as data
import numpy as np
import json

class Config:
    def __init__(self, json_path):
        with open(json_path, mode='r') as io:
            params = json.loads(io.read())
        self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, mode='w') as io:
            json.dump(self.__dict__, io, indent=4)

    def update(self, json_path):
        with open(json_path, mode='r') as io:
            params = json.loads(io.read())
        self.__dict__.update(params)

    @property
    def dict(self):
        return self.__dict__

def open_data(filepath):
    import pickle

    with open(filepath, 'rb') as fo:
        result = pickle.load(fo, encoding='bytes')

    return result

def unpickle(file, batch_num):
    import pickle
    import os
    batch_file = 'data_batch_' + str(batch_num)
    file_path =  os.path.join(file, batch_file)
    with open(file_path, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')

    return dict

def make_dataset( dict):
    return dict[b'data'].reshape(len(dict[b'data']), 3, 32, 32).transpose(0, 2, 3, 1), np.array(dict[b'labels'])

def unmat(file):
    from scipy import io
    mat_file = io.loadmat(file)
    return mat_file


class CustomDataset(data.Dataset):

    def __init__(self, data_path):
        super(CustomDataset, self).__init__()

        import pandas as pd
        data = pd.read_csv(data_path)

        self.X, self.y = self.make_dataset(data)

    def make_dataset(self, dict):
        return dict[b'data'].reshape(len(dict[b'data']), 3, 32, 32).astype('float32'), np.array(dict[b'labels'])

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)


class ImageDataset(data.Dataset):

    def __init__(self, data, test_mode=False):
        super(ImageDataset, self).__init__()
        if not test_mode:
            self.X, self.y = self.make_dataset(data)
        else:
            self.X, self.y = self.make_dataset(data)
            self.X, self.y = self.X[:400], self.y[:400]
        # self.X_len = self.X.shape[0]


    def make_dataset(self, dict):
        return dict[b'data'].reshape(len(dict[b'data']), 3, 32, 32).astype('float32'), np.array(dict[b'labels'])
        # return dict[b'data'].reshape(len(dict[b'data']), 3, 32, 32).transpose(0, 2, 3, 1), np.array(dict[b'labels'])

    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)
