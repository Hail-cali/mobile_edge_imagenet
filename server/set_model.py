import torch
from opt import parse_opts
from utils.data_loader import *
import os
from models.lightmobile import *
import torch.optim as optim
from utils.loader import *

def set_server_model(dpath='../dataset/cifar-10-batches-py',train_size=0.8, batch_size=30):
    opt = parse_opts()
    device = torch.device(f"cuda:{opt.gpu}" if opt.use_cuda else "cpu")
    print(device, 'use')

    result = unpickle(dpath, 3)
    dataset = ImageDataset(data=result)
    train, val = data.random_split(dataset,
                                   [int(len(dataset) * train_size), len(dataset) - int(len(dataset) * train_size)])

    train_loader = data.DataLoader(train, batch_size=batch_size, shuffle=True)
    val_loader = data.DataLoader(val, batch_size=batch_size, shuffle=True)

    print()
    model = LightMobileNet(pretrained=True).load()
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    start_epoch = 1
    for epoch in range(start_epoch, opt.n_epochs +1):
        val_loss, val_acc = val_epoch(model, val_loader, criterion, device)




if __name__=='__main__':
    set_server_model(dpath='../dataset/cifar-10-batches-py', train_size=0.8, batch_size=40)
