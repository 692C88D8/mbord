# coding=utf-8

init -1 python:

    class _LocationActionBaseClass(object):
        def __init__(self, name, description, spend_action_point):
            self._name = name
            self._description = description
            self.spend_action_point = spend_action_point

        def do_action(self, character, game, locaton_index):
            raise Exception('do_action not implemented for: %s' % self.name)

        @property
        def name(self):
            if self.spend_action_point:
                return '(!) ' + self._name
            return self._name

        @property
        def description(self):
            return self._description
            
    class LocationActionMoveCamp(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionMoveCamp, self).__init__("Move camp", "TODO", True)

        def do_action(self, character, game, locaton_index):
            if not game.locations_model.locations[locaton_index].can_have_camp:
                raise Exception('WTF in move camp action.')
            character.camp_location_index = locaton_index
            return True

            
    class LocationActionExplore(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionExplore, self).__init__("Explore", "TODO", True)

        def do_action(self, character, game, locaton_index):
            game.locations_model.locations[locaton_index].explored = True
            game.locations_model.add_random_closed_location()
            return True
            
#TODO Подумать: можно сделать типа классового метода CreateJobActionsList(jobs[], locaton_index)
#и пришлепывать этот лист вместо одиночного поочередного создания
    class LocationActionChangeJob(_LocationActionBaseClass):
        def __init__(self, name, description, job, job_num):
            super(LocationActionChangeJob, self).__init__(name, description, True)
            self.job = job
            self.job_num = job_num

        def do_action(self, character, game, locaton_index):
            if (character.job_location_index == locaton_index) and (character.job_num == self.job_num):
                raise Exception('WTF in change job. It should not be available')
            character.job_location_index = locaton_index
            character.job_num = self.job_num
            return True
            
        @property
        def name(self):
            if self.spend_action_point:
                return '(!) job:' + self._name
            return _name
    
    
    class LocationActionTradeResources(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionTradeResources, self).__init__("Trade resources", "TODO", True)

        def do_action(self, character, game, locaton_index):
            raise Exception('TODO trade not implemented')
    
