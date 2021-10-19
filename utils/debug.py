from sys import getsizeof


def debug_history(his, where):

    where: str
    his: dict

    print(f"\n{'-'*10}iter|[{his['epoch']}]debug phrase in {where} {'-'*10}")
    print(f'history total {his.keys()}')

    print(f'params status', end=' ')
    print(len(his['params'].keys()))
    params_list = list(his['params'].keys())
    print(his['params'][params_list[-1]].shape)
    print(params_list[-1], his['params'][params_list[-1]][-1])
    print(type(his['params']))
    print(his['params']['features.0.0.weight'].shape, end='\n')

    print(f"epoch {his['epoch']} | type: {type(his['epoch'])}",end='\n')
    print(f"train {his['train_los']} | type: {type(his['train_los'])}", end='\n')
    print(f"{'-' * 15}{'-' * 15}\n")

def debug_comm(msg, where):
    print(f"\n{'-' * 10} in {where} {'-' * 10}")
    print(f'{where} size of arg {getsizeof(msg)}')

    if isinstance(msg, bytes):
        print(f'last msg ', end='')
        print(msg[-5:])
        print(msg[-1:])
        print(msg[-2:])
        print(msg[-3:-1])

    elif isinstance(msg, dict):
        pass

    print(f"{'-' * 15}{'-' * 15}\n")


def verbose(his, i):

    # print(f"\n {'='*3} verbose {'='*3}")
    if i % 2 == 0:
        print(f"epoch: {his['epoch']} | train_loss {his['train_los'][-1]}", end=' | ')
        print(f"train_acc {his['train_acc'][-1]}")

        print(f"val_loss {his['val_los'][-1]}", end=' | ')
        print(f"val_acc {his['val_acc'][-1]}")



def get_latent_layer(model):
    features = {}
    for name, layer in enumerate(model.children):
        x = layer(x)

    pass


