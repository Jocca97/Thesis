import mesa
import numpy
from numpy import random

class MoralAgents(mesa.Agent):
    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.agent_type = agent_type  # This attribute differentiates agent types
        self.shared_attribute = None

    # Shared Behaviors

    def moral_worth_assignment(self):  # Change
        """

        This function is supposed to give moral worth to cooperators
        according to their contribution behaviors

        """
        if 1 <= self.calculate_invest() <= 5:
            self.moral_worth += 1
        elif 6 <= self.calculate_invest() <= 10:
            self.moral_worth += 2
        elif self.calculate_invest() >= 11:
            self.moral_worth += 3
        else:
            self.moral_worth -= 1

        return self.moral_worth

    def altruistic_punishment(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if self.calculate_contribution_amount() > other.calculate_contribution_amount():
                self.wealth -= cost_punish_agent
                other.wealth -= agent_punishment
            else:
                pass

    def antisocial_punishment(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if self.calculate_contribution_amount() < other.calculate_contribution_amount():
                self.wealth -= cost_punish_agent
                other.wealth -= agent_punishment
            else:
                pass

    def altruistic_punishment_frequency(self):
        ap_freq = 0
        if self.altruistic_punishment():
            ap_freq += 1

        if ap_freq == self.public_good_game.altruistic_punishment_freq:
            ap_freq = 0

        return ap_freq

    def antisocial_punishment_initiator(self):
        ap_freq = self.altruistic_punishment_frequency()

        if ap_freq == self.public_good_game.altruistic_punishment_freq:
            self.antisocial_punishment()
        elif ap_freq > self.public_good_game.altruistic_punishment_freq:
            pass
        else:
            pass

    def specific_behavior(self):
        if self.agent_type == "Cooperator":
            # Type 1 agent behavior
            pass
        elif self.agent_type == "Defector":
            # Type 2 agent behavior
            pass

    def calculate_probability_contributing(self):
        """

        A function that defines the probability of contribution according to what an agent's
        neighors do

        """
        #Pseucoded
        if self.agent_type == "Cooperator":
            if neighors < 4 and invest == True:
                self.probability_contributing = 0.6
            if neighors < 5 and invest == True:
                self.probability_contributing = 0.8
            if neighors < 6 and invest == True:
                self.probability_contributing = 0.9
            else:
                self.probability_contributing = 0.4

            return self.probability_contributing
        #Same idea with defectors but probability will be lower than the cooperator's
        elif self.agent_type == "Defector":
            if neighors < 4 and invest == True:
                self.probability_contributing = 0.3
            if neighors < 5 and invest == True:
                self.probability_contributing = 0.4
            if neighors < 6 and invest == True:
                self.probability_contributing = 0.5
            else:
                self.probability_contributing = 0.6

        def calculate_contribution_amount(self):
            """

            A function that defines the contribution amount according to?

            """

        def calculate_invest(self):
            """

            A method that defines the investment behaviors of agents

            """