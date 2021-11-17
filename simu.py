import numpy as np
import asyncio
import threading


class Body:
    def __init__(self, mass, radius, x, y, vx, vy):
        self.mass = mass
        self.radius = radius
        self.position = np.array([x, y])
        self.velocity = np.array([vx, vy])

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def move(self, displacement):
        self.position = self.position + displacement

    def apply_force(self, force):
        self.velocity = self.velocity + force

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius


class Simulation:
    def __init__(self, dt=0.01, speed=1):
        self.dt = dt  # update interval
        self.speed = speed  # simulation speed factor
        self.time = 0  # elapsed time
        self.bodies = []  # list of bodies in simulation
        self.main_body_index = None  # index of the center of simulation
        self.running = False
        self.loop = asyncio.get_event_loop()  # async loop
        self.sim_task = None  # async task
        threading.Thread(daemon=True, target=self.loop.run_forever).start()

    def get_dt(self):
        return self.dt

    def get_time(self):
        return self.time

    def get_bodies(self):
        return self.bodies

    def get_main_body_index(self):
        return self.main_body_index

    def get_main_body(self) -> Body:
        if self.main_body_index in range(len(self.bodies)):
            return self.bodies[self.main_body_index]

    def is_running(self):
        return self.running

    def set_dt(self, dt):
        if not self.is_running():
            self.dt = dt

    def reset_timer(self):
        self.time = 0

    def delete_body(self, body_index):
        self.bodies.pop(body_index)
        if body_index == self.get_main_body_index():
            if not self.bodies:
                self.set_main_body(len(self.bodies) - 1)
            else:
                self.set_main_body(None)

    def create_body(self, body: Body):
        self.bodies.append(body)
        if self.get_main_body_index() is None:
            self.set_main_body(len(self.bodies) - 1)

    def set_main_body(self, body_index):
        if body_index in range(len(self.bodies)):
            self.main_body_index = body_index

    def start_sim(self):  # resumes simulation
        if not self.is_running():
            self.reset_timer()
            self.sim_task = asyncio.run_coroutine_threadsafe(self.sim_cor(), self.loop)
            self.running = True

    def stop_sim(self):  # pauses simulation
        if self.is_running():
            self.sim_task.cancel()
            self.running = False

    async def sim_cor(self):
        while True:
            self.step()
            await asyncio.sleep(self.dt)

    def step(self):  # simulates one dt frame
        for body in self.bodies:
            for other in self.bodies:
                if other != body:
                    body.apply_force(self.dt * self.speed * other.get_mass() * (other.get_position() - body.get_position()))
        for body in self.bodies:
            body.move(self.dt * self.speed * body.get_velocity())
        center_displace = self.get_main_body().get_position()
        for body in self.bodies:
            body.move(-center_displace)
