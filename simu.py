import numpy as np


class Body:
    def __init__(self, m, pos):
        self.mass = 0
        self.position = np.zeros(2)


class Simulation:
    def __init__(self, dt, time=0):
        # parameters
        self.dt = dt  # step frequency
        # state
        self.time = time  # current time
        self.bodies = []  # list of bodies in simulation
        self.main_body = None  # index of the center of simulation
        self.running = False

    def get_state(self):
        pass

    def set_state(self, time=None, bodies=None, main_body=None):
        pass

    def start_sim(self):  # resumes simulation
        pass

    def stop_sim(self):  # pauses simulation
        pass

    def step(self):  # simulates one dt frame
        pass
