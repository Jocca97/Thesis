import mesa
import numpy as np

from numpy import random

from agents import MoralAgents

# Punishment
cost_punish_agent = 1
agent_punishment = 3


class PublicGoodGame(mesa.Model):
    def __init__(self, num_agents, altruistic_punishment_freq, width=10,
                 height=10):
        super().__init__(num_agents, altruistic_punishment_freq, width,
                         height)

        self.common_pool = 0
        self.multiplier = 1.6
        self.investment = 0
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # self.running = True
        self.datacollector = mesa.DataCollector(
            model_reporters={"Cooperator Count": count_agent_cooperator,
                             "Defector Count": count_agent_defector,
                             "Cooperator Average Wealth": cooperator_average_wealth,
                             "Defector Average Wealth": defector_average_wealth,
                             "Population Average Wealth": population_average_wealth,
                             "Cooperator Average Moral Worth:": cooperator_average_moral_worth,
                             "Defector Average Moral Worth:": defector_average_moral_worth,
                             "Population Average Moral Worth": population_average_moral_worth,
                             # "Altruistic Punishment": altruistic_punishment_frequency,
                             # "Antisocial Punishment": antisocial_punishment_frequency,
                             "AP Money Spent": money_spent_altruistic_punishment,
                             "AP Money Lost": money_lost_altruistic_punishment,
                             "ASP Money Spent": money_spent_antisocial_punishment,
                             "ASP Money Lost": money_lost_antisocial_punishment,
                             "Common Pool Wealth": common_pool_wealth,
                             },
        )

        # Create agents
        for i in range(int(num_cooperators)):
            # Create Cooperator
            moral_worth_initial_values = np.random.normal(5, 3.5, num_cooperators)
            a = Cooperator(self.next_id(), self)
            a.moral_worth = moral_worth_initial_values[i]

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)
            self.datacollector.collect(self)

        # Create Defector
        for i in range(int(self.num_defectors)):
            moral_worth_initial_values = np.random.normal(5, 3.5, self.num_defectors)
            b = Defector(self.next_id(), self)
            b.moral_worth = moral_worth_initial_values[i]

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))
            self.schedule.add(b)
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


class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, width=10, height=10, density=0.8, minority_pc=0.2):
        """ """

        self.width = width
        self.height = height
        self.density = density
        self.minority_pc = minority_pc
        self.common_pool = 0
        self.multiplier = 1.6
        self.investment = 0

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        # Set up agents
        for cell in self.grid.coord_iter():
            x, y = cell[1]
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < self.minority_pc else 0

                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        # self.running = True
        # self.datacollector = mesa.DataCollector(
        #     model_reporters={"Cooperator Count": count_agent_cooperator,
        #                      "Defector Count": count_agent_defector,
        #                      "Cooperator Average Wealth": cooperator_average_wealth,
        #                      "Defector Average Wealth": defector_average_wealth,
        #                      "Population Average Wealth": population_average_wealth,
        #                      "Cooperator Average Moral Worth:": cooperator_average_moral_worth,
        #                      "Defector Average Moral Worth:": defector_average_moral_worth,
        #                      "Population Average Moral Worth": population_average_moral_worth,
        #                      # "Altruistic Punishment": altruistic_punishment_frequency,
        #                      # "Antisocial Punishment": antisocial_punishment_frequency,
        #                      "AP Money Spent": money_spent_altruistic_punishment,
        #                      "AP Money Lost": money_lost_altruistic_punishment,
        #                      "ASP Money Spent": money_spent_antisocial_punishment,
        #                      "ASP Money Lost": money_lost_antisocial_punishment,
        #                      "Common Pool Wealth": common_pool_wealth,
        #                      },
        # )