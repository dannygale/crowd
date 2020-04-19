
from itertools import product
from typing import *

from .model import Model
from .engine import BasicEngine
from .activation import *

class Batch:
    def __init__(self, 
            model_cls:Class, 
            engine:Engine = None
            max_steps: int = 100,
            iterations:int = 1,
            parameters:Dict[str,Any] = { },
            variables:Dict[str, List[Any]] = { },
            agent_dcs:Dict[str,Callable] = { },
            model_dcs:Dict[str, Callable] = { }
            ):

        self.model_cls = model_cls
        self.engine = engine if engine else BasicEngine()
        self.max_steps = max_steps
        self.iterations = iterations
        self.parameters = parameters
        self.variables = variables
        self.agent_dcs = agent_dcs
        self.model_dcs = model_dcs

    def iter_variables(self):
        return product(self.variables.values())

    def run_all(self):
        self.agent_df = pd.DataFrame(columns = [ var for var in variables] \
                + [ 'iteration', 'step', 'agent' ] + [ name for name in self.agent_dcs ]])
        self.model_df = pd.DataFrame(columns = [ var for var in variables] \
                + [ 'iteration', 'step' ] + [ name for name in self.model_dcs ]])

        for scenario in self.iter_variables():
            self.run_scenario(scenario)


    def run_scenario(self, scenario):
        for i in range(self.iterations):
            sim = Simulation(
                    model = self.model_cls(**self.parameters, **scenario),
                    engine = BasicEngine(),
                    steps = self.max_steps
                    )
            sim.run()
            
            df = sim._model.agent_data()
            df['iteration'] = i
            for var in scenario:
                df[var] = scenario[var]
            self.agent_df = self.agent_df.concat(df, ignore_index=True)

            df = sim._model.model_data()
            df['iteration'] = i
            for var in scenario:
                df[var] = scenario[var]
            self.model_df = self.model_df.concat(df, ignore_index=True)


