import time
import random
import multiprocessing
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(message)s]', datefmt='%Y-%m-%d %H:%M:%S')


class RAtoken(DistProcess):

    def __init__(self, parent, initq):
        DistProcess.__init__(self, parent, initq)
        self._event_patterns = [EventPattern(Event.receive, 'Request', [], [(1, 'ts')], [self._event_handler_0]), EventPattern(Event.receive, 'Token', [], [(1, 'Token')], [self._event_handler_1])]
        self._sent_patterns = []
        self._label_events = {'cs': self._event_patterns, 'reply': self._event_patterns, 'starting': self._event_patterns, 'releasingCS': self._event_patterns}

    def setup(self, procList, PID, TKholder, req):
        self.ts = 0
        self.myID = PID
        self.otherProcList = procList
        self.requests = createdict(self.otherProcList)
        self.token = createdict(self.otherProcList)
        self.TKpresent = False
        self.TKheld = False
        self.prequests = req
        if (PID == TKholder):
            self.TKpresent = True
        logging.debug('process: ' + (str(self.myID)) + (' says Token with me: ') + (str(self.TKpresent)))
        self.procList = procList
        self.req = req
        self.PID = PID
        self.TKholder = TKholder

    def cs(self, task):
        self._label_('starting')
        self.ts = self.ts + (1)
        self.requests[self._id] = self.ts
        logging.debug('process ' + (str(self.myID)) + ('(%r)' % (self._id)) + (' is requesting CS'))
        if (self.TKpresent == False):
            logging.debug('process ' + (str(self.myID)) + ('(%r)' % (self._id)) + (' is sending reques with TS as ') + (str(self.ts)))
            self.send(('Request', self.ts), self.otherProcList)
            self._label_('reply')
            while (not (self.TKpresent == True)):
                self._process_event(self._event_patterns, True, None)
        self.TKheld = True
        self._label_('cs')
        task()
        self._label_('releasingCS')
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' exiting cs ...'))
        self.prequests = self.prequests - (1)
        if (self.prequests == 0):
            logging.debug('process ' + (str(self.myID)) + ('(%r)' % (self._id)) + (' has finished all its requests, bye...'))
        self.token[self._id] = self.ts
        self.TKheld = False
        for p in self.otherProcList:
            if (self.requests[p] <= self.token[p]):
                continue
            else:
                logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' issuing token to process: ') + (str(p)))
                self.TKpresent = False
                self.send(('Token', self.token), p)
                break

    def _event_handler_0(self, ts, _timestamp, _source):
        self.requests[_source] = max(self.requests[_source], ts)
        logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' received request from process %r ' % (_source)) + (' with timestamp ') + (str(ts)))
        if ((self.TKpresent == True) and (self.TKheld == False)):
            for p in self.otherProcList:
                if (self.requests[p] <= self.token[p]):
                    continue
                else:
                    logging.debug('process: ' + (str(self.myID)) + (' (%r)' % (self._id)) + (' issuing token to process: ') + (str(p)))
                    self.TKpresent = False
                    self.token[_source] = ts
                    self.send(('Token', self.token), p)
                    break

    def _event_handler_1(self, Token, _timestamp, _source):
        self.TKpresent = True
        self.token = Token
        self.token[self._id] = self.ts

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
    procList = createprocs(RAtoken, numProcs)
    assign = [0] * (numProcs)
    while reqCount:
        j = random.randrange(0, numProcs)
        assign[j]+=1
        reqCount = reqCount - (1)
    PID = 0
    j = 0
    R = random.randint(0, numProcs - (1))
    for p in procList:
        setupprocs({p}, [procList - ({p}), PID, R, assign[j]])
        PID = PID + (1)
        j+=1
    try:
        startprocs(procList)
    except IOError:
        print('exiting ...\n an IO error occured\n\n')