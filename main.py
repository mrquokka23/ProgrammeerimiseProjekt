from aigame import run, replay_genome
from mainmenu import mainmenu
from playergame import playergame
import os
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")

if __name__ == "__main__":
    while True:
        ret = mainmenu()
        print(ret)
        if ret == "Play":
            playergame()
        if ret[0] == "Train ai":
            run(config_path,ret[1])
        if ret[0] == "Replay":
            replay_genome(ret[1], config_path)


