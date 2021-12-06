import ui
import simu
import numpy as np
from math import ceil


def data_to_array(x_res, y_res, zoom, bodies=None, width=2):  # converts simulation data to a bitmap
    def in_bounds(x, y):
        nonlocal x_res, y_res
        return 0 <= x < x_res and 0 <= y < y_res

    def render_body(body: simu.Body, transparent=0):
        nonlocal data
        (x_pos, y_pos) = body.get_position()  # position in simulation
        (x_center, y_center) = (round(x_res / 2 + x_pos / zoom), round(y_res / 2 + y_pos / zoom))  # central pixel
        r = ceil(body.get_radius() / zoom)  # body radius in pixels
        rsq = r * r
        if not transparent:
            for i in np.arange(max(-r, -x_center), min(r+1, x_res - x_center)):
                for j in np.arange(max(-r, -y_center), min(r+1, y_res - y_center)):
                    if i * i + j * j <= rsq:
                        data[y_center + j, x_center + i] = body.get_mass()
        else:
            d = width * r
            for i in np.arange(max(-r, -x_center), min(r+1, x_res - x_center)):
                for j in np.arange(max(-r, -y_center), min(r+1, y_res - y_center)):
                    if abs(i * i + j * j - rsq) <= d:
                        data[y_center + j, x_center + i] = body.get_mass()

    if bodies is None:
        bodies = []
    data = np.zeros((y_res, x_res))
    for body in simulation.get_bodies():
        render_body(body)
    for body in bodies:
        render_body(body, width)
    return data


if __name__ == '__main__':
    # UI parameters
    fps = 60
    x_res = 800
    y_res = 700
    x_vis_res = 600
    y_vis_res = 600
    # simulation parameters

    # test data
    simulation = simu.Simulation(0.01, 1, 10 ** 3)
    # UI setup
    display = ui.UI(fps, data_to_array, simulation, x_res, y_res, x_vis_res, y_vis_res)
    display.run()
