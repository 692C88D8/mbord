﻿# coding=utf-8

init -1 python:
    import renpy.exports as renpy
    import renpy.store as store
    from pythoncode.character import Character as MB_Character # Character уже есть в RenPy
    import pythoncode.jobs as jobs
    
    #from enum import Enum
    #class GameState(Enum): Енумов в ренпи не завезли!
    class GameState:
        STOPPED = 1
        BORDER_MAP = 2
    
    class Game(store.object):
        
        def __init__(self):
            self.locations_model = LocationsModel()
            self.player_character = MB_Character()
            self.state = GameState.STOPPED
            
        def get_location_name_to_display(self, location_index):
            name = self.locations_model.locations[location_index].name
            if location_index == self.locations_model.selected_location_index:
                name = ">" + name
            loc_suffix = ""
            if location_index == self.player_character.camp_location_index:
                loc_suffix = "(c)"
            if location_index == self.player_character.job_location_index:
                loc_suffix += "(j)"
            if len(loc_suffix) > 0:
                name = name + " " + loc_suffix
            return name
        
        def get_location_description(self, location_index):
            return self.locations_model.locations[location_index].description
            
        def set_state(self, state):
            self.state = state
            
        def get_state(self):
            return self.state
            
        def get_character_job(self, character):
            if character.job_location_index is None:
                return jobs.JobIdle()
            return self.locations_model.locations[character.job_location_index].jobs[character.job_num]
            
        def new_turn_if_need(self):
            if self.player_character.action_points <= 0 :
                self.on_new_turn()
            
        def on_new_turn(self):
            pchar = self.player_character
            pchar.on_new_turn(self)
            
        def is_player_job_available(self):
            return self.player_character.get_current_job_state(self.locations_model) == MB_Character.JOB_AVAILABLE