
from .model import Model
from .engine import Engine, BasicEngine
from .activation import *

class Simulation:
    """A self-contained simulation"""

    def __init__(self, 
            model: Model,
            engine: Engine = None,
            steps: int = 10
            ):

        self._model = model 
        self._engine = engine if engine else BasicEngine()
        self._steps = steps

    def run(self, steps = None):
        self._model.init_data()
        self._engine.run(self._model, steps if steps else self._steps)

    def agent_data(self):
        return self._model.agent_data()
    def model_data(self):
        return self._model.model_data()

