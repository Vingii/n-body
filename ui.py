from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import askyesno
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import simu


def fps_to_interval(fps):
    return 1000 / fps


class UI:
    def __init__(self, fps, data_func, simulation: simu.Simulation, x_res, y_res, x_vis_res, y_vis_res):
        self.fps = fps
        self.data_func = lambda zoom: data_func(x_vis_res, y_vis_res, zoom)
        self.simulation = simulation
        # main window
        self.window = Tk()
        self.window.title("N-body")
        self.window.geometry(f"{x_res}x{y_res}")
        self.window.resizable(0, 0)
        # float validation
        vcmd = (self.window.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # simulation frame
        self.sim_frame = Frame(self.window, height=y_vis_res)
        self.sim_frame.pack(side=TOP, fill=BOTH)
        # simulation state
        self.state_frame = Frame(self.sim_frame)
        self.state_frame.pack(side=LEFT, fill=Y)
        self.time_label = Label(self.state_frame, text="Time:", anchor="w")
        self.time_label.grid(row=0, column=0, sticky=(W, E))
        self.time_info = Label(self.state_frame, text=self.simulation.get_time(), anchor="w")
        self.time_info.grid(row=0, column=1, sticky=(W, E))
        self.running_label = Label(self.state_frame, text="Running:", anchor="w")
        self.running_label.grid(row=1, column=0, sticky=(W, E))
        self.running_info = Label(self.state_frame, text=self.simulation.is_running(), anchor="w")
        self.running_info.grid(row=1, column=1, sticky=(W, E))
        self.bodies_label = Label(self.state_frame, text="Body count:", anchor="w")
        self.bodies_label.grid(row=2, column=0, sticky=(W, E))
        self.bodies_info = Label(self.state_frame, text=self.simulation.get_body_count(), anchor="w")
        self.bodies_info.grid(row=2, column=1, sticky=(W, E))
        # simulation visualization
        self.vis_fig = plt.figure()
        self.vis_fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.vis_frame = Frame(self.sim_frame, width=x_vis_res, height=y_vis_res)
        self.vis_frame.pack(side=RIGHT, fill=BOTH)
        self.vis_frame.pack_propagate(False)
        self.vis_canvas = FigureCanvasTkAgg(self.vis_fig, self.vis_frame)
        self.vis_canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)
        # control variables
        self.zoom_var = DoubleVar(value=1)  # simulation distance to visualization distance ratio
        self.speed_var = DoubleVar(value=self.simulation.get_speed())
        self.speed_var.trace_add("write", self.update_speed)
        # controls
        self.control_frame = Frame(self.window)
        self.control_frame.pack(side=BOTTOM, fill=X)
        self.pause_button = Button(self.control_frame, text="Play/Pause", command=self.pause_command)
        self.pause_button.grid(row=0, column=0, rowspan=2, sticky=(S, N))
        self.speed_label = Label(self.control_frame, text="Speed: 1")
        self.speed_label.grid(row=0, column=1)
        self.speed_slider = Scale(self.control_frame, from_=0, to=10, orient="horizontal", variable=self.speed_var,
                                  command=lambda value: self.scale_to_label(value, self.speed_label, "Speed"))
        self.speed_slider.grid(row=1, column=1)
        self.zoom_label = Label(self.control_frame, text="Zoom: 1")
        self.zoom_label.grid(row=0, column=2)
        self.zoom_slider = Scale(self.control_frame, from_=1, to=10, orient="horizontal", variable=self.zoom_var,
                                 command=lambda value: self.scale_to_label(value, self.zoom_label, "Zoom"))
        self.zoom_slider.grid(row=1, column=2)
        self.main_body_label = Label(self.control_frame, text="Main body:")
        self.main_body_label.grid(row=0, column=3)
        self.main_body_spinbox = Spinbox(self.control_frame, from_=0, to=simulation.get_body_count(),
                                         state="readonly", command=self.update_main_body, width=5)
        self.main_body_spinbox.grid(row=1, column=3)
        # add body
        self.masslog_var = DoubleVar(value=1)
        self.radiuslog_var = DoubleVar(value=1)
        self.x_var = DoubleVar(value=0)
        self.y_var = DoubleVar(value=0)
        self.vx_var = DoubleVar(value=0)
        self.vy_var = DoubleVar(value=0)
        self.create_body_button = Button(self.control_frame, text="Create body", command=self.create_body_command)
        self.create_body_button.grid(row=0, column=4, rowspan=2, sticky=(S, N))
        self.mass_label = Label(self.control_frame, text="Mass: 10")
        self.mass_label.grid(row=0, column=5)
        self.mass_slider = Scale(self.control_frame, from_=0, to=3, orient="horizontal", variable=self.masslog_var,
                                 command=lambda value: self.scale_to_label(10 ** float(value), self.mass_label, "Mass"))
        self.mass_slider.grid(row=1, column=5)
        self.mass_slider.config()
        self.radius_label = Label(self.control_frame, text="Radius: 10")
        self.radius_label.grid(row=0, column=6)
        self.radius_slider = Scale(self.control_frame, from_=0, to=2, orient="horizontal", variable=self.radiuslog_var,
                                   command=lambda value: self.scale_to_label(10 ** float(value), self.radius_label,
                                                                             "Radius"))
        self.radius_slider.grid(row=1, column=6)
        self.position_label = Label(self.control_frame, text="Position:")
        self.position_label.grid(row=0, column=7)
        self.x_entry = Entry(self.control_frame, validate="key", validatecommand=vcmd, width=8, textvariable=self.x_var)
        self.x_entry.grid(row=1, column=7)
        self.y_entry = Entry(self.control_frame, validate="key", validatecommand=vcmd, width=8, textvariable=self.y_var)
        self.y_entry.grid(row=2, column=7)
        self.velocity_label = Label(self.control_frame, text="Velocity:")
        self.velocity_label.grid(row=0, column=8)
        self.vx_entry = Entry(self.control_frame, validate="key", validatecommand=vcmd, width=8,
                              textvariable=self.vx_var)
        self.vx_entry.grid(row=1, column=8)
        self.vy_entry = Entry(self.control_frame, validate="key", validatecommand=vcmd, width=8,
                              textvariable=self.vy_var)
        self.vy_entry.grid(row=2, column=8)
        # presets
        self.presets_label = Label(self.control_frame, text="Presets:")
        self.presets_label.grid(row=2, column=0)
        self.clear_preset_button = Button(self.control_frame, text="Clear", command=self.clear_preset_command)
        self.clear_preset_button.grid(row=2, column=1)
        self.solar_system_button = Button(self.control_frame, text="Solar system", command=self.solar_system_command)
        self.solar_system_button.grid(row=2, column=2)
        # animation
        self.im = plt.imshow(self.data_func(self.zoom_var.get()), cmap=plt.get_cmap('Greys'), vmin=0, vmax=1,
                             animated=True)
        plt.axis("off")
        self.ani = animation.FuncAnimation(self.vis_fig, self.ani_step, interval=fps_to_interval(self.fps),
                                           blit=False)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):  # float validation
        if (action == '1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def run(self):
        self.update_data()
        self.window.mainloop()

    def ani_step(self, t):  # sets new frame of visualization
        self.im.set_array(self.data_func(self.zoom_var.get()))
        return self.im,

    def scale_to_label(self, value, label, name):
        label.configure(text=f"{name}: {float(value):.2f}")

    def update_data(self):
        self.time_info.configure(text=f"{self.simulation.get_time():.2f}")
        self.running_info.configure(text=str(self.simulation.is_running()))
        self.bodies_info.configure(text=str(self.simulation.get_body_count()))
        self.main_body_spinbox.configure(to=max(self.simulation.get_body_count() - 1, 0))
        # repeat
        self.window.after(int(fps_to_interval(self.fps)), self.update_data)

    def update_speed(self, *args):
        self.simulation.set_speed(self.speed_var.get())

    def update_main_body(self, *args):
        self.simulation.set_main_body(int(self.main_body_spinbox.get()))

    def pause_command(self):
        if self.simulation.is_running():
            self.simulation.stop_sim()
        else:
            self.simulation.start_sim()

    def create_body_command(self):
        self.simulation.create_body(
            simu.Body(10 ** self.masslog_var.get(), 10 ** self.radiuslog_var.get(), self.x_var.get(), self.y_var.get(),
                      self.vx_var.get(), self.vy_var.get()))

    def preset_decorator(fnc):
        def inner(self):
            if askyesno(title="Confirmation", message="This will delete your simulation."):
                self.simulation.stop_sim()
                self.simulation.clear_bodies()
                fnc(self)

        return inner

    @preset_decorator
    def clear_preset_command(self):
        pass

    @preset_decorator
    def solar_system_command(self):
        self.simulation.create_body(simu.Body(1000, 40, 0, 0, 0, 0))
        self.simulation.create_body(simu.Body(20, 15, 175, 0, 0, -80))
        self.simulation.create_body(simu.Body(5, 5, 200, 0, 0, -46))
