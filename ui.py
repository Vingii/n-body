from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fps_to_interval(fps):
    return 1000 / fps


class UI:
    def __init__(self, data_func, simulation, x_res, y_res, x_vis_res, y_vis_res):
        self.data_func = lambda zoom: data_func(x_vis_res, y_vis_res, zoom)
        self.simulation = simulation
        self.zoom = 1  # simulation distance to visualization distance ratio
        # main window
        self.window = Tk()
        self.window.title("N-body")
        self.window.geometry(f"{x_res}x{y_res}")
        self.window.resizable(0, 0)
        # simulation frame
        self.sim_frame = Frame(self.window)
        self.sim_frame.pack(side=TOP, fill=BOTH, expand=True)
        # simulation state
        self.state_frame = Frame(self.sim_frame)
        self.state_frame.pack(side=LEFT, fill=Y)
        self.time = Label(self.state_frame, text="t")
        self.time.grid(row=0)
        self.running = Label(self.state_frame, text="running")
        self.running.grid(row=1)
        self.bodies = Label(self.state_frame, text="bodies")
        self.bodies.grid(row=2)
        # simulation visualization
        self.vis_fig = plt.figure()
        self.vis_fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.vis_frame = Frame(self.sim_frame)
        self.vis_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.vis_canvas = FigureCanvasTkAgg(self.vis_fig, self.vis_frame)
        self.vis_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        # animation
        self.im = plt.imshow(self.data_func(self.zoom), cmap=plt.get_cmap('Greys'), vmin=0, vmax=1, animated=True)
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])
        self.ani = animation.FuncAnimation(self.vis_fig, self.ani_step, interval=fps_to_interval(30), blit=False)
        # controls
        self.control_frame = Frame(self.window)
        self.control_frame.pack(side=BOTTOM, fill=X)
        self.pause = Button(self.control_frame, text="play")
        self.pause.grid(column=0)

    def run(self):
        self.window.mainloop()

    def set_fps(self, fps):
        self.ani.event_source.interval = fps_to_interval(fps)

    def ani_step(self, t):  # sets new frame
        self.im.set_array(self.data_func(self.zoom))
        return self.im,
