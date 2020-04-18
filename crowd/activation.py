
from abc import ABC, abstractmethod
import numpy as np
import random
from typing import *
from .agent import Agent

def random_activation(agents: List[Agent]):
    for agent in random.shuffle(agents):
        yield(agent)

def basic_activation(agents: List[Agent], key:Callable = None):
    if key:
        agents = sorted(agents, key = key)
    for agent in agents:
        yield agent

