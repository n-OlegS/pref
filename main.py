from os.path import exists
from ui import *
from score import Score
from manager import Manager

while 1:
    path = input("Enter save path, blank to start a new game: ")
    if not len(path): break
    if exists(path): break

ui = UI()

if len(path):
    score = Score(ui, state=path)
else:
    score = Score(ui)
manager = Manager(ui, score)
ui.score = score

exit_flag = 0

command_dict = {
    # "exit": lambda: ui.end_game(),
    "score": lambda: ui.show_score(),
    "save": lambda: ui.request_save()
}

while exit_flag == 0:
    command = input("Input code: ")
    if command in command_dict:
        code = command_dict[command]()
        if code != 0: exit_flag = 1

    else:
        manager.idle(command)
