import ui
import simu
import numpy as np
from math import ceil


def data_to_array(x_res, y_res, zoom):  # converts simulation data to a bitmap
    def in_bounds(x, y):
        nonlocal x_res, y_res
        return 0 <= x < x_res and 0 <= y < y_res

    def render(body: simu.Body):
        nonlocal data
        (x_pos, y_pos) = body.get_position()  # position in simulation
        (x_center, y_center) = (round(x_res / 2 + x_pos / zoom), round(y_res / 2 + y_pos / zoom))  # central pixel
        r = ceil(body.get_radius() / zoom)  # body radius in pixels
        rsq = r * r
        for i in np.arange(-r, r + 1):
            for j in np.arange(-r, r + 1):
                if in_bounds(x_center + i, y_center + j) and i * i + j * j <= rsq:
                    data[y_center + j, x_center + i] = 1

    data = np.zeros((y_res, x_res))
    for body in simulation.get_bodies():
        render(body)
    return data


if __name__ == '__main__':
    x_vis_res = 600
    y_vis_res = 400
    simulation = simu.Simulation(0.01, 1, 10**3)
    display = ui.UI(data_to_array, simulation, 800, 600, x_vis_res, y_vis_res)
    simulation.create_body(simu.Body(1000, 40, 0, 0, 0, 0))
    simulation.create_body(simu.Body(20, 15, 175, 0, 0, -80))
    simulation.create_body(simu.Body(5, 5, 200, 0, 0, -45))
    simulation.start_sim()
    display.run()
