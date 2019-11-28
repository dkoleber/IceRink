import time
import random
from typing import Callable

import pyximport
pyximport.install()
from Engine import Engine, Mass

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
    mass_1 = Mass(8000,2,500,500, 0, 0)
    # mass_1 = Mass(2000,2,500,500, -1, -1)

    engine = Engine()
    engine.add_mass(mass_1)
    # engine.add_mass(Mass(500,5,200,100, 1, -1))

    renderer = Renderer(engine)
    renderer.start()

    frame_time = 1 / FPS

    tests = [
             (2, 2),
             (-1, 1),
             (-1, 2),
             (-1, -1),
             (1, 1),
             (0, 0),
             (1, -1)
             ]


    def step():
        global steps

        engine.step()
        if steps % 60 == 0:
            ind = int((steps / 60) % len(tests))
            # print('-'*10)
            # print(engine.entities)
            new_mass = mass_1.eject(100, 1, random.randint(-2, 2), random.randint(-2, 2))
            # print(f'testing {ind}')
            # new_mass = mass_1.eject(100, 1, tests[ind][0], tests[ind][1])
            if new_mass is not None:
                engine.add_mass(new_mass)
        steps += 1


    while(renderer.is_running):

        run_frame(step, frame_time)



if __name__=='__main__':
    run()