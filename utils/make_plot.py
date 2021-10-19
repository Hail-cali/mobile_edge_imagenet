import matplotlib.pyplot as plt
# import seaborn as sns
plt.style.use('seaborn')
import numpy as np

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





