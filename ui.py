from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fps_to_interval(fps):
    return 1000 / fps


class UI:
    def __init__(self, fps, data_func, simulation, x_res, y_res, x_vis_res, y_vis_res):
        self.fps = fps
        self.data_func = lambda zoom: data_func(x_vis_res, y_vis_res, zoom)
        self.simulation = simulation
        self.zoom = 1  # simulation distance to visualization distance ratio
        # main window
        self.window = Tk()
        self.window.title("N-body")
        self.window.geometry(f"{x_res}x{y_res}")
        self.window.resizable(0, 0)
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
        self.update_labels()
        # simulation visualization
        self.vis_fig = plt.figure()
        self.vis_fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.vis_frame = Frame(self.sim_frame, width=x_vis_res, height=y_vis_res)
        self.vis_frame.pack(side=RIGHT, fill=BOTH)
        self.vis_frame.pack_propagate(False)
        self.vis_canvas = FigureCanvasTkAgg(self.vis_fig, self.vis_frame)
        self.vis_canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)
        # animation
        self.im = plt.imshow(self.data_func(self.zoom), cmap=plt.get_cmap('Greys'), vmin=0, vmax=1, animated=True)
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])
        self.ani = animation.FuncAnimation(self.vis_fig, self.ani_step, interval=fps_to_interval(self.fps), blit=False)
        # controls
        # TODO pause, add/remove body, speed, precision, zoom, main body
        self.control_frame = Frame(self.window)
        self.control_frame.pack(side=BOTTOM, fill=X)
        self.pause = Button(self.control_frame, text="Play", command=self.pause_command)
        self.pause.grid(column=0)

    def run(self):
        self.window.mainloop()

    def set_fps(self, fps):
        self.ani.event_source.interval = fps_to_interval(fps)

    def ani_step(self, t):  # sets new frame
        self.im.set_array(self.data_func(self.zoom))
        return self.im,

    def update_labels(self):
        self.time_info.configure(text=f"{self.simulation.get_time():.2f}")
        self.running_info.configure(text=str(self.simulation.is_running()))
        self.bodies_info.configure(text=str(self.simulation.get_body_count()))
        self.window.after(int(fps_to_interval(self.fps)), self.update_labels)

    def pause_command(self):
        if self.simulation.is_running():
            self.simulation.stop_sim()
        else:
            self.simulation.start_sim()
