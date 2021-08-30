import matplotlib.pyplot as plt

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

path = '../dataset/cifar-10-batches-py'

result = unpickle(path, 2)

print()

X, y = make_dataset(result)

plt.imshow(X[100])
plt.show()