import numpy as np


class GenerationsCreators:
    def __init__(self,first_generation='', rule='', generations=2):
        """

        :param first_generation:
        :param rule: Is a list of lists base on foramt Bxxx/Sxxx
        :param generations:
        """
        self.first_generation = first_generation
        self.rule = rule
        self.generations = generations

    def search_neighbors(self, x, y, generation):
        """
        x: columns
        y: row
        return: list of neighbors
        """
        next_e = (x,y+1) # E
        before_e = (x,y-1) # W
        up_left_e = (x-1,y-1) # NW
        up_right_e = (x-1,y+1) # NE
        up_e = (x-1,y) # N
        down_left_e = (x+1,y-1) # SW
        down_right_e = (x+1,y+1) # SE
        down_e = (x+1,y) # S
        neighbors_lst_values = []
        if self.rule[-2] == 'M':
            neighbors_lst = [next_e,before_e,up_left_e,up_right_e,up_e,down_left_e,down_right_e,down_e]
        elif self.rule[-2] == 'H':
            neighbors_lst = [up_e,up_left_e,before_e, next_e,down_e,down_right_e]
        elif self.rule[-2] == 'V':
            neighbors_lst = [up_e,down_e,before_e,next_e]
        for i in neighbors_lst:
            try:
                neighbors_lst_values.append(generation[i[0],i[-1]])
            except:
                pass
        return neighbors_lst_values

    def apply_rule(self,current_generation,list_of_neighbors):
        """
        We apply the Generation rules. So, we need to find all the alive cells,which are
        the 1. So, before sum we must filter all the 1.

        :param current_generation:
        :param list_of_neighbors:
        :return:
        """
        list_of_neighbors = list(filter(lambda x:x==1,list_of_neighbors))
        future_state = 0
        if current_generation == 0:
            if sum(list_of_neighbors) in self.rule[0]:
                future_state = 1
        elif current_generation == 1:
            if sum(list_of_neighbors) in self.rule[1]:
                future_state = 1
            elif self.rule[-1]> 2:
                future_state = (current_generation + 1) % self.rule[-1]
                # In case of multi states the cell envolve
        elif current_generation not in [0, 1]:
            # In case the cell is not dead(0) or alive(1)
            future_state = (current_generation + 1) % self.rule[-1]
        return  future_state

    def next_generation(self, current_generation):
        new_generation = np.zeros(current_generation.shape).astype(int)
        for k,i in enumerate(current_generation):
            for kk,j in enumerate(i):
                new_state_of_element = self.apply_rule(current_generation[k,kk], self.search_neighbors(k,kk,
                                                                                                       current_generation))
                new_generation[k,kk] = new_state_of_element
        return  new_generation

    def create_generations(self):
        """

        :return:
        """
        universe = [] # We load all the generations
        # First we load the first generation
        universe.append(self.first_generation)
        temp = self.first_generation
        for generation in range(self.generations):
            current_generation = self.next_generation(temp)
            temp = current_generation.astype(int)
            universe.append(temp)
        return  universe





