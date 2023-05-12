import argparse

def parse_opts():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type=str,
                        default='uf101', help='dataset type')

    parser.add_argument('--SERVER_PORT', type=int,
                        default=59919)

    parser.add_argument('--SERVER_HOST', type=str,
                        default='127.0.0.2')

    parser.add_argument('--CLIENT_PORT', type=int,
                        default=59919)

    parser.add_argument('--CLIENT_HOST', type=str,
                        default='127.0.0.2')

    parser.add_argument('--TIMEOUT', type=int,
                        default=100)

    parser.add_argument(
        '--root_path',
        default='/root/data/edge',
        type=str,
        help='Root directory path of data')






    parser.add_argument(
        '--file_path',
        default='../dataset/cifar-10-batches-py',
        type=str,
        help='Root directory path of data')

    parser.add_argument(
        '--gpu',
        default=0,
        type=int)

    parser.add_argument(
        '--log_interval',
        default=5,
        type=int,
        help='Log interval for showing training loss')

    parser.add_argument(
        '--save_interval',
        default=2,
        type=int,
        help='Model saving interval')

    parser.add_argument(
        '--model',
        default='fedavg',
        type=str,
        help=
        'mobilenet | fedavg')

    parser.add_argument(
        '--pretrained',
        default=True,
        type=bool)

    parser.add_argument(
        '--testmode',
        default=True,
        type=bool)

    parser.add_argument(
        '--n_classes',
        default=400,
        type=int,
        help=
        'Number of classes (activitynet: 200, kinetics: 400 or 600, ucf101: 101, hmdb51: 51)'
    )
    parser.add_argument(
        '--lr_rate',
        default=1e-3,
        type=float,
        help='Initial learning rate (divided by 10 while training by lr scheduler)')

    parser.add_argument(
        '--use_cuda',
        action='store_true',
        help='If true, use GPU.')
    parser.set_defaults(std_norm=False)

    parser.add_argument(
        '--optimizer',
        default='sgd',
        type=str,
        help='Currently only support SGD')

    parser.add_argument(
        '--lr_patience',
        default=10,
        type=int,
        help='Patience of LR scheduler. See documentation of ReduceLROnPlateau.'
    )
    parser.add_argument(
        '--batch_size', default=32, type=int, help='Batch Size')

    parser.add_argument(
        '--train_size', default=0.8, type=float, help='Train Size')

    parser.add_argument(
        '--n_epochs',
        default=1,
        type=int,
        help='Number of total epochs to run')

    parser.add_argument(
        '--start_epoch',
        default=1,
        type=int,
        help='Training begins at this epoch. Previous trained model indicated by resume_path is loaded.'
    )
    parser.add_argument(
        '--resume_path',
        type=str,
        help='Resume training')
    parser.add_argument(
        '--pretrain_path', default='', type=str, help='Pretrained model (.pth)')

    parser.add_argument(
        '--k_clients',
        default=2,
        type=int,
        help='Number of Client')

    parser.add_argument(
        '--num_workers',
        default=4,
        type=int,
        help='Number of threads for multi-thread loading')
    parser.add_argument(
        '--norm_value',
        default=1,
        type=int,
        help='If 1, range of inputs is [0-255]. If 255, range of inputs is [0-1].')
    parser.add_argument(
        '--std_norm',
        action='store_true',
        help='If true, inputs are normalized by standard deviation.')

    args = parser.parse_args()

    return args
