from abc import ABC, abstractmethod

from .model import Model
from .agent import Agent, MPAgent

class Engine(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError(f"Must implement {self.__class__.__name__}.run")

class BasicEngine(Engine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, model:Model, steps:int = 10):
        print(type(model), model, type(steps), steps)
        for step in range(steps):
            self.step(model)
            model.collect_data(step)

            if model.finish():
                return

    def step(self, model:Model):
        #print(f'step {step}')
        #print(f'context: {ctx}')
        for agent in model.activate():
            ctx = model.context(agent)
            #print(f'agent {agent.id}')
            agent._step(ctx)
            model.update(agent)


import multiprocessing as mp
from .agent import MPAgent

class MPEngine(Engine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subproc = mp.Process(target = self._thread)
        self._queue = mp.Queue()

    def run(self, model:Model, steps:int = 10):
        self._subproc.start()

        super().run(model, steps)

        for agent in model.agents():
            agent.kill()

