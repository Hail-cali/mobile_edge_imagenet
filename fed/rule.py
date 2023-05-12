# this is for fed learning communication & train step
# designed by

from utils.data_loader import Config
from worker.train import BaseTrainer
from worker.set import Setter
from communicate.request import Transporter


class ReadyPhase:

    def __init__(self, worker=None):
        if worker is None:
            self.worker = Setter()

    def __call__(self, *args, **kwargs):
        w = self.worker.phase(*args, **kwargs)

        return w


class TrainPhase:

    def __init__(self, trainer=None):
        if trainer is None:
            self.worker = BaseTrainer(tasks=None)
        else:
            self.worker = trainer

        self.best = self.worker.best

    def __call__(self, *args, **kwargs):

        his, self.best = self.worker.phase(*args, **kwargs)

        return his


class CommunicatePhase:

    def __init__(self, streamer, transport=None):
        if transport is None:
            self.worker = Transporter(tasks=None, stream=streamer)
        else:
            self.worker = transport

        # self.best = self.worker.best

    def close(self):
        self.worker.close()

    async def __call__(self, *args, **kwargs):

        his = await self.worker.phase(*args, **kwargs)

        return his


class EndPhase:

    def __init__(self, worker=None, transport=None):
        if transport is None:
            self.worker = None
        else:
            self.worker = worker

        self.best = self.worker.best

    def __call__(self, *args, **kwargs):

        his, self.best = self.worker.phase(*args, **kwargs)

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