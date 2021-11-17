import numpy as np


class Body:
    def __init__(self, mass, radius, x, y):
        self.mass = mass
        self.radius = radius
        self.position = np.array([x, y])

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = np.array([x, y])

    def move(self, dx, dy):
        pass

    def get_mass(self):
        pass

    def set_mass(self, mass):
        pass

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        pass


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

    def create_body(self, body: Body):
        self.bodies.append(body)

    def set_main_body(self, main_body):
        pass

    def start_sim(self):  # resumes simulation
        pass

    def stop_sim(self):  # pauses simulation
        pass

    def step(self):  # simulates one dt frame
        pass
