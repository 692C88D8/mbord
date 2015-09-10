
init python:
      from pythoncode.resources import Resources
      from pythoncode.utils import *
      

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say(who, what, side_image=None, two_window=False):

    # Decide if we want to use the one-window or two-window variant.
    if not two_window:

        # The one window variant.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"

    # If there's a side image, display it above the text.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu


##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):

    window:
        style "menu_window"
        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, action, chosen in items:

                if action:

                    button:
                        action action
                        style "menu_choice_button"

                        text caption style "menu_choice"

                else:
                    text caption style "menu_caption"

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Main Menu
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    # The background of the main menu.
    window:
        style "mm_root"

    # The main menu buttons.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Start Game") action Start()
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit(confirm=False)

init -2:

    # Make all the main menu buttons be the same size.
    style mm_button:
        size_group "mm"



##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation():

    # The background of the game menu.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init -2:

    # Make all game menu navigation buttons the same size.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.

screen file_picker():

    frame:
        style "file_picker_frame"

        has vbox

        # The buttons at the top allow the user to pick a
        # page of files.
        hbox:
            style_group "file_picker_nav"

            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Quick"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Next"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Display a grid of file slots.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Display ten file slots, numbered 1 - 10.
            for i in range(1, columns * rows + 1):

                # Each file slot is a button.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Add the screenshot.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save():

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

screen load():

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

init -2:
    style file_picker_frame is menu_frame
    style file_picker_nav_button is small_button
    style file_picker_nav_button_text is small_button_text
    style file_picker_button is large_button
    style file_picker_text is large_button_text


##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences():

    tag menu

    # Include the navigation.
    use navigation

    # Put the navigation columns in a three-wide grid.
    grid 3 1:
        style_group "prefs"
        xfill True

        # The left column.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Voice Volume")
                    bar value Preference("voice volume")

                    textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Test"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2:
    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0


##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt(message, yes_action, no_action):

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action

    # Right-click and escape answer "no".
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu():

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Skip") action Skip()
        textbutton _("F.Skip") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Prefs") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"

    style button_not_active:
        is default
        size 12
        idle_color "#6666"
        hover_color "#6666"
        selected_idle_color "#6666"
        selected_hover_color "#6666"
        insensitive_color "#6666"
        
screen scr_map(game):
    # Информация сверху
    frame:
        xpos 0
        ypos 0
        align(0.0, 0.0)
        has hbox:
            spacing 10
            $ res = game.player_character.resources
            text "food: %s" % res.food
            text "fuel: %s" % res.fuel
            text "drugs: %s" % res.drugs
            text "arms: %s" % res.arms
            text "tools: %s" % res.tools
            text "material: %s" % res.material
    # Список локаций слева
    frame:
        xpos 0
        ypos 40
        xsize 300
        align(0.0, 0.0)
        has vbox
        $ i = 0
        for location in game.locations_model.locations:
            $ actions_list = game.locations_model.get_location_actions(game.player_character, i)
            $ location_name = game.get_location_name_to_display(i)
            if game.locations_model.is_location_in_reach(game.player_character, i) :
                textbutton(location_name):
                    action Function(game.locations_model.set_selected_location_index, i)
            else:
                textbutton(location_name):
                    style "button_not_active"
                    action Function(game.locations_model.set_selected_location_index, i)
            $ i = i + 1
    # Информация посередине
    frame:
        xpos 305
        ypos 40
        xsize 190
        align(0.0, 0.0)
        has vbox
        $ char = game.player_character
        text "Name: %s" % char.name
        text "physique: %s" % char.physique
        text "agility: %s" % char.agility
        text "spirit: %s" % char.spirit
        text "mind: %s" % char.mind
        text "ration: %s" % char.ration
        text "AP: %s" % char.action_points
        if game.is_player_job_available():
            text "Job: %s" % game.get_character_job(char).name
        else:
            text "Job: %s" % game.get_character_job(char).name:
                strikethrough True
        text "Storage: %s" % char.get_storage_name()
        if char.starving > 0 :
            text "Starving!"
        textbutton "Next turn":
            action Function(game.on_new_turn)
    # Список действий справа
    frame:
        xpos 500
        ypos 40
        xsize 300
        align(0.0, 0.0)
        has vbox
        $ loc_index = game.locations_model.selected_location_index
        $ actions = game.locations_model.get_location_actions(game.player_character, loc_index)
        if game.locations_model.is_location_in_reach(game.player_character, loc_index) :
            for action in actions:
                textbutton(action.name):
                    action Function(action.do_action, game.player_character, game, loc_index)
        else:
            for action in actions:
                textbutton(action.name):
                    style "button_not_active"
            
    # Текст с описанием внизу того на что наведен курсор мыши
    #TODO
    
    textbutton "Выход!":
        align(0.97, 0.0)
        action [Function(game.set_state, GameState.STOPPED), Return()]
        
