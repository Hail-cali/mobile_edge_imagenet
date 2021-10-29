import matplotlib.pyplot as plt
plt.style.use('seaborn')

def prefix_name(term='long'):
    from datetime import datetime
    import os

    if term == 'long':
        done_time =datetime.today().strftime("%Y-%m-%d::%H:%M:%S:%p")
        name = os.name + '_' + done_time
    else:
        done_time = datetime.today().strftime("%m-%d")
        name = os.name + '_' + done_time

    return name

def suffix_name(option=None):

    def wrap(name):
        return '(' + name + ')'

    if option is None:
        from opt import parse_opts

        OPT = parse_opts()
        return wrap(OPT.model)

    else:
        return wrap(option.model)


def logger(his, name):
    import os
    from collections import defaultdict
    import pickle

    DIR = 'log'
    DIR_PATH = os.path.join('..', DIR)
    if DIR not in os.listdir('../'):
        os.mkdir(DIR_PATH)

    logger = defaultdict()

    try:
        logger.update({'train_los': his['train_los'],
                       'val_los': his['val_los'],
                       'train_acc': his['train_acc'],
                       'val_acc': his['val_acc']
                        })
    except:
        print(f'Type error: check {his}')

    with open(os.path.join(DIR_PATH, f"{name}.pkl"), 'wb') as f:
        pickle.dump(logger, f)

    print(f'log saved in {DIR_PATH}/{name}.pkl')





def history_plot(his, name):
    """

    :param his: [dict,list] (train_acc, train_los, val_acc, val_los)
    :return: None
    """
    save_dir = 'img'

    import os
    if not save_dir in os.listdir('../'):
        os.mkdir('../'+save_dir)


    plt.plot(range(len(his['val_los'])), his['val_los'], marker='.', c='red', label="Validation-set Loss")
    plt.plot(range(len(his['train_los'])), his['train_los'], marker='.', c='blue', label="Train-set Loss")

    plt.legend(loc='upper right')
    plt.grid()
    plt.title(name)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()
    plt.savefig(f"../img/{name}_loss.png")

    plt.plot(range(len(his['val_acc'])), his['val_acc'], marker='.', c='red', label="Validation-set acc")
    plt.plot(range(len(his['train_acc'])), his['train_acc'], marker='.', c='blue', label="Train-set acc")

    plt.legend(loc='upper right')
    plt.grid()
    plt.title(name)
    plt.xlabel('epoch')
    plt.ylabel('Acc')
    plt.show()
    plt.savefig(f"../{save_dir}/{name}_acc.png")




def loss_plot(train_loss, val_loss, epoch, name):

    plt.plot(epoch, val_loss, marker='.', c='red', label="Validation-set Loss")
    plt.plot(epoch, train_loss, marker='.', c='blue', label="Train-set Loss")

    plt.legend(loc='upper right')
    plt.grid()
    plt.title(name)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()
    plt.savefig(f"../img/{name}_loss.png")
    return

def acc_plot(train_acc, val_acc, epoch, name):
    plt.plot(epoch, val_acc, marker='.', c='red', label="Validation-set acc")
    plt.plot(epoch, train_acc, marker='.', c='blue', label="Train-set acc")

    plt.legend(loc='upper right')
    plt.grid()
    plt.title(name)
    plt.xlabel('epoch')
    plt.ylabel('Acc')
    plt.show()
    plt.savefig(f"../img/{name}_acc.png")
    return




if __name__=='__main__':
    temp = {'train_los':[1],
                       'val_los': [0.2],
                       'train_acc': [0.3],
                       'val_acc': [0.8]
                        }
    logger(temp, prefix_name()+suffix_name())

