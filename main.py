import sys
from gameinfo import GameInfo
from architecture_class import Room, Furniture
from character import Enemy, Friend

Befriender = GameInfo()
GameInfo.getgamedata()
GameInfo.readrules(Befriender)
GameInfo.definelevel()

myitems = list()
optionlist = list()

"""
start the new room and its inhabitant
"""
GameInfo.current_room = GameInfo.defaultroom()
while GameInfo.lives > 0:
    GameInfo.banner()
    """
    checks if there is a character in the room
    for all cases, defines command options and the explore status of the room
    """
    inh_profile = GameInfo.current_room.get_ch_det()
    inhabitant = GameInfo.current_room.get_character()
    if inhabitant is not None:
        """
        checks the type of character
        """
        wtd = GameInfo.whatchoice(inhabitant, Room.current_room, myitems)
        command = wtd[0]
        optionlist = wtd[1]
    else:
        GameInfo.current_room.explored = 1
        if GameInfo.current_room.get_search() == 1:
            print('You already cleared and searched this room')
            optionlist = ['m']
            command = 'm'
        else:
            command = input(">  What do you want to do?\n\tMove (m)?\n\texplore (x)? > ")
            optionlist = ['m', 'x'] + GameInfo.generaloptionslist

    if command not in optionlist:
        """
        this section checks that the command is valid
        """
        print('\nSorry, no such command!')
        continue
    elif command == str.lower('m'):
        """
        this section deals with moving from room to room
        """
        #display possible moves
        moveoption = GameInfo.current_room.can_move(GameInfo.House_dict)
        GameInfo.changeroom(moveoption)
        continue

    elif command == str.lower('x'): #exploring sequence
        """
        this section defines searching for objects in the furniture (not already searched)
        """
        GameInfo.explore(Befriender, myitems)


    elif command == str.lower('t'): #talking sequence
        """
        this section defines the talk exchange with a friend and receiving a gift
        """
        GameInfo.speechsequence(Befriender, inhabitant, inh_profile, myitems)

    elif command == str.lower('f'): #fighting sequence
        """
        this section defines fighting with an enemy
        """
        if len(myitems) !=0:
            lives = GameInfo.lives
            myfight = GameInfo.rumble(Befriender, myitems, inhabitant, inh_profile[0], inh_profile[1])
            GameInfo.health = myfight[2]
            if lives > myfight[3]:
                GameInfo.defaultroom()
                GameInfo.lives = myfight[3]
            continue
        else:
            print('You cannot fight, your inventory is empty!')
            continue

    else:
        GameInfo.mainmenu(Befriender,command)

sys.exit(0)
