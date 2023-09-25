import mesa
import numpy as np

from numpy import random

from agents import MoralAgents

# Punishment
cost_punish_agent = 1
agent_punishment = 3


class PublicGoodGame(mesa.Model):
    def __init__(self, num_cooperators, num_defectors , altruistic_punishment_freq, width=10,
                 height=10):
        super().__init__(num_cooperators, num_defectors, altruistic_punishment_freq, width,
                         height)

        self.num_cooperators = num_cooperators
        self.num_defectors = num_defectors
        self.common_pool = 0
        self.multiplier = 1.6
        self.investment = 0
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={"Cooperator Count": count_agent_cooperator,
                             "Defector Count": count_agent_defector,
                             # "Cooperator Average Wealth": cooperator_average_wealth,
                             # "Defector Average Wealth": defector_average_wealth,
                             # "Population Average Wealth": population_average_wealth,
                             # "Cooperator Average Moral Worth:": cooperator_average_moral_worth,
                             # "Defector Average Moral Worth:": defector_average_moral_worth,
                             # "Population Average Moral Worth": population_average_moral_worth,
                             # # "Altruistic Punishment": altruistic_punishment_frequency,
                             # # "Antisocial Punishment": antisocial_punishment_frequency,
                             # "AP Money Spent": money_spent_altruistic_punishment,
                             # "AP Money Lost": money_lost_altruistic_punishment,
                             # "ASP Money Spent": money_spent_antisocial_punishment,
                             # "ASP Money Lost": money_lost_antisocial_punishment,
                             # "Common Pool Wealth": common_pool_wealth,
                             },
        )

        # Create agents

        for i in range(self.num_cooperators):
            cooperator = MoralAgents(unique_id=i, model=self, agent_type="Cooperator")
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.schedule.add(cooperator)
            self.grid.place_agent(cooperator, (x, y))
            self.datacollector.collect(self)

        for i in range(self.num_defectors):
            defector = MoralAgents(unique_id=i + self.num_cooperators, model=self, agent_type="Defector")
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.schedule.add(defector)
            self.grid.place_agent(defector, (x, y))
            self.datacollector.collect(self)


    def set_investment(self, investment):
        """

        This method calculates the investment amount of each agent belonging to the
        Cooperator and Defector classes and sums it all up.

        """
        cooperator_investment = 0
        defector_investment = 0
        # Calculate investment for each Cooperator instance
        for agent in self.schedule.agents:
            if isinstance(agent, Cooperator):
                cooperator_investment += agent.calculate_invest()

        # Calculate investment for each Defector instance
        for agent in self.schedule.agents:
            if isinstance(agent, Defector):
                defector_investment += agent.calculate_invest()

        investment = cooperator_investment + defector_investment
        self.investment += investment
        self.common_pool += investment

    def calculate_payoff(self):
        """

        This method calculates the payoff of each agent

        """
        print(self.investment)
        print(self.common_pool)
        self.payoff = (self.investment * self.multiplier) / (self.num_cooperators + self.num_defectors)

        return self.payoff

    # def common_pool_wealth(self):
    #     self.common_pool += self.calculate_payoff()
    #
    #     return self.common_pool

    def agent_transform(self):
        """

        A method that mutates agents according to their investment behaviors

        """
        for agent in self.schedule.agents:
            if isinstance(agent, Defector) and agent.calculate_invest() > 2:  # fixed loss amount
                wealth = agent.wealth
                id = agent.unique_id
                new_agent = Cooperator(id, self, wealth)
                # Add the new agent to grid and remove old one
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
                self.grid.place_agent(new_agent, (x, y))
                self.schedule.add(new_agent)
            elif isinstance(agent, Cooperator) and agent.calculate_invest() == 2:  # fixed loss amount
                wealth = agent.wealth
                id = agent.unique_id
                new_agent = Defector(id, self, wealth)
                # Add the new agent to grid and remove old one
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
                self.grid.place_agent(new_agent, (x, y))
                self.schedule.add(new_agent)

    def step(self):
        self.investment = 0
        self.schedule.step()
        self.agent_transform()
        self.set_investment(self.investment)
        self.calculate_payoff()
        self.datacollector.collect(self)

        # if self.num_cooperators == 0:
        #     self.running = False


def count_agent_cooperator(model):
    amount_cooperator = sum(1 for agent in model.schedule.agents if agent.agent_type == "cooperator")

    return amount_cooperator

def count_agent_defector(model):
    amount_defector = sum(1 for agent in model.schedule.agents if agent.agent_type == "defector")

    return amount_defector