import numpy as np
import asyncio
import threading


class Body:

    def __init__(self, mass, radius, x, y, vx, vy, name=None):
        self._mass = mass
        self._radius = radius
        self._position = np.array([x, y])
        self._velocity = np.array([vx, vy])

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity

    def move(self, displacement):
        self._position = self._position + displacement

    def apply_force(self, force):
        self._velocity = self._velocity + force

    def get_mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass

    def get_radius(self):
        return self._radius

    def set_radius(self, radius):
        self._radius = radius


class Simulation:
    def __init__(self, dt=0.01, speed=1, kappa=1):
        self._kappa = kappa  # gravitational constant
        self._dt = dt  # update interval
        self._speed = speed  # simulation speed factor
        self._time = 0  # elapsed time
        self._bodies = []  # list of bodies in simulation
        self._main_body_index = None  # index of the center of simulation
        self._running = False
        self._loop = asyncio.get_event_loop()  # async loop
        self._sim_task = None  # async task
        threading.Thread(daemon=True, target=self._loop.run_forever).start()

    def get_kappa(self):
        return self._kappa

    def get_dt(self):
        return self._dt

    def get_speed(self):
        return self._speed

    def get_time(self):
        return self._time

    def get_bodies(self):
        return self._bodies

    def get_body_count(self):
        return len(self._bodies)

    def get_main_body_index(self):
        return self._main_body_index

    def get_main_body(self) -> Body:
        if self._main_body_index in range(self.get_body_count()):
            return self._bodies[self._main_body_index]
        else:
            return None

    def is_running(self):
        return self._running

    def set_kappa(self, kappa):
        self._kappa = kappa

    def set_dt(self, dt):
        self._dt = dt

    def set_speed(self, speed):
        self._speed = speed

    def reset_timer(self):
        self._time = 0

    def delete_body(self, body_index):
        self._bodies.pop(body_index)
        if body_index == self.get_main_body_index():
            if not self._bodies:
                self.set_main_body(self.get_body_count() - 1)
            else:
                self.set_main_body(None)

    def clear_bodies(self):
        self._bodies = []
        self.set_main_body(None)

    def create_body(self, body: Body):
        self._bodies.append(body)
        if not self.get_main_body():
            self.set_main_body(self.get_body_count() - 1)

    def set_main_body(self, body_index):
        if body_index in range(self.get_body_count()):
            self._main_body_index = body_index
            self.center_main_body()

    def start_sim(self):  # resumes simulation
        if not self.is_running():
            self.reset_timer()
            self._sim_task = asyncio.run_coroutine_threadsafe(self.sim_cor(), self._loop)
            self._running = True

    def stop_sim(self):  # pauses simulation
        if self.is_running():
            self._sim_task.cancel()
            self._running = False

    async def sim_cor(self):
        while True:
            self.step()
            await asyncio.sleep(self._dt)

    def step(self):  # simulates one dt frame
        self._time += self._dt * self._speed
        for body in self._bodies:
            for other in self._bodies:
                if other != body:
                    r = other.get_position() - body.get_position()
                    body.apply_force(
                        self._kappa * self._dt * self._speed * other.get_mass() * r / (np.linalg.norm(r) ** 3))
        for body in self._bodies:
            body.move(self._dt * self._speed * body.get_velocity())
        self.center_main_body()

    def center_main_body(self):
        if self.get_main_body():
            center_displace = self.get_main_body().get_position()
            for body in self._bodies:
                body.move(-center_displace)
