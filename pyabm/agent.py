
class Agent:
    def __init__(self, uid:int, *args, **kwargs):
        self.id = uid
        self.init(*args, **kwargs)

    def init(*args, **kwargs):
        pass

    def _step(self, context):
        self.step(context)

    def step(self, context):
        pass

from threading import Thread
from queue import Queue
class ThreadedAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = Thread(target=self._thread)
        self.queue = Queue()

        self.thread.start()

    def _thread(self):
        while True:
            try:
                ctx = self.queue.get(timeout = 1)
            except Empty:
                # TODO: check if killed
                pass
            else:
                self.step(ctx)

    def _step(self, context = {}):
        self.queue.put(context)



import multiprocessing as mp

class MPAgent:
    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subproc = mp.Process(target=self._thread)
        self.queue = mp.JoinableQueue()

        self.die = mp.Event()

        self.subproc.start()

    def _thread(self):
        while True:
            try:
                ctx = self.queue.get(timeout = 1)
            except Empty:
                # TODO: check if killed
                if self.die.is_set():
                    return
            else:
                self.agent.step(ctx)
                self.queue.task_done()

    def _step(self, context = {}):
        self.queue.put(context)

    def kill(self):
        self.die.set()

