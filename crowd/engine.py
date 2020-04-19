from abc import ABC, abstractmethod
import multiprocessing as mp

from .model import Model
from .agent import Agent, MPAgent

class Engine(ABC):
    @abstractmethod
    def run(self, model:Model, steps:int = 10):
        raise NotImplementedError(f"Must implement {self.__class__.__name__}.run")

    @abstractmethod
    def step(self):
        raise NotImplementedError(f"Must implement {self.__class__.__name__}.step")

class BasicEngine(Engine):
    def run(self, model:Model, steps:int = 10):
        #print(type(model), model, type(steps), steps)
        for step in range(steps):
            self.step(model)
            model.collect_data(step)

            if model.finish():
                return

    def step(self, model:Model):
        global_ctx = model.global_context()
        for agent in model.activate():
            #print(f'agent {agent.id}')
            agent._step(global_ctx.update(model.agent_context(agent))))
            model.update(agent)


class MPEngine(BasicEngine):
    def run(self, model:Model, steps:int = 10):
        super().run(model, steps)
        for agent in model.agents():
            agent.kill()

    def step(self, *args, **kwargs):
        super().step(*args, **kwargs)

        for agent in model.agents():
            agent.wait_step()
