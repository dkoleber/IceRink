import time
import random
from typing import Callable

import pyximport
pyximport.install()
from Engine import Engine, Mass, RandomAgent

from Renderer import Renderer

FPS = 20

steps = 0

def run_frame(function: Callable, frame_time:float):
    start_time = time.time()
    function()
    duration = time.time() - start_time
    sleep_time = max(0, frame_time-duration)
    if(sleep_time > 0):
        time.sleep(sleep_time)


def run():
    bounds = (1000, 1000)
    engine = Engine(bounds)

    # mass_1 = Mass(100000,1,500,500, 0, 0)
    # engine.add_mass(mass_1)

    agent_1 = RandomAgent(100000, 1, 500, 500)
    engine.add_mass(agent_1)

    renderer = Renderer(engine, bounds)
    renderer.start()



    def step():
        global steps
        engine.step()
        steps += 1

    frame_time = 1 / FPS
    while(renderer.is_running):

        run_frame(step, frame_time)



if __name__=='__main__':
    run()