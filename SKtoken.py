import logging
import random
import time
from collections import deque
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(message)s]', datefmt='%Y-%m-%d %H:%M:%S')


class SKtoken(DistProcess):

    def __init__(self, parent, initq):
        DistProcess.__init__(self, parent, initq)
        self._event_patterns = [EventPattern(Event.receive, 'request', [], [(1, 'n')], [self._event_handler_0]), EventPattern(Event.receive, 'Token', [], [(1, 'rqueue'), (2, 'rLN')], [self._event_handler_1])]
        self._sent_patterns = []
        self._label_events = {'CS': self._event_patterns, 'reply': self._event_patterns, 'starting': self._event_patterns, 'releasingCS': self._event_patterns}

    def setup(self, procList, PID, TKholder, req):
        self.myID = PID
        self.otherProcList = procList
        self.RN = createdict(self.otherProcList)
        self.LN = createdict(self.otherProcList)
        self.TKpresent = False
        self.TKheld = False
        self.prequests = req
        self.Q = deque()
        if (self.myID == TKholder):
            self.TKpresent = True
        logging.debug('process: ' + (str(self.myID)) + (' says Token with me: ') + (str(self.TKpresent)))
        self.procList = procList
        self.req = req
        self.PID = PID
        self.TKholder = TKholder

    def cs(self, task):
        self._label_('starting')
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' requesting CS ...'))
        if (self.TKpresent == False):
            self.RN[self._id] = self.RN[self._id] + (1)
            logging.debug('process ' + (str(self.myID)) + ('(%r)' % (self._id)) + (' is sending request with request value ') + (str(self.RN[self._id])))
            self.send(('request', self.RN[self._id]), self.otherProcList)
            self._label_('reply')
            while (not (self.TKpresent == True)):
                self._process_event(self._event_patterns, True, None)
        self.TKpresent = True
        self.TKheld = True
        self._label_('CS')
        task()
        self.LN[self._id] = self.RN[self._id]
        self.TKheld = False
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' exiting CS ...'))
        for p in self.otherProcList:
            if ((not (p in self.Q)) and (self.RN[p] == self.LN[p] + (1))):
                self.Q.append(p)
        if (len(self.Q) > 0):
            self.TKpresent = False
            temp = self.Q.popleft()
            logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' issuing token to process: ') + (str(temp)))
            self.send(('Token', self.Q, self.LN), temp)
        self._label_('releasingCS')
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' exiting CS ...'))

    def _event_handler_0(self, n, _timestamp, _source):
        self.RN[_source] = max(self.RN[_source], n)
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' received request from process %r ' % (_source)) + (' who has been in CS for  ') + (str(n)) + (' times'))
        if ((self.TKpresent == True) and (self.TKheld == False)):
            (self.TKpresent == False)
            self.send(('Token', self.Q, self.LN), _source)
            logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' issuing token to process: ') + (str(_source)))

    def _event_handler_1(self, rqueue, rLN, _timestamp, _source):
        self.TKpresent = True
        self.LN = rLN
        self.Q = rqueue

    def main(self):

        def cs_task():
            logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' in CS ...'))
        while True:
            self.cs(cs_task)
            t = random.randint(0, 3)
            time.sleep(t)

def createdict(otherProcList):
    temp = dict(((p, 0) for p in otherProcList))
    return temp

def main():
    if (len(sys.argv) == 3):
        numProcs = int(sys.argv[1])
        reqCount = int(sys.argv[2])
    else:
        print('number of requests not assigned, creating 10 processes as a default mechanism')
        numProcs = 10
        reqCount = 27
    use_channel('tcp')
    procList = createprocs(SKtoken, numProcs)
    assign = [0] * (numProcs)
    while reqCount:
        j = random.randrange(0, numProcs)
        assign[j]+=1
        reqCount = reqCount - (1)
    PID = 0
    j = 0
    R = random.randint(0, numProcs - (1))
    for p in procList:
        setupprocs({p}, [procList, PID, R, assign[j]])
        PID = PID + (1)
        j+=1
    try:
        startprocs(procList)
    except IOError:
        print('exiting ...\n an IO error occured\n\n')