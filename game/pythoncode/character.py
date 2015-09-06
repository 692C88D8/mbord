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
        res = self.resources.quantities
        for i in xrange(0, len(res)):
            if res[i] > 0:
                payment = res[i] / 10
                if payment < 1:
                    payment = 1
                res[i] -= payment

    def on_new_turn(self, job):
        # сброс непотраченных очков действия
        if self.action_points > 0:
            self.action_points = 0
        # потребление еды
        food = self.resources.get_food()
        ration = self.ration
        if food >= ration:
            self.resources.add_food(-self.ration)
            self.starving = 0
        else:
            self.resources.set_food(0)
            self.starving += (ration - food)
        # сброс ресурсов или плата за их хранение
        if self.__storage == Character.STORAGE_NONE:
            self.resources.reset_all_to_zero()
        elif self.__storage == Character.STORAGE_RENT:
            self.pay_storage_rent()
        # получение оплаты за работу
        job.do_job(self)
        # TODO за работу могли получить еду. Стоит ли её сразу тут использовать для погашения starving?
        # добавление очков действия
        self.restore_action_points()