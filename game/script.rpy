# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('Eileen', color="#c8ffc8")

# The game starts here.
label start:

    $ game = Game()
    $ game.set_state(GameState.BORDER_MAP)
    while game.get_state() != GameState.STOPPED:
        $ renpy.call_screen("scr_map", game)

    #call screen scr_map(game)

    return
