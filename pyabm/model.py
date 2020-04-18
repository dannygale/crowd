
from typing import *
from abc import ABC, abstractmethod

from .agent import *
from .engine import *
from .activation import *
from .grid import *

import pandas as pd

class Model:
    """A model containing a number of agents"""

    def __init__(self, 
            agents:List[Agent] = None, 
            agent_data: Dict[str, Callable] = None,
            model_data: Dict[str, Callable] = None,
            ):
        self._agents = agents if agents else {}
        self._agent_data = agent_data if agent_data else {}
        self._model_data = model_data if model_data else {}

        self._data = {}

    def init_data(self):
        #self._agent_df['agent'] = None
        #self._agent_df['step'] = None
        mi = pd.MultiIndex.from_product([[ 0 ], [ agent.id for agent in self._agents ]],
                names = ['step', 'agent'])
        self._agent_df = pd.DataFrame(index=mi)
        for name, collector in self._agent_data.items():
            self._agent_df[name] = None

        self._model_df = pd.DataFrame()
        self._model_df['step'] = None
        for name, collector in self._model_data:
            self._model_df[name] = None

    def collect_data(self, step):
        """ Collect the data we need for each time step """
        #print(f'step {step}: collecting data')
        for agent in self.agents():
            for name, collector in self._agent_data.items():
                self._agent_df.loc[(step, agent.id), name] = collector(agent)

        for name, collector in self._model_data.items():
            self._model_df.loc[step, name] = collector(self)

    def context(self):
        """ Generate the context passed to each agent for each step """
        pass

    def update(self, agent):
        """ Integrate agent state changes """
        pass

    def finish(self):
        ''' Return a boolean indicating if execution should stop '''
        pass

    def activate(self):
        ''' Yield the agents in the order they should be run '''
        pass

    def agents(self):
        return iter(self._agents)
    def agent_data(self):
        return self._agent_df
    def model_data(self):
        return self._model_df


