'''
Created on Jul 31, 2013

@author: Justin
'''


BUILD_TABLE = [["Skinny", "Average", "Overweight", "Fat", "Very Fat"],
               [(40,80),   (60,120),  (80,160),  (90,180),  (120,240)], 
               [(50,90),   (75,135),  (100,175), (115,205), (150,270)], 
               [(60,100),  (90,150),  (120,195), (135,225), (180,300)], 
               [(70,110),  (105,165), (140,215), (160,250), (210,330)],
               [(80,120),  (115,175), (150,230), (175,265), (230,350)], 
               [(85,130),  (125,195), (165,255), (190,295), (250,390)], 
               [(95,150),  (140,220), (185,290), (210,330), (280,440)], 
               [(105,165), (155,245), (205,320), (235,370), (310,490)], 
               [(115,180), (170,270), (225,355), (255,405), (340,540)],
               [-5,        0,         -1,        -3,        -5     ]]

HEIGHT_TABLE = [["height"],
               [(4.4,5.2)],
               [(4.7,5.5)],
               [(4.10,5.8)], 
               [(5.1,5.11)], 
               [(5.3,6.1)], 
               [(5.5,6.3)], 
               [(5.8,6.6)], 
               [(5.11,6.9)], 
               [(6.2,7.0)]]

APPEARANCE_TABLE = [["Horrific", "Monstrous", "Hideous", "Ugly", "Unattractive", "Average", "Attractive", "Handsome", "Very handsome", "Transcendent"],
                    ["You are indescribably monstrous or unspeakably foul, andcannot interact with normal mortals. This gives -6 on reaction rolls. The GM may decide that this trait is supernatural and unavailable to normal characters -24 points",
                     "You are hideous and clearly unnatural. Most people react to you as a monster rather than a sapient being. This gives -5 on reaction rolls. Again, this trait might not be appropriate for normal characters. -20 points",
                     "You have any sort of disgusting looks you can come up with: a severe skin disease, wall-eye . . . preferably several things at once. This gives -4 on reaction rolls. -16 points",
                     "You have a few disgusting looks maybe only stringy hair and snaggleteeth. This gives -2 on reaction rolls. -8 points.",
                     "You look vaguely unappealing, but it's nothing anyone can put a finger on. This gives -1 on reaction rolls. -4 points.",
                     "Your appearance gives you no reaction modifiers either way; you can blend easily into a crowd. A viewer's impression of your looks depends on your behavior. If you smile and act friendly, you will be remembered as pleasant-looking; if you frown and mutter, you will be remembered as unattractive.",
                     "You don't enter beauty contests, but are definitely good-looking. This gives +1 on reaction rolls. 4 points.",
                     "You could enter beauty contests. This gives +4 on reaction rolls made by those attracted to members of your sex, +2 from everyone else. 12 points.",
                     "You could win beauty contests  regularly. This gives +6 on reaction rolls made by those attracted to members of your sex, +2 from others. Exception: Members of the same sex with reason to dislike you (more than -4 in reaction penalties, regardless of bonuses) resent your good looks, and react at -2 instead. As well, talent scouts, friendly drunks, slave traders, and other nuisances are liable to become a problem for you. 16 points",
                     "You are an ideal specimen. This gives +8 (!) on reaction rolls made by those attracted to members of your sex, +2 from others,and all the troublesome side effects of Very Handsome. 20 points"],
                    [-24, -20, -16, -8, -4, 0, 4, 12, 16, 20]]



WEALTH_TABLE = [["Dead Broke", "Poor", "Struggling", "Average", "Comfortable", "Wealthy", "Filthy Rich", "Multimillionaire"],
                ["You have no job, no source of income, no money, and no property other than the clothes you are wearing. Either you are unable to work or there are no jobs to be found. -25",
                 "Your starting wealth is only 1/5 of the average for your society. Some jobs are not available to you, and no job you find pays very well. -15",
                 "Your starting wealth is only 1/2 of the average for your society. Any job is open to you (you can be a Struggling doctor or movie actor), but you don't earn much. This is appropriate if you are, for instance, a 21st-century student. -10 points.",
                 "The default wealth level. 0 points. Comfortable: You work for a living, but your lifestyle is better than most. Your starting wealth is twice the average. 10 points.",
                 "Your starting wealth is five times average; you live very well indeed. 20 points.",
                 "Your starting wealth is 20 times the average. 30 points",
                 "Your starting wealth is 100 times average. You can buy almost anything you want without considering the cost",
                 "Filthy rich doesn't even begin to describe your wealth! For every 25 points you spend beyond the 50 points to be Filthy Rich, increase your starting wealth by another factor of 10: Multimillionaire 1 costs 75 points and gives 1,000 times average starting wealth, Multimillionaire 2 costs 100 points gives 10,000 times starting wealth, and so on. 50 points + 25 points/level of Multimillionaire."],
                [0, .2, .5, 1, 2, 5, 20, 100, 1000],
                [-25, -15, -10, 0, 10, 20, 30, 50, 75]]


STARTING_WEALTH = [250, 500, 750, 1000, 2000, 5000, 10000, 15000, 20000, 30000, 50000, 75000, 100000]
  
DAMAGE_TABLE = [("1d-6","1d-5"),("1d-6","1d-5"),("1d-5","1d-4"),("1d-5","1d-4"),("1d-4","1d-3"), 
                ("1d-4","1d-3"),("1d-3","1d-2"),("1d-3","1d-2"),("1d-2","1d-1"),("1d-2","1d"),
                ("1d-1","1d+1"),("1d-1","1d+2"),("1d","2d-1"),("1d","2d"),("1d+1","2d+1"),
                ("1d+1","2d+2"),("1d+2","3d-1"),("1d+2","3d"),("2d-1","3d+1"),("2d-1","3d+2"),
                ("2d","4d-1"),("2d","4d"),("2d+1","4d+1"),("2d+1","4d+2"),("2d+2","5d-1"), 
                ("2d+1","5d+2")]

SKILL_COST_TABLE = [["PS", "E", "A", "H", "VH"],
                    [1,     0,   -1,  -2,  -3],
                    [2,     1,    0,  -1,  -2],
                    [4,     2,    0,  -1,  -2],
                    [8,     3,    2,   1,   0],
                    [12,    4,    3,   2,   1],
                    [16,    5,    4,   3,   2]]




