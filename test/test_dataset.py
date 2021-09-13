import matplotlib.pyplot as plt
from models.lightmobile import LightMobileNet
from utils.data_loader import ImageDataset
from utils.data_loader import *

def unpickle(file, batch_num):
    import pickle
    import os
    batch_file = 'data_batch_' + str(batch_num)
    file_path =  os.path.join(file, batch_file)
    with open(file_path, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')

    return dict

def make_dataset(dict):

    return dict[b'data'].reshape(len(dict[b'data']), 3, 32, 32).transpose(0, 2, 3, 1), dict[b'labels']

def unmat(file):
    from scipy import io
    mat_file = io.loadmat(file)
    return mat_file





dpath='../dataset/cifar-10-batches-py'
train_size=0.8
batch_size=30

# result = unpickle(dpath, 2)
# X, y = make_dataset(result)
# plt.imshow(X[100])
# plt.show()

result = unpickle(dpath, 3)
dataset = ImageDataset(data=result)
train, val = data.random_split(dataset,
                                   [int(len(dataset) * train_size), len(dataset) - int(len(dataset) * train_size)])

train_loader = data.DataLoader(train, batch_size=batch_size, shuffle=True)
val_loader = data.DataLoader(val, batch_size=batch_size, shuffle=True)

print()