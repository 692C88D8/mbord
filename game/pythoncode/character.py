# coding=utf-8

import resources


class Character:
    def __init__(self):
        self.name = "Anon"

        self.physique = 3
        self.agility = 3
        self.spirit = 3
        self.mind = 3

        self.action_points = 2

        self.resources = resources.Resources()

        # Хоть кампинг в стартовой локации запрещен, но будем считать что изначально он в нём.
        self.camp_location_index = 0

        self.job_location_index = None # номер локации с работой
        self.job_num = None # номер работы на локации