
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
            agent_dcs: Dict[str, Callable] = None, # dcs = data collectors
            model_dcs: Dict[str, Callable] = None,
            activation: Callable = basic_activation
            ):
        self._agents = agents if agents else {}
        self._agent_dcs = agent_dcs if agent_dcs else {}
        self._model_dcs = model_dcs if model_dcs else {}

        self.activation = activation

    def init_data(self):
        #self._agent_df['agent'] = None
        #self._agent_df['step'] = None
        mi = pd.MultiIndex.from_product([[ 0 ], [ agent.id for agent in self._agents ]],
                names = ['step', 'agent'])
        self._agent_df = pd.DataFrame(index=mi)
        for name, collector in self._agent_dcs.items():
            self._agent_df[name] = None

        self._model_df = pd.DataFrame()
        self._model_df['step'] = None
        for name, collector in self._model_dcs.items():
            self._model_df[name] = None

    def collect_data(self, step):
        """ Collect the data we need for each time step """
        #print(f'step {step}: collecting data')
        for agent in self.agents():
            for name, collector in self._agent_dcs.items():
                self._agent_df.loc[(step, agent.id), name] = collector(agent)

        for name, collector in self._model_dcs.items():
            self._model_df.loc[step, name] = collector(self)

    def agents(self):
        return iter(self._agents)

    def agent_data(self):
        return self._agent_df

    def model_data(self):
        return self._model_df

    ''' Methods below are expected to be overridden as needed '''

    def global_context(self):
        """ Generate the global context for each step. The same global context
        is passed to every agent """
        return {}

    def agent_context(self, agent):
        """ Generate the context for each agent for each step. The 
        global context is updated with the agent context and passed to the 
        agent as a single context. Duplicate keys in the global and agent 
        contexts will receive the value specified in the agent_context"""
        return {}

    def update(self, agent):
        """ Integrate agent state changes """
        pass

    def finish(self):
        ''' Return a boolean indicating if execution should stop '''
        pass

    def activate(self):
        ''' Yield the agents in the order they should be run '''
        return self.activation(self._agents)



