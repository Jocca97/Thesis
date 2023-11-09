import mesa
import numpy as np
from mesa import agent

from numpy import random

from cooperator import Cooperator
from defector import Defector


class PublicGoodGame(mesa.Model):
    def __init__(self, num_cooperators, defector_ratio, width=10,
                 height=10):
        super().__init__(num_cooperators, defector_ratio, width,
                         height)
        self.num_cooperators = num_cooperators
        self.num_defectors = round(self.num_cooperators * defector_ratio)
        self.defector_ratio = defector_ratio
        self.common_pool = 0
        self.multiplier = 1.6
        self.investment = 0
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.datacollector = mesa.DataCollector(
            agent_reporters={"Wealth": "wealth"},
            model_reporters={"Cooperator Count": count_agent_cooperator,
                             "Defector Count": count_agent_defector,
                             "Cooperator Average Wealth": cooperator_average_wealth,
                             "Defector Average Wealth": defector_average_wealth,
                             "Population Average Wealth": population_average_wealth,
                             "Cooperator Average Moral Worth:": cooperator_average_moral_worth,
                             "Defector Average Moral Worth:": defector_average_moral_worth,
                             "Population Average Moral Worth": population_average_moral_worth,
                             "Altruistic Punishment": ap_frequency,
                             "Antisocial Punishment": asp_frequency,
                             "AP Money Spent": money_spent_ap,
                             "AP Money Lost": money_lost_ap,
                             "ASP Money Spent": money_spent_asp,
                             "ASP Money Lost": money_lost_asp,
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

    def set_investment(self):
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

    def common_pool_wealth(self):
        self.common_pool += self.investment

        return self.common_pool

    def calculate_payoff(self):
        """

        This method calculates the payoff of each agent

        """
        self.payoff = (self.investment * self.multiplier) / (self.num_cooperators + self.num_defectors)

        return self.payoff

    def step(self):
        self.schedule.step()
        self.set_investment()
        for agent in self.schedule.agents:
            if isinstance(agent, Cooperator or Defector):
                agent.wealth += self.calculate_payoff()
        self.datacollector.collect(self)
        if self.common_pool_wealth() == 0:
            self.running = False



# Agent Count

def count_agent_cooperator(model):
    amount_cooperator = sum(1 for agent in model.schedule.agents if isinstance(agent, Cooperator))

    return amount_cooperator


def count_agent_defector(model):
    amount_defector = sum(1 for agent in model.schedule.agents if isinstance(agent, Defector))

    return amount_defector


# Wealth

def common_pool_wealth(model):
    cp_wealth = 0
    cp_wealth += model.common_pool

    return cp_wealth

def cooperator_average_wealth(model):
    cooperators_wealth = [agent.wealth for agent in model.schedule.agents if isinstance(agent, Cooperator)]
    if len(cooperators_wealth) > 0:
        n = sum(cooperators_wealth) / len(cooperators_wealth)
    else:
        n = 0
    return n


def defector_average_wealth(model):
    defectors_wealth = [agent.wealth for agent in model.schedule.agents if isinstance(agent, Defector)]
    return sum(defectors_wealth) / len(defectors_wealth) if len(defectors_wealth) > 0 else 0


def population_average_wealth(model):
    cooperator_avg_wealth = cooperator_average_wealth(model)
    defector_avg_wealth = defector_average_wealth(model)
    pop_avg_wealth = (cooperator_avg_wealth + defector_avg_wealth) / 2

    return pop_avg_wealth


# Moral Worth

def cooperator_average_moral_worth(model):
    cooperator_moral_worth_report = [agent.moral_worth for agent in model.schedule.agents if
                                     isinstance(agent, Cooperator)]
    if len(cooperator_moral_worth_report) > 0:
        cooperator_avg_moral_worth = sum(cooperator_moral_worth_report) / len(cooperator_moral_worth_report)
    else:
        cooperator_avg_moral_worth = 0

    return cooperator_avg_moral_worth


def defector_average_moral_worth(model):
    defector_moral_worth_report = [agent.moral_worth for agent in model.schedule.agents if
                                   isinstance(agent, Defector)]
    if len(defector_moral_worth_report) > 0:
        defector_avg_moral_worth = sum(defector_moral_worth_report) / len(defector_moral_worth_report)
    else:
        defector_avg_moral_worth = 0

    return defector_avg_moral_worth


def population_average_moral_worth(model):
    cooperator_avg_moral_worth = cooperator_average_moral_worth(model)
    defector_avg_moral_worth = defector_average_moral_worth(model)
    pop_avg_moral_worth = (cooperator_avg_moral_worth + defector_avg_moral_worth) / 2

    return pop_avg_moral_worth


#Frequency of each punishment type

def ap_frequency(model):
    for agent in model.schedule.agents:
        print(agent.ap_freq)
        return agent.ap_freq


def asp_frequency(model):
    for agent in model.schedule.agents:
        print(agent.asp_freq)
        return agent.asp_freq

# Money spent and lost within each punishment type

def money_spent_ap(model):
    money_spent_ap = 0
    for agent in model.schedule.agents:
        money_spent_ap += agent.ap_money_spent

    return money_spent_ap

def money_lost_ap(model):
    money_lost_ap = 0
    for agent in model.schedule.agents:
        money_lost_ap += agent.ap_money_lost

    return money_lost_ap

def money_spent_asp(model):
    money_spent_asp = 0
    for agent in model.schedule.agents:
        money_spent_asp += agent.asp_money_spent

    return money_spent_asp

def money_lost_asp(model):
    money_lost_asp = 0
    for agent in model.schedule.agents:
        money_lost_asp += agent.asp_money_lost

    return money_lost_asp








