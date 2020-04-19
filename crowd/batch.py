
from itertools import product
from typing import *

import pandas as pd
from tqdm import tqdm

from .model import Model
from .engine import Engine, BasicEngine
from .activation import *
from .sim import Simulation

class Batch:
    def __init__(self, 
            model_cls:type, 
            engine:Engine = None,
            steps:int = 10,
            iterations:int = 1,
            parameters:Dict[str,Any] = { },
            variables:Dict[str, List[Any]] = { },
            agent_dcs:Dict[str,Callable] = { },
            model_dcs:Dict[str, Callable] = { }
            ):

        self.model_cls = model_cls
        self.engine = engine if engine else BasicEngine()
        self.steps = steps
        self.iterations = iterations
        self.parameters = parameters
        self.variables = variables
        self.agent_dcs = agent_dcs
        self.model_dcs = model_dcs

    def iter_variables(self):
        ''' return a list of tuples representing the scenarios to test '''
        if len(self.variables) == 1:
            return [ (v,) for v in list(self.variables.values())[0] ]
        else:
            return product(self.variables.values())

    def run_all(self):
        self.agent_df = pd.DataFrame(columns = [ var for var in self.variables] \
                + [ 'iteration', 'step', 'agent', 'run' ] + [ name for name in self.agent_dcs ])
        self.model_df = pd.DataFrame(columns = [ var for var in self.variables] \
                + [ 'iteration', 'step', 'run' ] + [ name for name in self.model_dcs ])

        run_num = 0
        for scenario in self.iter_variables():
            scenario = { var:val for var,val in list(zip(self.variables, scenario)) }
            for i in range(self.iterations):
                sim = self.run_scenario(scenario)

                df = sim._model.agent_df()
                df['iteration'] = i
                df['run'] = run_num
                for var in scenario:
                    df[var] = scenario[var]
                self.agent_df = pd.concat([self.agent_df, df], ignore_index=True)

                df = sim._model.model_df()
                df['iteration'] = i
                df['run'] = run_num
                for var in scenario:
                    df[var] = scenario[var]
                self.model_df = pd.concat([self.model_df, df], ignore_index=True)

                run_num += 1


    def run_scenario(self, scenario):
        sim = Simulation(
                model = self.model_cls(
                    **scenario,
                    **self.parameters, 
                    agent_dcs = self.agent_dcs,
                    model_dcs = self.model_dcs,
                    ),
                engine = BasicEngine(),
                steps = self.steps
                )
        sim.run()
        return sim
            


