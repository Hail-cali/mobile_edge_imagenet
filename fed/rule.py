# this is for fed learning communication & train step
# designed by

from utils.data_loader import Config
from worker.train import BaseTrainer
from worker.set import Worker

'''
w = model, loaders, criterion, optimizer, history, model_params, opt, device
'''



'''
while epoch <= opt.n_epochs:

    if epoch == start:
        # utils.debug.debug_history(history, f'client {epoch}_start')
        model.load_state_dict(copy.deepcopy(history['params']), strict=False)

    else:
        model.load_state_dict(copy.deepcopy(history['params']), strict=False)

    # train step
    history, model_params = one_epoch_train(model, loaders, criterion, optimizer,
                                            history, model_params, opt, device)

    # communication step

    await send_stream(writer, history, recipient='S', giver=self.name)

    await read_stream(reader, queue, recipient=self.name, giver='S')

    rep_his = await process_stream(queue, tasks=self.name, given='S')
    history = self.update_history(history, rep_his)

    # utils.debug.debug_history(history, 'client after read')

    epoch = history['epoch']

    if epoch % opt.log_interval == 0:
        logger(history, prefix_name(term='short') + suffix_name(opt))

'''


class ReadyPhase:

    def __init__(self, worker=None):
        if worker is None:
            self.task = Worker()

    def __call__(self, *args, **kwargs):
        w = self.task.phase(*args, **kwargs)

        return w


class TrainPhase:

    def __init__(self, trainer=None):
        if trainer is None:
            self.task = BaseTrainer(tasks=None)
        else:
            self.task = trainer

        self.best = self.task.best

    def __call__(self, *args, **kwargs):

        his, self.best = self.task.phase(*args, **kwargs)

        return his


class CommunicatePhase:

    def __init__(self, transport=None):
        if transport is None:
            self.task = None
        else:
            self.task = transport

        self.best = self.task.best

    def __call__(self, *args, **kwargs):

        his = self.task.phase(*args, **kwargs)

        return his


class EndPhase:

    def __init__(self, transport=None):
        if transport is None:
            self.task = None
        else:
            self.task = transport

        self.best = self.task.best

    def __call__(self, *args, **kwargs):

        his, self.best = self.task.phase(*args, **kwargs)

        return his


class BaseRule:

    '''
    Base Fed avg phase rule class

    -----------------------------
    should check opt setting first
    rule's config follow opt's arg ahead to config's setting
    -----------------------------

    prior option arg is bellow

    - n_epochs
    - check_point
    '''

    def __init__(self, opt=None):
        self.setup_phase = ReadyPhase()
        self.train_phase = TrainPhase()
        self.com_phase = CommunicatePhase()
        self.end_phase = EndPhase()

        self.config = Config(json_path=str('base' + '/config.json'))


        try:
            if opt is not None:
                self.config.n_epochs = opt.n_epochs

        except:
            print('CONFIG SYNCHRO Error: check config setting')

    def loop(self, x):
        w = self.setup_phase(x)
        while self.timeline:
            w = self.train_phase(w)
            w = self.com_phase(w)

        w = self.end_phase(w)

        return w

    def server_loop(self, x):
        w = self.setup_phase(x)
        while self.timeline:
            w = self.com_phase(w)

        w = self.end_phase(w)

        return w

    @property
    def timeline(self):
        return self.config.check_point <= self.config.n_epochs

    @timeline.setter
    def timeline(self, i):
        self.config.check_point = i

    def __repr__(self):
        return f'FED_BASE_RULE FROM {__name__}'






if __name__ == '__main__':
    from opt import parse_opts
    opt = parse_opts()

    c = BaseRule(opt=opt)
    print()