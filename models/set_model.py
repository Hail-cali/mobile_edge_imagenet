from models.lightmobile import *

import torch.optim as optim

from utils.data_loader import *
from utils.epoch_loader import *

import copy


def load_model(opt):
    if opt.model == 'mobilenet':
        model = LightMobileNet(pretrained=opt.pretrained).load()

    else:
        model = None
        print(f'check opt model, invalid model name {opt.model} \n | capable opt is | mobilenet |')

    return model



def set_model(model, opt, dpath='../dataset/cifar-10-batches-py',file=3, train_size=0.8, batch_size=40, testmode=False):


    device = torch.device(f"cuda:{opt.gpu}" if opt.use_cuda else "cpu")
    print(device, 'use')

    result = unpickle(dpath, file)

    dataset = ImageDataset(data=result, test_mode=testmode)

    train, val = data.random_split(dataset,
                                   [int(len(dataset) * train_size), len(dataset) - int(len(dataset) * train_size)])

    train_loader = data.DataLoader(train, batch_size=batch_size, shuffle=True)

    val_loader = data.DataLoader(val, batch_size=batch_size, shuffle=True)

    print()
    # model = LightMobileNet(pretrained=True).load()
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    history = dict(epoch=0, train_los=[], train_acc=[], val_los=[], val_acc=[], params=copy.deepcopy(model.state_dict()))

    best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = 10000.0

    model_params = dict(best_params=best_model_wts, best_loss=best_loss)

    return (train_loader, val_loader),  criterion, optimizer, history, model_params, device


def one_epoch_train(model, loaders, criterion, optimizer, history, model_params, opt, device):

    train_loader, val_loader = loaders

    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, history['epoch'], opt.log_interval, device)
    history['train_los'].append(train_loss), history['train_acc'].append(train_acc)

    val_loss, val_acc = val_epoch(model, val_loader, criterion, device)
    history['val_los'].append(val_loss), history['val_acc'].append(val_acc)

    history['params'] = copy.deepcopy(model.state_dict())
    history['epoch'] += 1

    if val_loss < model_params['best_loss']:
        model_params['best_loss'] = val_loss
        model_params['best_params'] = copy.deepcopy(model.state_dict())

    return history, model_params



# def full_epoch_train(model, loaders, criterion, optimizer, history, model_params, device):
#
#
#     train_loader, val_loader = loaders
#
#     for epoch in range(OPT.start_epoch, OPT.n_epochs + 1):
#
#         train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, epoch, opt.log_interval, device)
#         history['train_los'].append(train_loss), history['train_acc'].append(train_acc)
#
#         val_loss, val_acc = val_epoch(model, val_loader, criterion, device)
#         history['val_los'].append(val_loss), history['val_acc'].append(val_acc)
#         history['params'] = copy.deepcopy(model.state_dict())
#
#         if val_loss < model_params['best_loss']:
#             model_params['best_loss'] = val_loss
#             model_params['best_params'] = copy.deepcopy(model.state_dict())
#
#     return history, model_params


if __name__=='__main__':

    from opt import parse_opts
    opt = parse_opts()

    model = load_model(opt)

    loaders, criterion, optimizer, history, model_params, device = set_model(
        model,
        opt,
        dpath='../dataset/cifar-10-batches-py',
        file=1,
        train_size=0.8,
        batch_size=40,
        testmode=True)

    print()