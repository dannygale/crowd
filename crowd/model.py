
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
        self._agents = agents if agents else []
        self._agent_dcs = agent_dcs if agent_dcs else {}
        self._model_dcs = model_dcs if model_dcs else {}

        self.activation = activation

        self._agent_df = None
        self._model_df = None

    def init_data(self):
        cols = ['step', ] + [ name for name in self._model_dcs]
        self._model_data = { k:list() for k in cols }
        cols = ['step', 'agent'] + [ name for name in self._agent_dcs]
        self._agent_data = { k:list() for k in cols }

    def collect_data(self, step):
        """ Collect the data we need for each time step """
        #print(f'collecting data for step {step}')
        for agent in self.agents():
            self._agent_data['step'].append(step)
            self._agent_data['agent'].append(agent.id)
            for name, collector in self._agent_dcs.items():
                self._agent_data[name].append(collector(agent))

        self._model_data['step'].append(step)
        for name, collector in self._model_dcs.items():
            self._model_data[name].append(collector(self))

    @property
    def num_agents(self):
        return len(self._agents)

    def agents(self):
        return iter(self._agents)

    def agent_data(self):
        return self._agent_data

    def agent_df(self):
        if self._agent_df:
            return self._agent_df
        self._agent_df = pd.DataFrame.from_dict(self.agent_data())
        return self._agent_df
        
    def model_data(self):
        return self._model_data

    def model_df(self):
        if self._model_df:
            return self._model_df
        self._model_df = pd.DataFrame.from_dict(self.model_data())
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

    def end_of_step(self):
        ''' Do any handling that needs to be done between steps '''
        pass

    def finish(self):
        ''' Return a boolean indicating if execution should stop '''
        pass

    def activate(self):
        ''' Yield the agents in the order they should be run '''
        return self.activation(self._agents)



