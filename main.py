from ui import *
from score import Score
from manager import Manager

ui = UI()
score = Score(ui)
manager = Manager(ui, score)
ui.score = score

exit_flag = 0

command_dict = {
    # "exit": lambda: ui.end_game(),
    "score": lambda: ui.show_score()
}

while exit_flag == 0:
    command = input("Input code: ")
    if command in command_dict:
        code = command_dict[command]()
        if code != 0: exit_flag = 1

    else:
        manager.idle(command)
