import numpy as np


class Body:
    def __init__(self, mass, radius, x, y):
        self.mass = mass
        self.radius = radius
        self.position = np.array([x, y])


class Simulation:
    def __init__(self, dt=0.01):
        self.dt = dt  # update interval
        self.time = 0  # elapsed time
        self.bodies = []  # list of bodies in simulation
        self.main_body = None  # index of the center of simulation
        self.running = False

    def get_dt(self):
        return self.dt

    def get_time(self):
        return self.time

    def get_bodies(self):
        return self.bodies

    def get_main_body(self):
        return self.main_body

    def is_running(self):
        return self.running

    def set_dt(self, dt):
        self.dt = dt

    def reset_timer(self):
        self.time = 0

    def delete_body(self, body_index):
        self.bodies.pop(body_index)

    def create_body(self, body):
        self.bodies.append(body)

    def set_main_body(self, main_body):
        pass # TODO

    def start_sim(self):  # resumes simulation
        pass # TODO

    def stop_sim(self):  # pauses simulation
        pass # TODO

    def step(self):  # simulates one dt frame
        pass # TODO
