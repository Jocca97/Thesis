import mesa
import random
from numpy import random



# Punishment
cost_punish_agent = 1
agent_punishment = 3


class Defector(mesa.Agent):
    def __init__(self, unique_id, model, wealth=20):
        super().__init__(unique_id, model)
        self.public_good_game = model

        # Assign to self object
        self.wealth = wealth
        self.moral_worth = 0
        self.probability_contributing = self.calculate_probability_contributing()
        self.contribution_amount = self.calculate_contribution_amount()
        self.invest = self.calculate_invest()
        self.punishment_probabilities = [0.43, 0.77, 0.01, 0.15, 0.13]
        #data collector
        self.ap_freq = 0
        self.asp_freq = 0
        self.ap_money_spent = 0
        self.asp_money_spent = 0
        self.ap_money_lost = 0
        self.asp_money_lost = 0

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
        if -20 <= self.moral_worth <= -11:
            self.probability_contributing = 0.2
        elif -10 <= self.moral_worth <= -1:
            self.probability_contributing = 0.3
        elif self.moral_worth == 0:
            self.probability_contributing = 0.4
        elif 1 <= self.moral_worth <= 10:
            self.probability_contributing = 0.5
        elif 11 <= self.moral_worth <= 20:
            self.probability_contributing = 0.6

        return self.probability_contributing

    def calculate_contribution_amount(self):
        """

        A function that defines the probability of the amount of a contribution according to the agent's moral wort

        """
        self.contribution_amount = 0
        if -20 <= self.moral_worth <= -11:
            self.contribution_amount = 17.7
        elif -10 <= self.moral_worth <= -1:
            self.contribution_amount = 17.7
        elif self.moral_worth == 0:
            self.contribution_amount = 17.7 # Copenhagen
        elif 1 <= self.moral_worth <= 10:
            self.contribution_amount = 17.7
        elif 11 <= self.moral_worth <= 20:
            self.contribution_amount = 17.7

        return self.contribution_amount

    def calculate_invest(self):
        """

        A function that defines the investment behaviors of defector

        """
        fixed_loss = 2
        if self.calculate_probability_contributing() >= random.random():
            invest = self.calculate_contribution_amount()
        else:
            invest = fixed_loss

        return invest

    def moral_worth_assignment(self):  # Change
        """

        This function is supposed to give moral worth to defectors
        according to their contribution behaviors

        """
        if 3 <= self.calculate_invest() <= 10:
            self.moral_worth += 1
        elif 11 <= self.calculate_invest() <= 20:
            self.moral_worth += 2
        elif self.calculate_invest() <= 2:  # fixed_loss = 2
            self.moral_worth -= 1

        return self.moral_worth


    def punishment_behaviors(self):
        cost_punish_agent = 1
        agent_punishment = 3
        for agent in self.model.schedule.agents:
            neighbors = self.model.grid.get_neighbors(agent.pos, moore=True)
            if len(neighbors) > 0:
                other = self.random.choice(neighbors)
                if self.calculate_invest() > other.calculate_invest():
                    if random.random() <= self.punishment_probabilities[0]:
                        if 1 <= self.calculate_invest() - other.calculate_invest() <= 10:
                            agent.wealth -= cost_punish_agent
                            other.wealth -= agent_punishment
                            self.ap_freq += 1
                            self.ap_money_spent += 1
                            self.ap_money_lost += 3
                    elif random.random() <= self.punishment_probabilities[1]:
                        if 11 <= self.calculate_invest() - other.calculate_invest() <= 20:
                            agent.wealth -= cost_punish_agent
                            other.wealth -= agent_punishment
                            self.ap_freq += 1
                            self.ap_money_spent += 1
                            self.ap_money_lost += 3
                # Antisocial Punishment
                if self.calculate_invest() < other.calculate_invest():
                    if random.random() <= self.punishment_probabilities[2]:
                        if 1 <= other.calculate_invest() - self.calculate_invest() <= 10:
                            agent.wealth -= cost_punish_agent
                            other.wealth -= agent_punishment
                            self.asp_freq += 1
                            self.asp_money_spent += 1
                            self.asp_money_lost += 3

                elif self.calculate_invest() > other.calculate_invest():
                    if random.random() <= self.punishment_probabilities[3]:
                        if 11 <= other.calculate_invest() - self.calculate_invest() <= 20:
                            agent.wealth -= cost_punish_agent
                            other.wealth -= agent_punishment
                            self.asp_freq += 1
                            self.asp_money_spent += 1
                            self.asp_money_lost += 3
            else:
                pass
    def agent_transform(self):
        """

        A method that mutates agents according to their investment behaviors

        """
        from cooperator import Cooperator
        for agent in self.model.schedule.agents:
            if self.calculate_invest() > 2:
                wealth = agent.wealth
                id = agent.unique_id
                new_agent = Cooperator(id, self.model, wealth)
                # Add the new agent to grid and remove old one
                x = self.random.randrange(self.model.grid.width)
                y = self.random.randrange(self.model.grid.height)
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                self.model.grid.place_agent(new_agent, (x, y))
                self.model.schedule.add(new_agent)

    def step(self):
        self.move()
        if self.wealth > 0:
            self.calculate_probability_contributing()
            self.calculate_contribution_amount()
            self.calculate_invest()
            self.agent_transform()
            self.punishment_behaviors()
            self.moral_worth_assignment()
        else:
            pass

