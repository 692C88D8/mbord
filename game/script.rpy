# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('Eileen', color="#c8ffc8")

python:
    from pythoncode.character import Character as MB_Character # Character уже есть в RenPy

# The game starts here.
label start:
    $ game = Game()
    $ game.set_state(GameState.BORDER_MAP)
    $ pchar = MB_Character()
    call screen scr_char_edit(pchar)
    if _return:
        $ game.player_character = pchar
    else:
        return
    while game.get_state() != GameState.STOPPED:
        call screen scr_map(game)

    #call screen scr_map(game)

    return
