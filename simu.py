import numpy as np
import asyncio
import threading


class Body:

    def __init__(self, mass, radius, x, y, vx, vy):
        self._mass = mass
        self._radius = radius
        self._position = np.array([x, y])
        self._velocity = np.array([vx, vy])

    def get_position(self):
        return np.copy(self._position)

    def set_position(self, position):
        self._position = position

    def get_velocity(self):
        return np.copy(self._velocity)

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
    def __init__(self, dt=0.01, speed=1, kappa=1, max_r_log=2):
        self._kappa = kappa  # gravitational constant
        self._dt = dt  # update interval
        self._max_r_log = max_r_log  # maximal body radius log 10
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

    def get_max_r_log(self):
        return self._max_r_log

    def get_max_r(self):
        return 10 ** self._max_r_log

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

    def get_main_body(self):
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
        if body_index in range(self.get_body_count()):
            self._bodies.pop(body_index)
            if self.get_main_body_index() is not None:
                if body_index < self.get_main_body_index():
                    self.set_main_body(self.get_main_body_index() - 1)
                elif body_index == self.get_main_body_index():
                    self.set_main_body(None)

    def clear_bodies(self):
        self._bodies = []
        self.set_main_body(None)

    def create_body(self, body: Body):
        self._bodies.append(body)

    def set_main_body(self, body_index):
        if body_index in range(self.get_body_count()):
            self._main_body_index = body_index
        else:
            self._main_body_index = None
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
        # collisions
        col_done = False
        while not col_done:
            col_done = True
            for body_index, body in enumerate(self._bodies):
                for other_index, other in enumerate(self._bodies):
                    if body_index != other_index:
                        dif_vector = other.get_position() - body.get_position()
                        rsq = sum(dif_vector * dif_vector)
                        if rsq < (body.get_radius() + other.get_radius()) ** 2:
                            self.collide(body_index, other_index)
                            col_done = False
                            break
                if not col_done:
                    break
        # apply forces
        for body in self._bodies:
            for other in self._bodies:
                if other != body:
                    r = other.get_position() - body.get_position()
                    if (r != [0, 0]).all():
                        body.apply_force(
                            self._kappa * self._dt * self._speed * other.get_mass() * r / (np.linalg.norm(r) ** 3))
        # move bodies
        for body in self._bodies:
            body.move(self._dt * self._speed * body.get_velocity())
        self.center_main_body()

    def collide(self, body1_index, body2_index):
        body1 = self._bodies[body1_index]
        body2 = self._bodies[body2_index]
        mass = body1.get_mass() + body2.get_mass()
        radius = min(self.get_max_r(), np.sqrt(body1.get_radius() ** 2 + body2.get_radius() ** 2))
        (x, y) = \
            (body1.get_mass() * body1.get_position() + body2.get_mass() * body2.get_position()) / mass
        (vx, vy) = \
            (body1.get_mass() * body1.get_velocity() + body2.get_mass() * body2.get_velocity()) / mass
        self.delete_body(max(body1_index, body2_index))  # higher index first
        self.delete_body(min(body1_index, body2_index))
        self.create_body(Body(mass, radius, x, y, vx, vy))

    def center_main_body(self):
        if self.get_body_count():
            if self.get_main_body():
                center_displace = self.get_main_body().get_position()
            else:
                center_displace = sum((body.get_mass() * body.get_position() for body in self._bodies)) / \
                                  sum(body.get_mass() for body in self._bodies)
            for body in self._bodies:
                body.move(-center_displace)
