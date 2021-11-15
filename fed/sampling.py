
'''
client sampling rule: base rule is no-sampling which means should contains all client's train params
when update fed learning
'''



class BaseSamplingRule:

    def __init__(self):
        self.rule = None



