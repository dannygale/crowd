
import multiprocessing as mp
from collections import OrderedDict
from threading import Thread
from queue import Queue

class Agent:
    def __init__(self, uid:int, *args, **kwargs):
        self.id = uid
        self.setup(*args, **kwargs)

    def setup(*args, **kwargs):
        pass

    def _step(self, context):
        self.step(context)

    def step(self, context):
        pass

    def wait_step(self):
        return


class StagedAgent(Agent):
    """ An Agent that supports multiple stages per step
    stages are traversed in order
    """
    def __init__(self, uid:int, stages: OrderedDict[str,str] = None, *args, **kwargs):
        self.stages = stages
        for stage, method_name in self.stages.items():
            if not hasattr(self, method_name):
                raise ValueError(f"{method_name} does not exist in {self.__class__.__name__} for stage {stage}")
        self.current_stage = self.stages.keys()[0]
        self.current_stage_num = 0

        super().__init__(uid, *args, **kwargs)

    def step(self, context):
        if self.current_stage is None:
            self.current_stage = self.stages.keys()[0]

        # TODO: step through stages and call functions
        getattr(self, self.stages[self.current_stage])(context)
        self.current_stage = self.next_stage()

    def next_stage(self):
        self.current_stage_num += 1
        if self.current_stage_num >= len(self.stages): 
            self.current_stage_num = 0
        return list(self.stages)[self.current_stage_num]

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




class MPAgent(Agent):
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
                if self.die.is_set():
                    return
            else:
                self.step(ctx)
                self.queue.task_done()

    def _step(self, context = {}):
        self.queue.put(context)

    def kill(self):
        self.die.set()

    def wait_step(self):
        self.queue.join()

