from pyabm import *

class MoneyAgent(Agent):
    def init(self, wealth=1):
        self.wealth = wealth
        
class MoneyModel(Model):
    def context(self):
        return {}
    
agents = [ MoneyAgent(i) for i in range(10) ]


def get_money(agent):
    return agent.wealth


sim = Simulation(model = MoneyModel(agents, agent_data = {'wealth':get_money}),)
sim.run()
