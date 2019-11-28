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
    default_density = .5


    bounds = (1000, 1000)

    mass_1 = Mass(10000,default_density,500,500, 0, 0)
    # mass_1 = Mass(2000,2,500,500, -1, -1)

    engine = Engine(bounds)
    engine.add_mass(mass_1)
    # engine.add_mass(Mass(500,5,200,100, 1, -1))

    renderer = Renderer(engine, bounds)
    renderer.start()

    frame_time = 1 / FPS

    def step():
        global steps

        engine.step()
        if steps % 60 == 0 and steps < 300:
            for entity in engine.entities:
                new_mass = entity.eject(int(entity.amount / 2), default_density, random.randint(-2, 2), random.randint(-2, 2))

                if new_mass is not None:
                    engine.add_mass(new_mass)
            print(len(engine.entities))
        steps += 1


    while(renderer.is_running):

        run_frame(step, frame_time)



if __name__=='__main__':
    run()