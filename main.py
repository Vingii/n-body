import ui
import simu
import numpy as np
from math import ceil


def data_to_array(x_res, y_res, zoom, bodies=None, width=2):  # converts simulation data to a bitmap

    def render_body(body: simu.Body, transparent=0):
        nonlocal data
        (x_pos, y_pos) = body.get_position()  # position in simulation
        (x_center, y_center) = (round(x_res / 2 + x_pos / zoom), round(y_res / 2 + y_pos / zoom))  # central pixel
        r = ceil(body.get_radius() / zoom)  # body radius in pixels
        rsq = r * r
        if min(data.shape[1], y_center + r + 1) - max(y_center - r, 0) > 0 and min(data.shape[0],  # is in view
                                                                                   x_center + r + 1) - max(x_center - r,
                                                                                                           0) > 0:
            ytab, xtab = np.meshgrid(
                np.arange(min(data.shape[1], y_center + r + 1) - max(y_center - r, 0)),
                np.arange(min(data.shape[0], x_center + r + 1) - max(x_center - r, 0)))

            xtab = xtab - min(r, x_center)
            ytab = ytab - min(r, y_center)
            if not transparent:
                data[max(x_center - r, 0):min(data.shape[1], x_center + r + 1),
                max(y_center - r, 0):min(data.shape[0], y_center + r + 1)] = \
                    np.where(abs(xtab * xtab + ytab * ytab) > rsq,
                             data[max(x_center - r, 0):min(data.shape[0], x_center + r + 1),
                             max(y_center - r, 0):min(data.shape[1], y_center + r + 1)], body.get_mass())
            else:
                d = width * r
                data[max(x_center - r, 0):min(data.shape[0], x_center + r + 1),
                max(y_center - r, 0):min(data.shape[1], y_center + r + 1)] = \
                    np.where(abs(xtab * xtab + ytab * ytab - rsq) > d,
                             data[max(x_center - r, 0):min(data.shape[0], x_center + r + 1),
                             max(y_center - r, 0):min(data.shape[1], y_center + r + 1)], body.get_mass())

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
    y_res = 150
    x_vis_res = 600
    y_vis_res = 600
    # simulation parameters

    # test data
    simulation = simu.Simulation(0.01, 1, 10 ** 3)
    # UI setup
    display = ui.UI(fps, data_to_array, simulation, x_res, y_res, x_vis_res, y_vis_res)
    display.run()
