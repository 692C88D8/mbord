# coding=utf-8

init -1 python:

    import random

    from pythoncode.jobs import *
    
    class _LocationBaseClass(object):
        def __init__(self, name, description, can_have_camp):
            self._name = name
            self._description = description
            self.explored = False  # Для неисследованных недоступны имена, описание и действия(кроме исследования)
            self.can_have_camp = can_have_camp
            self.jobs = []

        @property
        def name(self):
            if self.explored:
                return self._name
            return "???"

        @property
        def description(self):
            if self.explored:
                return self._description
            return "???"


    class LocationThinMist(_LocationBaseClass):
        def __init__(self):
            super(LocationThinMist, self).__init__("Thin mist", "TODO", False)


    class LocationSlums(_LocationBaseClass):
        def __init__(self):
            super(LocationSlums, self).__init__("Slums", "TODO", True)
            self.jobs = [JobFoodThief()]

    class LocationMarket(_LocationBaseClass):
        def __init__(self):
            super(LocationMarket, self).__init__("Market", "TODO", True)


    class LocationDepository(_LocationBaseClass):
        def __init__(self):
            super(LocationDepository, self).__init__("Depository", "TODO", True)


    class LocationCharityMission(_LocationBaseClass):
        def __init__(self):
            super(LocationCharityMission, self).__init__("Charity Mission", "TODO", True)
            self.jobs = [JobFoodBeggar()]

    class LocationOutpost(_LocationBaseClass):
        def __init__(self):
            super(LocationOutpost, self).__init__("Outpost", "TODO", True)
            self.jobs = [JobFoodWhore()]


    class LocationSlaverEncampment(_LocationBaseClass):
        def __init__(self):
            super(LocationSlaverEncampment, self).__init__("Slaver Encampment", "TODO", True)


    class LocationRuinedFortifications(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedFortifications, self).__init__("Ruined Fortifications", "TODO", True)


    class LocationJunkyard(_LocationBaseClass):
        def __init__(self):
            super(LocationJunkyard, self).__init__("Junk yard", "TODO", True)
            self.jobs = [JobScavenger()]

            
    class LocationMine(_LocationBaseClass):
        def __init__(self):
            super(LocationMine, self).__init__("Mine", "TODO", True)
            self.jobs = [JobFuelExtractor()]

            
    class LocationDyingGrove(_LocationBaseClass):
        def __init__(self):
            super(LocationDyingGrove, self).__init__("Dying grove", "TODO", True)
            self.jobs = [JobWoodGathering(), JobHerbalism()]
            

    class LocationRuinedHouses(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedHouses, self).__init__("Ruined houses", "TODO", True)
            self.jobs = [JobMarauder()]


    class LocationRuinedFactory(_LocationBaseClass):
        def __init__(self):
            super(LocationRuinedFactory, self).__init__("Ruined factory", "TODO", True)
            self.jobs = [JobToolScavenger()]


    class LocationGrimBattlefield(_LocationBaseClass):
        def __init__(self):
            super(LocationGrimBattlefield, self).__init__("Grim battlefield", "TODO", True)
            self.jobs = [JobWeaponLooter()]


    class LocationsModel:
        def __init__(self):
            # стартовая локация
            mist = LocationThinMist()
            mist.explored = True
            mist.can_have_camp = False
            # доступные локации. Сюда они постепенно переезжают из __closed_locations
            # при вызове _add_random_closed_location()
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
            
            result = []
            if (character.camp_location_index != location_index) and loc.can_have_camp:
                result.append(LocationActionMoveCamp())
            for job_num in xrange(0, len(loc.jobs)):
                if (character.job_location_index != location_index) or (character.job_num != job_num):
                    job = loc.jobs[job_num]
                    result.append(LocationActionChangeJob(job.name, job.description, job, job_num))
            return result

        def add_random_closed_location(self):
            if not self.__closed_locations:
                return  # Если закрытых не осталось, то просто ничего не делаем
            last_index = len(self.__closed_locations) - 1
            random_index = random.randint(0, last_index)  # Return a random integer N a <= N <= b
            self.locations.append(self.__closed_locations[random_index])
            if random_index < last_index:
                self.__closed_locations[random_index] = self.__closed_locations[last_index]
            del self.__closed_locations[last_index]
