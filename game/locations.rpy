﻿# coding=utf-8

init -1 python:

    import random

    from pythoncode.jobs import *
    from pythoncode.character import Character as MB_Character # Character уже есть в RenPy
    
    class _LocationBaseClass(object):
        def __init__(self, name, description, can_have_camp):
            self._name = name
            self._description = description
            # TODO возможно списку исследованных локаций стоит переехать в персонажа
            self.explored = False  # Для неисследованных недоступны имена, описание и действия(кроме исследования)
            self.can_have_camp = can_have_camp
            self.jobs = []

        def get_specific_actions(self, character):
            return []
            
        @property
        def name(self):
            if self.explored:
                return self._name
            return "???"

        @property
        def description(self):
            if self.explored:
                return self._description
            return "Unknown location"


    class LocationThinMist(_LocationBaseClass):
        def __init__(self):
            super(LocationThinMist, self).__init__("Thin mist", "Starting location", False)


    class LocationSlums(_LocationBaseClass):
        def __init__(self):
            super(LocationSlums, self).__init__("Slums", "Here you can steal food", True)
            self.jobs = [JobFoodThief()]

    class LocationMarket(_LocationBaseClass):
        def __init__(self):
            super(LocationMarket, self).__init__("Market", "Here you can buy food", True)

        def get_specific_actions(self, character):
            if character.resources.summary_except_food() < 2:
                return []
            return [LocationActionBuyFood()]
            

    class LocationDepository(_LocationBaseClass):
        def __init__(self):
            super(LocationDepository, self).__init__("Depository", "Here you can rent storage", True)

        def get_specific_actions(self, character):
            storage_type = character.get_storage()
            if storage_type == MB_Character.STORAGE_NONE:
                return [LocationActionRentStorage()]
            if storage_type == MB_Character.STORAGE_RENT:
                return [LocationActionNoMoreRentStorage()]
            return []

    class LocationCharityMission(_LocationBaseClass):
        def __init__(self):
            super(LocationCharityMission, self).__init__("Charity Mission", "Here you can begg for food", True)
            self.jobs = [JobFoodBeggar()]

            
    class LocationOutpost(_LocationBaseClass):
        def __init__(self):
            super(LocationOutpost, self).__init__("Outpost", "You can be a whore here", True)
            self.jobs = [JobFoodWhore()]


    class LocationSlaverEncampment(_LocationBaseClass):
        def __init__(self):
            super(LocationSlaverEncampment, self).__init__("Slaver Encampment", "Nothing to do here for now", True)


    class LocationRuinedFortifications(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedFortifications, self).__init__("Ruined Fortifications", "Nothing to do here for now", True)


    class LocationJunkyard(_LocationBaseClass):
        def __init__(self):
            super(LocationJunkyard, self).__init__("Junk yard", "You can scavange some resources here", True)
            self.jobs = [JobScavenger()]

            
    class LocationMine(_LocationBaseClass):
        def __init__(self):
            super(LocationMine, self).__init__("Mine", "You can extract fuel here", True)
            self.jobs = [JobFuelExtractor()]

            
    class LocationDyingGrove(_LocationBaseClass):
        def __init__(self):
            super(LocationDyingGrove, self).__init__("Dying grove", "You can gather wood or herbs here", True)
            self.jobs = [JobWoodGathering(), JobHerbalism()]
            

    class LocationRuinedHouses(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedHouses, self).__init__("Ruined houses", "You can get some materials here", True)
            self.jobs = [JobMarauder()]


    class LocationRuinedFactory(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedFactory, self).__init__("Ruined factory", "You can scavange some tools here", True)
            self.jobs = [JobToolScavenger()]


    class LocationGrimBattlefield(_LocationBaseClass):
        def __init__(self):
            super(LocationGrimBattlefield, self).__init__("Grim battlefield", "You can loot some weapons here", True)
            self.jobs = [JobWeaponLooter()]


    class LocationsModel:
        def __init__(self):
            # стартовая локация
            mist = LocationThinMist()
            mist.explored = True
            mist.can_have_camp = False
            # доступные локации. Сюда они постепенно переезжают из __closed_locations
            # при вызове _add_random_closed_location()
            # TODO Ващет правильно было бы чтобы игрок знал какие локации для него открыты(__closed_locations убираем, а в персонажа добавляем словарь из индексов и состояния(0 открыто, 1 исследовано))
            # Или проще одна целочисленная переменная - число исследованных локаций. Неоткрытых всё равно не больше 1.
            # Но отложим это до того когда будет больше одного персонажа 
            self.locations = [mist]
            self.__closed_locations = [
                LocationSlums(),
                LocationMarket(),
                LocationDepository(),
                LocationCharityMission(),
                LocationOutpost(),
                LocationSlaverEncampment(),
                LocationRuinedFortifications(),
                LocationJunkyard(),
                LocationMine(),
                LocationDyingGrove(),
                LocationRuinedHouses(),
                LocationRuinedFactory(),
                LocationGrimBattlefield(),
            ]
            # Добавим рандомную первую локацию, куда можно перейти из тумана
            self.add_random_closed_location()
            self.selected_location_index = 0 # Номер локации выбранной в интерфейсе

        def set_selected_location_index(self, location_index):
            self.selected_location_index = location_index
            
        def get_location_actions(self, character, location_index):
            loc = self.locations[location_index]
            if not loc.explored:
                return [LocationActionExplore()]
            
            result = loc.get_specific_actions(character)
            if (character.camp_location_index != location_index) and loc.can_have_camp:
                result.append(LocationActionMoveCamp())
            for job_num in xrange(0, len(loc.jobs)):
                if (character.job_location_index != location_index) or (character.job_num != job_num):
                    job = loc.jobs[job_num]
                    result.append(LocationActionChangeJob(job.name, job.description, job, job_num))
            return result

        def add_random_closed_location(self):
            if not self.__closed_locations:
                return False # Если закрытых не осталось, то просто ничего не делаем
            last_index = len(self.__closed_locations) - 1
            random_index = random.randint(0, last_index)  # Return a random integer N a <= N <= b
            self.locations.append(self.__closed_locations[random_index])
            if random_index < last_index:
                self.__closed_locations[random_index] = self.__closed_locations[last_index]
            del self.__closed_locations[last_index]
            return True
            
        def is_location_in_reach(self, character, location_index):
            in_reach_num = character.agility + character.spirit
            location_num = len(self.locations)
            camp_index = character.camp_location_index
                
            reachable_back = int(in_reach_num / 2) # сколько локаций доступно до лагеря
            if reachable_back > camp_index:
                reachable_back = camp_index
            reachable_fwd = in_reach_num - reachable_back # сколько локаций доступно с учетом лагеря и после него
            # Если лагерь близко к концу списка то добавим локаций из начала.
            past_last_available_index = camp_index + reachable_fwd
            diff = past_last_available_index - location_num
            if diff > 0:
                reachable_back += diff
            # Из-за того что reachable_fwd с учетом лагеря, то получается <, а не <=
            return camp_index - reachable_back <= location_index < camp_index + reachable_fwd
