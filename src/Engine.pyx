import math
import threading
from typing import List


def angle_between(angle_1, angle_2):
    result = angle_2 - angle_1
    if abs(result) > math.pi:
        result = (math.pi * 2) - result
    return result


r2d = (180./math.pi)

class Mass:
    def __init__(self, amount, density, x, y, v_x = 0, v_y = 0):
        self.amount = amount
        self.density = density
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
    def __str__(self):
        return f'<Mass {self.amount}kg ({str(self.x)[:7]} + {str(self.v_x)[:7]}, {str(self.y)[:7]} + {str(self.v_y)[:7]})>' #@ {self.density}kg/m^2
    def __repr__(self):
        return str(self)
    def get_volume(self):
        return self.amount / self.density
    def get_radius(self):
        return math.sqrt((self.amount / self.density) / math.pi)
    def eject(self, amount, density, v_x, v_y):
        if amount >= self.amount:
            return None
        ratio = amount / self.amount
        result = Mass(amount, density, None, None, v_x, v_y)

        # calculate momentum
        i_m_x = self.amount * self.v_x #initial momentum in x direction
        i_m_y = self.amount * self.v_y #initial momentum in y direction
        self.amount -= amount
        r_m_x = result.amount * v_x #result's momentum in x direction
        r_m_y = result.amount * v_y #result's momentum in y direction
        n_m_x = i_m_x - r_m_x #new momentum in x direction
        n_m_y = i_m_y - r_m_y #new momentum in x direction
        self.v_x = n_m_x / self.amount
        self.v_y = n_m_y / self.amount

        # calculate orientation of new mass relative to this one
        n_angle = (math.atan2(self.v_y, self.v_x) + (math.pi * 2)) % (math.pi * 2)
        r_angle = (math.atan2(result.v_y, result.v_x) + (math.pi * 2)) % (math.pi * 2)
        # diff_angle = r_angle - n_angle
        diff_angle = angle_between(n_angle, r_angle)

        # print(f'init n({n_angle * r2d}) r({r_angle * r2d}) d({diff_angle * r2d})')

        actual_angle = n_angle
        if self.v_x == 0 and self.v_y == 0:
            # print('self not moving')
            actual_angle = r_angle
        elif result.v_x != 0 or result.v_y != 0:  # if the new mass isn't moving, just use this mass' angle
            if abs(diff_angle) > (math.pi / 2): # indicating they're not going the same direction
                # print(f'different directions')
                n_angle += math.pi
                n_angle %= (math.pi * 2)
                # actual_angle = (ratio * r_angle) + ((1 - ratio) * n_angle)
                actual_angle = n_angle + (angle_between(n_angle, r_angle) * (1 - ratio))
                # print(f'n({n_angle * (180/math.pi)}) r({r_angle * (180/math.pi)}) a({actual_angle * (180/math.pi)})')
            elif n_angle == r_angle:
                # if they're going the exact same direction
                # print('exact same directions')
                if result.v_x == self.v_x: # if the new mass is going the same speed, they go side by side
                    actual_angle += (math.pi / 2)
                elif result.v_x < self.v_x: # if it's going slower, it goes in back
                    actual_angle += math.pi
                # otherwise,  the new mass is going faster, so it goes in front which is the default

            else: # indicating they're going the same direction
                # print('same directions')
                # actual_angle = (ratio * r_angle) + ((1 - ratio) * n_angle)
                actual_angle = n_angle + (angle_between(n_angle, r_angle) * (1 - ratio))
                actual_angle += (math.pi / 2)*(diff_angle / abs(diff_angle))

        else:
            # print('other not moving')
            actual_angle += math.pi

        # print(f'a({actual_angle * r2d})')

        distance = result.get_radius() + self.get_radius()
        result.x = self.x + math.cos(actual_angle) * distance
        result.y = self.y + math.sin(actual_angle) * distance



        # calculate center of mass for combination of masses
        com_x = (ratio * result.x) + ((1 - ratio) * self.x)
        com_y = (ratio * result.y) + ((1 - ratio) * self.y)
        shift_x = com_x - self.x
        shift_y = com_y - self.y
        self.x += shift_x
        self.y += shift_y
        result.x += shift_x
        result.y += shift_y

        return result

    def combine(self, other):
        pass

class Engine:
    def __init__(self):
        self.entities:List[Mass] = []
    def step(self):
        for entity in self.entities:
            entity.x += entity.v_x
            entity.y += entity.v_y
    def add_mass(self, mass:Mass):
        self.entities.append(mass)