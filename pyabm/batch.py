
from itertools import product
from typing import *

from .model import Model
from .engine import BasicEngine

class Batch:
    def __init__(self, 
            model:Model,
            max_steps: int = 100,
            iterations:int = 1,
            parameters:Dict[str,Any] = { },
            variables:Dict[str, List[Any]] = { },
            agent_data:Dict[str,Callable] = { },
            model_data:Dict[str, Callable] = { }
            ):

        self.model = model
        self.max_steps = max_steps
        self.iterations = iterations
        self.parameters = parameters
        self.variables = variables
        self.agent_data = agent_data
        self.model_data = model_data

    def iter_variables(self):
        return product(self.variables.values())

    def run_all(self):
        for scenario in self.iter_variables():
            self.run_scenario(scenario)

    def run_scenario(self, scenario):
        for i in range(self.iterations):
        sim = Simulation(
                model = self.model,
                engine = BasicEngine(),
                # TODO: finish this





