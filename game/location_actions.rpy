# coding=utf-8

label lbl_buyfood(in_resources_for_trade, out_resources_to_sell):
    call screen scr_buy_food(in_resources_for_trade, out_resources_to_sell)
    return (_return)

init -1 python:

    from pythoncode.character import Character as MB_Character # Character уже есть в RenPy
    from pythoncode.resources import Resources
    
    class _LocationActionBaseClass(object):
        def __init__(self, name, description, spend_action_point):
            self._name = name
            self._description = description
            self.spend_action_point = spend_action_point

        def do_action(self, character, game, locaton_index):
            raise Exception('do_action not implemented for: %s' % self.name)
        
        def __common_action_result(self, character, game, locaton_index):
            if self.spend_action_point:
                character.action_points = character.action_points - 1
            game.new_turn_if_need()
            return True

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
            super(LocationActionMoveCamp, self).__init__("Move camp", "Move camp here", True)

        def do_action(self, character, game, locaton_index):
            if not game.locations_model.locations[locaton_index].can_have_camp:
                raise Exception('WTF in move camp action.')
            character.camp_location_index = locaton_index
            return self.__common_action_result(character, game, locaton_index)

            
    class LocationActionExplore(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionExplore, self).__init__("Explore", "Explore location", True)

        def do_action(self, character, game, locaton_index):
            game.locations_model.locations[locaton_index].explored = True
            game.locations_model.add_random_closed_location()
            return self.__common_action_result(character, game, locaton_index)
            
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
            return self.__common_action_result(character, game, locaton_index)
            
        @property
        def name(self):
            if self.spend_action_point:
                return '(!) job:' + self._name
            return _name
    
    
    class LocationActionBuyFood(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionBuyFood, self).__init__("Buy food", "Trade other resources for food", False)

        def do_action(self, character, game, locaton_index):
            res_to_sell = Resources()
            res_to_sell.food = 0
            #ret = False
            #renpy.show_screen("scr_buy_food", character.resources, res_to_sell, ret)
            ret = renpy.call_in_new_context("lbl_buyfood", character.resources, res_to_sell)
            if ret:
                character.resources.subtract(res_to_sell)
                character.resources.food += int(res_to_sell.get_can_buy_number())
            return self.__common_action_result(character, game, locaton_index)
    
            
    class LocationActionRentStorage(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionRentStorage, self).__init__("Rent storage", "Rent a storage for 10% of your resources", True)

        def do_action(self, character, game, locaton_index):
            character.set_storage(MB_Character.STORAGE_RENT)
            return self.__common_action_result(character, game, locaton_index)
            
            
    class LocationActionNoMoreRentStorage(_LocationActionBaseClass):
        def __init__(self):
            super(LocationActionNoMoreRentStorage, self).__init__("No more rent storage", "No more rent", True)

        def do_action(self, character, game, locaton_index):
            character.set_storage(MB_Character.STORAGE_NONE)
            return self.__common_action_result(character, game, locaton_index)
