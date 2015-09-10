# coding=utf-8

import resources


class Character:
    _AP_DEF = 2
    _RATION_DEF = 1

    STORAGE_NONE = 0
    STORAGE_RENT = 1
    STORAGE_FREE = 2

    def __init__(self):
        self.name = "Anon"

        self.physique = 3
        self.agility = 3
        self.spirit = 3
        self.mind = 3

        self.action_points = Character._AP_DEF
        self.ration = Character._RATION_DEF
        # чем больше starving тем голоднее
        self.starving = 0;

        self.resources = resources.Resources()

        self.__storage = Character.STORAGE_NONE

        # Хоть кампинг в стартовой локации запрещен, но будем считать что изначально он в нём.
        self.camp_location_index = 0

        self.job_location_index = None # номер локации с работой
        self.job_num = None # номер работы на локации

    def set_storage(self, storage_type):
        self.__storage = storage_type

    def get_storage(self):
        return self.__storage

    def get_storage_name(self):
        names = ['None', 'Rent', 'Free']
        return names[self.__storage]

    def restore_action_points(self):
        self.action_points += Character._AP_DEF

    def pay_storage_rent(self):
        res = self.resources.to_list()
        for i in xrange(0, len(res)):
            if res[i] > 0:
                payment = int(res[i] / 10)
                if payment < 1:
                    payment = 1
                res[i] -= payment
        self.resources.from_list(res)

    def on_new_turn(self, game):
        job = game.get_character_job(self)
        # сброс непотраченных очков действия
        if self.action_points > 0:
            self.action_points = 0
        # потребление еды
        food = self.resources.food
        ration = self.ration
        if food >= ration:
            self.resources.food -= self.ration
            self.starving = 0
        else:
            self.resources.food = 0
            self.starving += (ration - food)
        # сброс ресурсов или плата за их хранение
        if self.__storage == Character.STORAGE_NONE:
            self.resources.reset_all_to_zero()
        elif self.__storage == Character.STORAGE_RENT:
            self.pay_storage_rent()
        # получение оплаты за работу, если локация с ней доступна
        if self.get_current_job_state(game.locations_model) == Character.JOB_AVAILABLE:
            job.do_job(self)
        # TODO за работу могли получить еду. Стоит ли её сразу тут использовать для погашения starving?
        # добавление очков действия
        self.restore_action_points()

    JOB_NONE = 0
    JOB_NOT_AVAILABLE = 1
    JOB_AVAILABLE = 2

    def get_current_job_state(self, locations_model):
        if self.job_location_index is None:
            return Character.JOB_NONE
        if locations_model.is_location_in_reach(self, self.job_location_index):
            return Character.JOB_AVAILABLE
        return Character.JOB_NOT_AVAILABLE