#init -1 python:
#    glob_char = None
#    def update_name(value=""):
#        global glob_char
#        glob_char.name = value
        
screen scr_char_edit(char):
    # TODO осилить ввод имени
    #$ global glob_char
    #$ glob_char = char
    frame:
        has vbox
        #text "Enter your name:"
        #input default char.name length 12 changed update_name
        text "physique: %s" % char.physique
        bar value FieldValue(char, 'physique', range=5, offset=0, step=1)
        text "agility: %s" % char.agility
        bar value FieldValue(char, 'agility', range=5, offset=0, step=1)
        text "spirit: %s" % char.spirit
        bar value FieldValue(char, 'spirit', range=5, offset=0, step=1)
        text "mind: %s" % char.mind
        bar value FieldValue(char, 'mind', range=5, offset=0, step=1)
        text "ration: %s" % char.ration
        bar value FieldValue(char, 'ration', range=5, offset=0, step=1)
        text "AP: %s" % char.action_points
        bar value FieldValue(char, 'action_points', range=5, offset=0, step=1)
        textbutton("Ok"):
                action Return(True)
        textbutton("Cancel"):
                action Return(False)


screen scr_buy_food(in_resources_for_trade, out_resources_to_sell):
    zorder 1
    modal True
    frame:
        has vbox
        if in_resources_for_trade.fuel > 0:
            text "Sell fuel: %d" % out_resources_to_sell.fuel
            bar value FieldValue(out_resources_to_sell, 'fuel', range=in_resources_for_trade.fuel, offset=0, step=1)
        if in_resources_for_trade.drugs > 0:
            text "Sell drugs: %d" % out_resources_to_sell.drugs
            bar value FieldValue(out_resources_to_sell, 'drugs', range=in_resources_for_trade.drugs, offset=0, step=1)
        if in_resources_for_trade.arms > 0:
            text "Sell arms: %d" % out_resources_to_sell.arms
            bar value FieldValue(out_resources_to_sell, 'arms', range=in_resources_for_trade.arms, offset=0, step=1)
        if in_resources_for_trade.tools > 0:
            text "Sell tools: %d" % out_resources_to_sell.tools
            bar value FieldValue(out_resources_to_sell, 'tools', range=in_resources_for_trade.tools, offset=0, step=1)
        if in_resources_for_trade.material > 0:
            text "Sell material: %d" % out_resources_to_sell.material
            bar value FieldValue(out_resources_to_sell, 'material', range=in_resources_for_trade.material, offset=0, step=1)
        $ food_buy_num = out_resources_to_sell.get_can_buy_number()
        text "Buy food: %d" % food_buy_num
        if food_buy_num > 0 and is_whole_number(food_buy_num):
            textbutton("Trade"):
                action Return(True)
        else:
            textbutton("Trade"):
                style "button_not_active"
        
        textbutton("Cancel"):
                action Return(False)