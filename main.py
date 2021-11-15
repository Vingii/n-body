import ui
import simu


def data_to_array(x_res, y_res):  # converts simulation data to a bitmap
    pass  # TODO


if __name__ == '__main__':
    simulation = simu.Simulation(0.01)
    display = ui.UI(data_to_array,800,600,600,400)
    display.run()
