# coding=utf-8

import random


class _JobBaseClass(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def do_job(self, character):
        raise Exception('do_job not implemented for: %s' % self.name)


# Работа ничегонеделания. Типа паттерн NULL Object или как-то так зовут
# Хотя возможно при отсутствии работы всё таки стоит возвращать None
# TODO подумать когда придет время
class JobIdle(_JobBaseClass):
    def __init__(self):
        super(JobIdle, self).__init__("Idle", "TODO")

    def do_job(self, character):
        return None


class JobFoodThief(_JobBaseClass):
    def __init__(self):
        super(JobFoodThief, self).__init__("Stealing food", "TODO")

    def do_job(self, character):
        if 0 == random.randint(0, 1):
            character.resources.food += (character.mind + character.agility)


class JobFoodBeggar(_JobBaseClass):
    def __init__(self):
        super(JobFoodBeggar, self).__init__("Begg for food", "TODO")

    def do_job(self, character):
        character.resources.food += character.spirit


class JobFoodWhore(_JobBaseClass):
    def __init__(self):
        super(JobFoodWhore, self).__init__("Sex for food", "TODO")

    def do_job(self, character):
        character.resources.food += character.agility


class JobScavenger(_JobBaseClass):
    def __init__(self):
        super(JobScavenger, self).__init__("Scavenging", "TODO")

    def do_job(self, character):
        val = character.agility + character.mind
        # Тут мне очень не хватает обычного switch case. Извраты со словарем имен параметров мне кажется слишком извратным
        # Сделаю тупо на if хорошо их не очень много
        rnd = random.randint(0, 4)
        if 0 == rnd:
            character.resources.fuel += val
        elif 1 == rnd:
            character.resources.drugs += val
        elif 2 == rnd:
            character.resources.arms += val
        elif 3 == rnd:
            character.resources.tools += val
        else:
            character.resources.material += val


class JobFuelExtractor(_JobBaseClass):
    def __init__(self):
        super(JobFuelExtractor, self).__init__("Fuel extraction", "TODO")

    def do_job(self, character):
        character.resources.fuel += (character.agility + character.physique)


class JobWoodGathering(_JobBaseClass):
    def __init__(self):
        super(JobWoodGathering, self).__init__("Wood gathering", "TODO")

    def do_job(self, character):
        character.resources.fuel += (character.agility + character.physique)


class JobHerbalism(_JobBaseClass):
    def __init__(self):
        super(JobHerbalism, self).__init__("Herbalism", "TODO")

    def do_job(self, character):
        character.resources.drugs += (character.agility + character.mind)


class JobMarauder(_JobBaseClass):
    def __init__(self):
        super(JobMarauder, self).__init__("Marauding", "TODO")

    def do_job(self, character):
        character.resources.material += (character.agility + character.physique)


class JobToolScavenger(_JobBaseClass):
    def __init__(self):
        super(JobToolScavenger, self).__init__("Scavenging tools", "TODO")

    def do_job(self, character):
        character.resources.tools += (character.agility + character.physique)


class JobDemolisher(_JobBaseClass):
    def __init__(self):
        super(JobDemolisher, self).__init__("Demolishing", "TODO")

    def do_job(self, character):
        character.resources.material += (character.agility + character.physique)


class JobWeaponLooter(_JobBaseClass):
    def __init__(self):
        super(JobWeaponLooter, self).__init__("Looting", "TODO")

    def do_job(self, character):
        character.resources.arms += (character.agility + character.physique)