from curses import color_pair

# text created using http://www.patorjk.com/software/taag/ and using font "Rectangles"


exitmsg = r"""
 _____                                               _          _                 
|  _  |___ ___ ___ ___    ___ ___ ___ ___ ___ ___   | |_ ___   | |___ ___ _ _ ___ 
|   __|  _| -_|_ -|_ -|  | -_|_ -|  _| .'| . | -_|  |  _| . |  | | -_| .'| | | -_|
|__|  |_| |___|___|___|  |___|___|___|__,|  _|___|  |_| |___|  |_|___|__,|\_/|___|
                                         |_|                                                                                
"""

intro = r"""
 _ _ _     _                      _          __        _____             ___         _  | |                         
| | | |___| |___ ___ _____ ___   | |_ ___   |  |   ___| __  |___ ___ _ _|  _|___ ___| |_|_|___    ___ ___ _____ ___ 
| | | | -_| |  _| . |     | -_|  |  _| . |  |  |__| -_| __ -| -_| .'| | |  _| . |  _|  _| |_ -|  | . | .'|     | -_|
|_____|___|_|___|___|_|_|_|___|  |_| |___|  |_____|___|_____|___|__,|___|_| |___|_| |_|   |___|  |_  |__,|_|_|_|___|
                                                                                                 |___|              
"""

play = r"""                                                                       
 _____                                           _              _         
|  _  |___ ___ ___ ___    ___ ___ ___ ___ ___   | |_ ___    ___| |___ _ _ 
|   __|  _| -_|_ -|_ -|  |_ -| . | .'|  _| -_|  |  _| . |  | . | | .'| | |
|__|  |_| |___|___|___|  |___|  _|__,|___|___|  |_| |___|  |  _|_|__,|_  |
                             |_|                           |_|       |___|
"""

infos_main_menu = r"""                                                                              
 _____                    _    ___                                 _     ___     
|  _  |___ ___ ___ ___   |_|  |  _|___ ___    _____ ___ ___ ___   |_|___|  _|___ 
|   __|  _| -_|_ -|_ -|  | |  |  _| . |  _|  |     | . |  _| -_|  | |   |  _| . |
|__|  |_| |___|___|___|  |_|  |_| |___|_|    |_|_|_|___|_| |___|  |_|_|_|_| |___|                                                                          
"""


def display_gameover(screen, y, x, color_pair_number):
    #  these function is helpful because curses cant display multiline text at once
    gameover = [r"     _____                  _____ ",
                r"    |   __|___ _____ ___   |     |_ _ ___ ___ ",
                r"    |  |  | .'|     | -_|  |  |  | | | -_|  _|",
                r"    |_____|__,|_|_|_|___|  |_____|\_/|___|_|  ",
                ]
    for ay, line in enumerate(gameover):
        screen.addstr(y + ay, x, line, color_pair(color_pair_number))


space_to_continue = r"""                                                                                      
                                               _                      _   _             
 ___ ___ ___ ___ ___    ___ ___ ___ ___ ___   | |_ ___    ___ ___ ___| |_|_|___ _ _ ___ 
| . |  _| -_|_ -|_ -|  |_ -| . | .'|  _| -_|  |  _| . |  |  _| . |   |  _| |   | | | -_|
|  _|_| |___|___|___|  |___|  _|__,|___|___|  |_| |___|  |___|___|_|_|_| |_|_|_|___|___|
|_|                        |_|                                                          
"""


def display_controls(screen, y, x, color_pair_number):
    controls = [
        r"                      _             _     ",
        r"                     | |           | |    ",
        r"       ___ ___  _ __ | |_ _ __ ___ | |___ ",
        r"      / __/ _ \| '_ \| __| '__/ _ \| / __|",
        r"     | (_| (_) | | | | |_| | | (_) | \__ \ ",
        r"      \___\___/|_| |_|\__|_|  \___/|_|___/",
        " ",
        r"    movement : arrows key",
        r"    quit : escape ",
        r"    return to menu : d",
        r"    pause : p"
        r"    "]

    for ay, line in enumerate(controls):
        screen.addstr(y + ay, x, line, color_pair(color_pair_number))


def display_pause(screen, y, x, color_pair_number):
    pause = [
        r" _____ _____ _____ _____ _____ ____",
        r"|  _  |  _  |  |  |   __|   __|    \ ",
        r"|   __|     |  |  |__   |   __|  |  |",
        r"|__|  |__|__|_____|_____|_____|____/ "
    ]
    for ay, line in enumerate(pause):
        screen.addstr(y + ay, x, line, color_pair(color_pair_number))


def display_info_title(screen, y, x, color_pair_number):
    infos = [
        r" _____                  _     ___",
        r"|   __|___ _____ ___   |_|___|  _|___ ",
        r"|  |  | .'|     | -_|  | |   |  _| . |",
        r"|_____|__,|_|_|_|___|  |_|_|_|_| |___|"]

    for ay, line in enumerate(infos):
        screen.addstr(y + ay, x, line, color_pair(color_pair_number))
