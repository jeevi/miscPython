import random


class P(DistProcess):

    def __init__(self, parent, initq):
        DistProcess.__init__(self, parent, initq)
        self._event_patterns = [EventPattern(Event.receive, 'Request', [], [], [self._event_handler_0]), EventPattern(Event.receive, 'Reply', [], [(1, 'lc')], [self._event_handler_1])]
        self._sent_patterns = []
        self._label_events = {'cs': self._event_patterns, 'start': self._event_patterns, 'end': self._event_patterns, 'release': self._event_patterns, 'reply': self._event_patterns}

    def setup(self, ps, requests):
        self.reqc = None
        self.s = ps
        self.waiting = set()
        self.replied = set()
        self.ps = ps
        self.requests = requests

    def cs(self, task):
        self._label_('start')
        self.reqc = self.logical_clock()
        self.send(('Request', self.reqc), self.s)
        self._label_('reply')
        while (not (len(self.replied) == len(self.s))):
            self._process_event(self._event_patterns, True, None)
        self._label_('cs')
        task()
        self._label_('release')
        self.reqc = None
        self.output('Is releasing.')
        self.send(('Reply', 
        self.logical_clock()), self.waiting)
        self._label_('end')
        self.waiting = set()
        self.replied = set()

    def main(self):

        def anounce():
            self.output('In cs!')
        while True:
            self.cs(anounce)

    def _event_handler_0(self, _timestamp, _source):
        if ((self.reqc == None) or ((_timestamp, _source) < (self.reqc, self._id))):
            self.send(('Reply', 
            self.logical_clock()), _source)
        else:
            self.waiting.add(_source)

    def _event_handler_1(self, lc, _timestamp, _source):
        if ((self.reqc != None) and (lc > self.reqc)):
            self.replied.add(_source)

def main():
    ps = createprocs(P, int(sys.argv[1]))
    proc = int(sys.argv[1])
    req = int(sys.argv[2])
    assign = [0] * (proc)
    time.sleep(5)
    while req:
        j = random.randrange(0, proc)
        assign[j]+=1
        req = req - (1)
    j = 0
    for p in ps:
        setupprocs([p], [ps - ({p})])
        j = j + (1)
    time.sleep(5)
    startprocs(ps)
    time.sleep(5)