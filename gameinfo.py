import sys
from architecture_class import Room, Furniture
from character import Enemy, Friend

class GameInfo():
    author = 'Hacène Dramchini'
    generaloptionslist = ['k', 'o', 'r', 'q', '@']
    lives = 3
    health = 9
    default_room  = ''
    current_room = ''
    #Dictionaries:
    #   for the rooms in the house
    House_dict = dict()
    #   for each item of furniture
    Furn_dict = dict()
    #   for Friends
    Fr_dict = dict()
    #   for Enemies
    En_dict = dict()
    #   for all characters
    Ch_dict = dict()
    potentialfriends = 0

    def __Init__(self, game_title):
        self.title = game_title

    @classmethod
    def getgamedata(cls):
        """
        this section gets the layout of the room,
        the furniture with hidden object in each room
        the characters in each room
        """
        def buildhouse(stg, stg_name, stg_desc):
            """
            function to create room objects and assign details
            """
            n_stg = stg
            stg = Room()
            stg.name = str.lower(stg_name)
            stg.description = stg_desc
            cls.House_dict[str(n_stg)] = stg
            return stg, cls.House_dict

        def furnishhouse(r_name, stg, stg_name, stg_desc, stg_hidden):
            """
            function to create furniture objects and assign details
            """
            n_stg = stg
            stg = Furniture()
            stg.name = stg_name
            stg.description = stg_desc
            """
            the hidden_item will pass a 2 item list to the hidden property of the furniture
            all items follow the same list pattern
            (see in next function ==> unwrap_gift)
            """
            hidden_item = stg_hidden.split('|')
            stg.set_hidden(hidden_item)
            stg.set_room(r_name)
            cls.Furn_dict[str(n_stg)] = stg

            """
            #assign furniture to room
            """
            myroom = cls.House_dict[r_name]
            myroom.set_furn(n_stg, stg_name, stg_desc)

            return stg, cls.Furn_dict, cls.House_dict

        def charsetting(s_name, c_type, room_asgn, c_cat, c_speech, c_weakness):
            """
            function to create character objects and assign details
            """
            n_stg = s_name
            unwrap_gift = c_weakness.split('|')
            if c_type == 'Friend':
                """
                the unwrap_gift will pass a 2 item list to the friend
                all items follow the same list pattern
                (see in previous function ==> hidden_item)
                """
                stg = Friend(s_name, c_cat, c_speech, (unwrap_gift[0],unwrap_gift[1]))
                cls.Fr_dict[str(n_stg)] = stg
                cls.Ch_dict[str(n_stg)] = stg
            else:
                stg = Enemy(s_name, c_cat, c_speech, unwrap_gift)
                GameInfo.potentialfriends += 1
                cls.En_dict[str(n_stg)] = stg
                cls.Ch_dict[str(n_stg)] = stg
            for rm, r_obj in cls.House_dict.items():
                """
                assign character to room
                """
                if room_asgn == rm:
                    r_obj.set_character(stg)
                    r_obj.set_ch_det(cls.Ch_dict)

            return stg, cls.Fr_dict, cls.En_dict, cls.Ch_dict, cls.House_dict

        """
        this section reads the layout of the house and links the rooms.

        The file "house_layout.txt" has the following structure:
          col 1:  room name (origin) ==> key value from house_dict (no space!)
          col 2:  direction
          col 3:  room name (target) ==> key value from house_dict (no space!)
        """
        fhand = open('room_details.txt')
        i = 1
        for line in fhand:
            att = line.split('\t')
            if len(att) != 0:
                buildhouse(att[0], att[1], att[2])
                if i ==1:
                    GameInfo.default_room = cls.House_dict[att[0]]
                    GameInfo.current_room = cls.House_dict[att[0]]
                i += 1
        fhand.close

        """
        this section reads the layout of the house and links the rooms.

        The file "house_layout.txt" has the following structure:
          col 1:  room name (origin) ==> key value from house_dict (no space!)
          col 2:  direction
          col 3:  room name (target) ==> key value from house_dict (no space!)

        """
        fhand = open('house_layout.txt')
        for line in fhand:
            line = line.strip()
            att = line.split('\t')
            if len(att) != 0:
                crr = GameInfo.House_dict[att[0]]
                tgr = GameInfo.House_dict[att[2]]
                crr.link_room(tgr, att[1])
        fhand.close

        """
        this section defines the furniture in each room

        The file "furn_data.txt" has the following structure:
          col 1:  room name ==> key value in House_dict (no space!)
          col 2:  furniture name ==> key value in Furn_dict (no space!)
          col 3:  furniture display name
          col 4:  furniture description
          col 5:  hidden object
                      divided into 2 components separated by | sign
                          comp 1: object, set to "nothing" if no object
                          comp 2: 0 = not relevant
                                  k = will kill a character
                                  c = will convert an enemy into a friend
        """
        fhand = open('furn_data.txt')
        for line in fhand:
            att = line.split('\t')
            if len(att) != 0:
                furnishhouse(att[0], att[1], att[2], att[3], str.strip(att[4]))
        fhand.close

        """
        this section defines all the characters in the game
        The file "character_data.txt" has the following structure:
          First lists all Enemies
          Second lists all Friends
          col 1:  character name ==> key value in Char_dict, En_Dict or Fr_Dict (no space!)
          col 2:  character type ==> Friend or Enemy
          col 3:  room to be found in ==> key value in House_dict (no space!)
          col 4:  character description
          col 5:  character speech
                  Enemy or Friend (to cater for potential Enemy conversion into Friend)
                      3 bar separated components
                          comp 1: greetings
                          comp 2: hint as to the use for the gift to be received
                          comp 3: line to bestow the character gift to the player
          col 6:  | separated content
                  Enemy:  comp 1: what frightens it
                          comp 2: what kills it
                          comp 3: what converts it into a friend
                  Friend: comp 1: gift name
                          comp 2: category (always "g")
                          comp 3: Enemy concerns (target name)
        """
        fhand = open('character_data.txt')
        for line in fhand:
            #removes the line return at the end of the line
            cline = line.rstrip()
            att = cline.split('\t')
            if len(att) != 0:
                charsetting(att[0], att[1], att[2], att[3], att[4], att[5])
        fhand.close

    def readrules(self):
        """
        This is the game introduction section
        """
        self.readfile('houseexplorer_rules.txt')
        a = 1
        b = 1
        self.banner()
        print('> or play (p)')
        while a == 1:
            optionlist = ['p'] + self.generaloptionslist
            inp = input('  > ')
            if len(inp)>0:
                if str.lower(inp[0]) not in optionlist:
                    continue
                elif str.lower(inp[0]) in self.generaloptionslist:
                    self.mainmenu(str.lower(inp[0]))
                    continue
                else:
                    break
            else:
                continue

    @classmethod
    def definelevel(cls):
        """
        this is the main playing section
        """
        print('********************************************')
        print('*            Choose your level             *')
        print('********************************************')
        print('* 1) Easy, 2) Medium, 3) hard, 4) insane   *')
        print('********************************************')
        while True:
            inp = input('> ')
            if len(inp) !=0:
                if str.lower(inp[0]) not in ['1','2','3','4']:

                    continue
                elif inp == '4':
                    cls.lives = 1
                    cls.health = 3
                    break
                else:
                    tval = int(inp) - 1
                    cls.lives = 3 - tval
                    cls.health = 9
                    break
            else:
                continue

        print('********************************************')
        print("Let's begin")
        print('********************************************')

    @staticmethod
    def banner():
        """
        function to display always the general options
        """
        print('************************************************')
        print('* map (k) - options (o) - rules (r) - quit (q) *')
        print('************************************************')

    @classmethod
    def completedgame(cls):
        """
        this function is for the end of the game once all enemies have been vanquished or converted
        """
        print('************************************************')
        print('  CONGRATULATIONS - YOU WIN - no more enemies  *')
        print('************************************************')
        if Enemy.converts !=0:
            enm = ('    x','  O/ ',' /|  ',' / \ ')
            inb = ('     ','     ',' ==> ','     ')
            frd = ('     ',' \O/ ','  |  ',' / \ ')
            if Enemy.converts == 1:
                myend = ('enemy', 'a friend')
            else:
                myend = ('enemies', 'friends')
            print('\tYou converted', Enemy.converts, myend[0], 'into', myend[1])
            x = 1
            while x < len(enm)+1:
                print(enm[x-1] * 3, inb[x-1], frd[x-1] * 3)
                x +=1
            if Enemy.converts == GameInfo.potentialfriends:
                print('\nPerfect game!\nYou managed to convert all your enemies into friends!\nVery well done!!!!')
                print('\nYou now live in a house full of friends!')
            else:
                print('\nWell done converting some of your enemies into friends!\n')
                print('A pity you had to kill some!\n')
                print('Still, the house is now enemy free!\nWell done!')
        else:
            print('\nYou killed all your enemies!\nNext time try to change them into friends!')
        exit('Thank you for playing')

    @classmethod
    def credit(cls):
        print('Thank you for playing!')
        print('Created by', cls.author)

    def readfile(self,txtfile):
        """
        function to read the various text files
        """
        fhand = open(txtfile)
        print(fhand.read())
        fhand.close

    def mainmenu(self, inp):
        """
        #this function is to deal with player keying a main menu options
        the option '@' is a secret cheat to see the list of enemies and what affects them and how
        """
        if inp == 'k':
            self.readfile('house_map.txt')
        elif inp == 'r':
            self.readfile('houseexplorer_rules.txt')
        elif inp == 'o':
            self.readfile('houseexplorer_options.txt')
        elif inp == '@':
            self.readfile('houseexplorer_enemies.txt')
        elif inp == 'q':
            confirm = input('> Do you really want to quit (y or n)? > ')
            if confirm == 'y':
                exit('Thank you for playing')
        else:
            print('something is wrong!')

    def chat(self, lp):
        """
        this function deals with the conversation with a character
        """
        if lp == 0:
            print('[ You]:\t\tPlease to meet you!')
        elif lp==1:
            print('[ You]:\tWhat is special about you?')
        else:
            print('[ You]:\tIt is so nice for you.')

    @staticmethod
    def whatchoice(inhabitant, current_room, myitems):
        """
        This function defines the options available to the player
        """
        if isinstance(inhabitant,Enemy)==True:
            GameInfo.current_room.set_explored(0)
            if inhabitant.get_concede() == 1:
                optionlist = ['m', 'x'] + GameInfo.generaloptionslist
                mystg = input(">  What do you want to do?\n\tMove (m)?\n\tExplore (x)? > ")
            else:
                if len(myitems) != 0:
                    optionlist = ['m', 'f'] + GameInfo.generaloptionslist
                    mystg = input(">  What do you want to do?\n\tMove (m)?\n\tFight (f)? > ")
                else:
                    optionlist = ['m'] + GameInfo.generaloptionslist
                    mystg = input(">  You can only Move (m)! > ")
        else:
            GameInfo.current_room.explored = 1
            if GameInfo.current_room.get_searched() == 0:
                optionlist = ['m', 'x', 't'] + GameInfo.generaloptionslist
                mystg = input(">  What do you want to do?\n\tMove (m)?\n\texplore (x)?\n\ttalk (t)? > ")
            else:
                optionlist = ['m', 't'] + GameInfo.generaloptionslist
                mystg = input(">  What do you want to do?\n\tMove (m)?\n\ttalk (t)? > ")
        return mystg, optionlist, myitems

    @classmethod
    def defaultroom(cls):
        """
        this function reset the game to the original default room
        where the game starts and where the player respawn after losing a life
        """
        cls.current_room = cls.default_room
        inhabitant = cls.current_room.get_character()
        inh_profile = cls.current_room.get_ch_det()
        cls.current_room.describe()
        return cls.current_room

    @classmethod
    def changeroom(cls, moveoption):
        """
        this function deals with moving between rooms
        """
        optl = str([x[0] for x in moveoption])
        a = 0
        b = 1
        while a == 0:
            mymove = input(' > your choice: ')
            if mymove not in optl:
                print('Not an option!')
                continue
            else:
                if mymove in optl:
                    myref = int(mymove) - 1
                    mytup = moveoption[myref]
                    GameInfo.current_room = GameInfo.current_room.move(mytup[1], GameInfo.House_dict)
                    inhabitant = GameInfo.current_room.get_character()
                    inh_profile = GameInfo.current_room.get_ch_det()
                    GameInfo.current_room.describe()
                    if isinstance(inhabitant,Enemy)==True:
                        inhabitant.set_concede(0)
                    print("\n")
                    a == 1
                    break
                elif mymove in GameInfo.generaloptionslist:
                    GameInfo.mainmenu(mymove)
                else:
                    continue

    def speechsequence(self, inhabitant, inh_profile, myitems):
        """
        this function deals with the talk sequence of the game
        """
        myspeech = inhabitant.talk()
        print('[' + inh_profile[0], 'says]: I am', inh_profile[0] + ', a', inh_profile[1] +'.')
        lp = 0
        while lp<3:
            inp = input('(press return) >')
            GameInfo.chat(self, lp)
            if lp<2:
                print('[' + inh_profile[0], 'says]:\t', myspeech[lp],'\n')
            lp +=1
        inp = input('>')
        if inhabitant.get_given() == 0:
            print('[' + inh_profile[0], 'says]:\t', myspeech[2],'\n')
            gft = str(inhabitant.present)
            if gft[0] in ['a','f']:
                msg = 'some'
            else:
                msg = 'a'
            print('\n', inhabitant.name, 'gives you', msg, inhabitant.present, '\n')
            myitems.append(inhabitant.gift)
            inhabitant.set_given(1)

    def explore(self, myitems):
        """
        this function deals with searching the room
        """
        a = 0
        while a == 0:
            for k,v in GameInfo.House_dict.items():
                if v.name == GameInfo.current_room.name:
                    r_name = k
                    continue
            Cansearchin = GameInfo.current_room.searchable(GameInfo.Furn_dict, r_name)
            """
            defines the furniture in the room that has not yet been searched
            """
            if len(Cansearchin) != 0:
                res_list = str([x[0] for x in Cansearchin])
                mysearch = input('> Select a number or x to stop searching > ')
                if mysearch == 'x':
                    a = 1
                    break
                elif mysearch in res_list:
                    myref = int(mysearch) - 1
                    mytup = Cansearchin[myref]
                    myfurn = GameInfo.Furn_dict[mytup[1]]
                    print('\n\tIn the', myfurn.get_name(), 'you found ==> ', myfurn.get_hidden(),'\n')
                    if myfurn.get_hidden() != str.lower('nothing'):
                        myitems.append((myfurn.get_hidden(),myfurn.get_purpose()))
                        myfurn.set_hidden('nothing')
                    myfurn.set_explore(1)
                elif mysearch in GameInfo.generaloptionslist:
                    GameInfo.mainmenu(self, mysearch)
                else:
                    print('This is not an option!')

            else:
                GameInfo.current_room.set_searched(1)
                print('You already searched/found everything in this room!')
                a = 1
                break
        return myitems

    def rumble(self, myitems, inhabitant, name, profile):
        """
        this function deals with the fight sequence of the game
        """
        fightfinished = False
        while fightfinished == False:
            print('************* FIGHT - FIGHT - FIGHT ************')
            print('*           YOU\tvs.\t', str.upper(name), 'the', profile)
            print('************************************************')
            numlist = list()
            rk = 1
            print('You can use:')
            usedweapon = [itm[0] for itm in myitems]
            for usedweapon in myitems:
                print('\t-', rk, ')\t', usedweapon[0])
                numlist.append(str(rk))
                rk +=1
            print('\tor simply give up the fight (g)!')
            fightinput = input('> what do you want to use? > ')
            if fightinput not in numlist:
                if fightinput != str.lower('g'):
                    print('This is not an option!\n')
                else:
                    print('Wise choise!\n')
                    break
            else:
                myref = int(fightinput) - 1
                weapon = myitems[myref]
                fightresult = inhabitant.fight(weapon, GameInfo.health, GameInfo.lives)
                GameInfo.health = fightresult[1]
                if fightresult[0] == True:
                    if inhabitant.get_befriended() == 1:
                        myitems.pop(myref)
                        converted = Friend(inhabitant.name, inhabitant.description, inhabitant.conversation, ("",""))
                        converted.set_given(1)
                        converted.explored = 1
                        GameInfo.Fr_dict[str(inhabitant.name)] = converted
                        GameInfo.En_dict.pop(inhabitant.name)
                        inhabitant = converted
                        GameInfo.current_room.set_character(inhabitant)
                        print('Well done, you converted', inhabitant.name, 'into a friend\n')
                    else:
                        if inhabitant.get_killed() == 1:
                            GameInfo.En_dict.pop(inhabitant.name)
                            inhabitant = None
                            GameInfo.current_room.set_character(None)

                    if len(GameInfo.En_dict) == 0:
                        GameInfo.completedgame()
                    fightfinished = True
                else:
                    if fightresult[2] == 0:
                        exit('Thank you for playing')
                    elif fightresult[2]!= GameInfo.lives:
                        print('You cannot fight anymore!')
                        GameInfo.lives = fightresult[2]
                        fightfinished = True

        return myitems, inhabitant, GameInfo.health, GameInfo.lives