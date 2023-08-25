import mesa
from numpy import random

# Parameters
# Payoffs
fixed_loss = 2
# Punishment
cost_punish_agent = 1
agent_punishment = 3

class Cooperator(mesa.Agent):
    """

    An agent with high probability of contributing to the common pool
    and able to engage in both ASP and AP

    """

    def __init__(self, unique_id, model, wealth=20):
        super().__init__(unique_id, model)
        self.public_good_game = model

        # Assign to self object
        self.wealth = wealth
        self.moral_worth = 0
        self.probability_contributing = self.calculate_probability_contributing()
        self.contribution_amount = self.calculate_contribution_amount()
        self.invest = self.calculate_invest()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def calculate_probability_contributing(self):
        """

        A function that defines the probability of contribution according to the agent's moral worth

        """
    def calculate_contribution_amount(self):
        """

        A function that defines the contribution amount according to the agent's moral worth

        """

    def calculate_invest(self):
        """

        A method that defines the investment behaviors of agents

        """

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

    def step(self):
        self.move()
        if self.wealth > 0: