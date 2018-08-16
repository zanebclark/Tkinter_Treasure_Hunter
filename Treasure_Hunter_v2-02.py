try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    import Tkinter as tkinter
    from tkinter import *
    from tkinter import messagebox
from random import randint
from math import sqrt
from typing import List, Dict, Tuple


# Application flow
# app.py, calls a controller
# controller loads model
# controller loads view
# app.py enters mainloop
# app.py exits mainloop
# app.py asks controllers to stop
# controller asks view to stop
# While in the main loop
#
# view receives user input
# view calls controller
# controller handles input - acts on model
# controller handles update - acts on view

#
# A A Model-View-Controller framework for TKinter.
# Model: Data Structure. Controller can send messages to it, and model can respond to message.
# View : User interface elements. Controller can send messages to it. View can call methods from Controller when an event happens.
# Controller: Ties View and Model together. turns UI responses into changes in data and vice versa.

#
# Controller: Ties View and Model together.
#       --Performs actions based on View events.
#       --Sends messages to Model and View and gets responses
#       --Has Delegates
#       --Controllers may talk to other controllers through delegates
# initialize properties in view, if any
# initalize properties in model, if any
# event handlers -- add functions called by command attribute in view
# delegates -- add functions called by delegtes in model or view

# View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
# make the view
# set the delegate/callback pointer
# control variables go here. Make getters and setters for them below
# load the widgets
# Getters and setters for the control variables.
# returns a string of the entry text
# sets the entry text given a string


# Model: Data Structure.
#   --Controller can send messages to it, and model can respond to message.
#   --Uses delegates from vc to send messages to the Controller of internal change
#   --NEVER communicates with View
#   --Has setters and getters to communicate with Controller
# set delegate/callback pointer
# initialize model
# Delegate goes here. Model would call this on internal change
# Setters and getters for the model
# delegate called on change
# Any internal processing for the model

class MyController(object):
    def __init__(self):
        self.model = MyModel(self)
        self.view = MyView(self)
        self.view.load_view()
        self.model.second_configure()

    def get_window_dims(self) -> Tuple[int, int]:
        # print("Getting window dimensions...")
        return self.model.window_dims

    def get_diff_levels(self) -> List[int]:
        lst = list(self.model.lvls.keys())
        return lst

    def get_diff_setting(self):
        return self.model.diff_setting_model

    def update_diff(self):
        val = self.view.diff_setting_view
        # print("Updating Difficulty to {0}".format(val))
        self.model.diff_setting_model = val
        self.view.change_window_dims(self.model.window_dims)

    def clicking_cont(self, tpl: Tuple[int, int]):
        info = self.model.clicking_model(tpl)
        return info

    def winning_cont(self):
        self.view.winning_view()

    def get_canvas_dims(self) -> Tuple[int, int]:
        tpl = (self.view.canvas.winfo_width(), self.view.canvas.winfo_height())
        return tpl

    def resize_cont(self, tpl: Tuple[int, int]):
        # print("resize cont")
        # print(tpl)
        self.model.resize_model(tpl)

    def get_click_info(self):
        return self.model.click_info

    def clicks_shown(self):
        self.model.click_shown = True

    def increase_search_radius_cont(self):
        self.model.search_radius += 5

    def new_game(self):
        # print("New Game!")
        self.view.root.destroy()
        del self.model
        self.__init__()

    def display(self):
        self.view.root.mainloop()


class MyView(object):
    def __init__(self, vc):
        self.vc = vc
        self.root = Tk()
        self.__diff_setting_view = IntVar()
        self.__diff_setting_view.set(self.vc.get_diff_setting())
        self.__window_offset = None
        self.__diff_sel = IntVar()
        self.title = "Find the treasure!"
        self.icon_name = "favicon.ico"
        self.__click_count = IntVar()
        self.__click_x = IntVar()
        self.__click_y = IntVar()
        self.__distance_view = IntVar()
        self.__search_radius = IntVar()
        self.__draw_boolean = BooleanVar()
        self.__draw_boolean.set(False)
        self.frame_instr = Frame(self.root)
        self.diff_label = Label(self.frame_instr)
        self.diff_setter = OptionMenu(self.frame_instr, self.__diff_setting_view, *self.vc.get_diff_levels(),
                                      command=self.diff_change)
        self.instr = Label(self.frame_instr)
        self.frame_canvas = Frame(self.root)
        self.canvas = Canvas(self.frame_canvas)
        self.frame_hud = Frame(self.root)
        self.clicks_x_coord_label = Label(self.frame_hud)
        self.clicks_x_coord_disp = Label(self.frame_hud)
        self.clicks_y_coord_label = Label(self.frame_hud)
        self.clicks_y_coord_disp = Label(self.frame_hud)
        self.clicks_label = Label(self.frame_hud)
        self.click_disp = Label(self.frame_hud)
        self.distance_label = Label(self.frame_hud)
        self.distance_disp = Label(self.frame_hud)
        self.show_clicks_btn = Button(self.frame_hud)
        self.increase_radius_btn = Button(self.frame_hud)
        self.new_game_bnt = Button(self.frame_hud)
        self.canvas_list = []

    def load_view(self):
        self.root.resizable(False, False)
        window = self.vc.get_window_dims()
        # print(window)
        screen = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        center = []

        for i in range(0, 2):
            # print(i)
            i = int(round((screen[i] / 2) - (window[i] / 2)))
            # print(i)
            center.append(i)

        # print("{0}x{1}+{2}+{3}".format(window[0], window[1], center[0], center[1]))
        self.root.geometry("{0}x{1}+{2}+{3}".format(window[0], window[1], center[0], center[1]))
        self.root.title(self.title)
        self.root.iconbitmap(self.icon_name)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.frame_instr.config(borderwidth=5, relief=RAISED)
        self.frame_instr.grid(row=0, column=0, sticky=N + S + E + W)
        self.frame_instr.rowconfigure(0, weight=1)
        self.frame_instr.columnconfigure(1, weight=1)

        self.diff_label.config(text="Difficulty:")
        self.diff_label.grid(row=0, column=0, sticky=N + W)
        self.diff_setter.grid(row=1, column=0, sticky=N + W)

        self.instr.config(text="These are the instructions...", padx=5, pady=5)
        self.instr.grid(row=0, column=1, sticky=N + W + E, rowspan=2)

        self.frame_canvas.config(borderwidth=5, relief=SUNKEN)

        self.frame_canvas.grid(row=1, column=0, sticky=N + S + E + W)
        self.frame_canvas.rowconfigure(0, weight=1)
        self.frame_canvas.columnconfigure(0, weight=1)
        self.canvas.config(background="#baa86f")
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.canvas.bind("<ButtonPress-1>", self.clicking_view)
        self.canvas.bind("<Configure>", self.resize_view)

        self.frame_hud.config(borderwidth=5, relief=RAISED)
        self.frame_hud.grid(row=2, column=0, sticky=N + S + E + W)

        self.clicks_x_coord_label.config(text="Click X Coord")
        self.clicks_x_coord_label.grid(row=0, column=0)
        self.clicks_x_coord_disp.config(textvariable=self.__click_x)
        self.clicks_x_coord_disp.grid(row=1, column=0)

        self.clicks_y_coord_label.config(text="Click Y Coord")
        self.clicks_y_coord_label.grid(row=0, column=1)
        self.clicks_y_coord_disp.config(textvariable=self.__click_y)
        self.clicks_y_coord_disp.grid(row=1, column=1)

        self.clicks_label.config(text="Number of Clicks")
        self.clicks_label.grid(row=0, column=2)
        self.click_disp.config(textvariable=self.__click_count)
        self.click_disp.grid(row=1, column=2)

        self.distance_label.config(text="Distance from Treasure")
        self.distance_label.grid(row=0, column=3)
        self.distance_disp.config(textvariable=self.__distance_view)
        self.distance_disp.grid(row=1, column=3)

        self.frame_hud.columnconfigure(4, weight=1)
        self.show_clicks_btn.config(text="Track Clicks", command=self.canvas_handler)
        self.show_clicks_btn.grid(row=1, column=4, sticky=S + E)

        self.increase_radius_btn.config(text="Increase Winning Radius", command=self.increase_search_radius_view)
        self.increase_radius_btn.grid(row=0, column=4, sticky=N + E)

        # TODO: This button should pack upon the game's conclusion and have a "new game" function
        self.new_game_bnt.config(text="New Game?", command=None)

    def change_window_dims(self, tpl: Tuple[int, int]):
        self.root.geometry("{0}x{1}".format(*tpl))

    def clicking_view(self, event):
        tpl = (event.x, event.y)
        info = self.vc.clicking_cont(tpl)
        self.click_count = info["clickcount"]
        self.click_x = info["click_x"]
        self.click_y = info["click_y"]
        self.distance_view = info["distance"]
        self.erase_guesses()
        if self.__draw_boolean.get():
            self.draw_guesses()

    def resize_view(self, event):
        # print("resize view")
        tpl = (event.width, event.height)
        self.__click_count.set(None)
        self.__click_x.set(None)
        self.__click_y.set(None)
        self.__distance_view.set(None)
        self.__draw_boolean.set(False)
        self.canvas_handler()
        self.canvas_handler()
        self.canvas_list = []

        # print(tpl)

        self.vc.resize_cont(tpl)

    # region click_count ###############################################################################################
    @property
    def click_count(self) -> int:
        return self.__click_count.get()

    @click_count.setter
    def click_count(self, value: int):
        if isinstance(value, int):
            self.__click_count.set(value)
        else:
            print("click_count not integer: " + str(type(value)))

    # endregion ########################################################################################################

    # region click_x ###########################################################################################
    @property
    def click_x(self) -> int:
        return self.__click_x.get()

    @click_x.setter
    def click_x(self, value: int):
        if isinstance(value, int):
            self.__click_x.set(value)
        else:
            print("click_x not integer: " + str(type(value)))

    # endregion ########################################################################################################

    # region click_y ###########################################################################################
    @property
    def click_y(self) -> int:
        return self.__click_y.get()

    @click_y.setter
    def click_y(self, value: int):
        if isinstance(value, int):
            self.__click_y.set(value)
        else:
            print("click_y not integer: " + str(type(value)))

    # endregion ########################################################################################################

    # region distance_view ###########################################################################################
    @property
    def distance_view(self) -> int:
        return self.__distance_view.get()

    @distance_view.setter
    def distance_view(self, val: int):
        if isinstance(val, int):
            self.__distance_view.set(val)
        else:
            print("distance_view not integer: " + str(type(val)))

    # endregion ########################################################################################################

    # region draw_boolean ###########################################################################################
    @property
    def draw_boolean(self) -> int:
        return self.__draw_boolean.get()

    @draw_boolean.setter
    def draw_boolean(self, value: int):
        if isinstance(value, int):
            self.__draw_boolean.set(value)
        else:
            print("draw_boolean not integer: " + str(type(value)))

    # endregion ########################################################################################################

    # region search_radius ###########################################################################################
    @property
    def search_radius(self) -> int:
        return self.__search_radius.get()

    @search_radius.setter
    def search_radius(self, value: int):
        if isinstance(value, int):
            self.__search_radius.set(value)
        else:
            print("search_radius not integer: " + str(type(value)))

    # endregion ########################################################################################################

    def diff_change(self, _):
        self.vc.update_diff()

    # region diff_setting_view #########################################################################################
    @property
    def diff_setting_view(self) -> int:
        return self.__diff_setting_view.get()

    @diff_setting_view.setter
    def diff_setting_view(self, value: bool):
        if isinstance(value, int):
            self.__diff_setting_view.set(value)
        else:
            print("diff_setting_view not integer: " + str(type(value)))

    # endregion ########################################################################################################

    def winning_view(self):
        self.canvas.delete("all")
        self.canvas.config(bg="#D3D3D3")
        # self.diff_setter.destroy()
        self.canvas.bind("<ButtonPress-1>", "")
        new_game_bnt = Button(self.frame_hud, text="New Game?", command=self.vc.new_game)
        new_game_bnt.grid(row=0, column=0, rowspan=2, columnspan=5, sticky=N + S + E + W)

    def draw_guesses(self):
        clicks = self.vc.get_click_info()
        for (order, (x_coord, y_coord, dist, rad)) in clicks.items():
            circle = self.canvas.create_oval(
                (x_coord - rad),
                (y_coord - rad),
                (x_coord + rad),
                (y_coord + rad),
                fill=self.fill_gradient(dist)
            )
            self.canvas_list.append(circle)
            self.fill_gradient(1)

    def erase_guesses(self):
        self.canvas.delete("all")

    def canvas_handler(self):
        # print("Canvas Handler Called, draw boolean: {}".format(self.__draw_boolean.get()))
        if self.__draw_boolean.get():
            self.__draw_boolean.set(False)
            self.erase_guesses()
            self.show_clicks_btn.config(text="Track Clicks")
        elif not self.__draw_boolean.get():
            self.draw_guesses()
            self.__draw_boolean.set(True)
            self.vc.clicks_shown()
            self.show_clicks_btn.config(text="Hide Clicks")
        # print("Canvas Handler Ended, draw boolean: {}".format(self.__draw_boolean.get()))

    def fill_gradient(self, distance) -> str:
        clicks = self.vc.get_click_info()
        min_dist = 1000000
        max_dist = 0
        for _, _, dist, _ in clicks.values():
            if dist > max_dist:
                max_dist = dist
            if dist < min_dist:
                min_dist = dist
        # print("Min Dist: " + str(min_dist))
        # print("Max Dist: " + str(max_dist))

        rng = max_dist - min_dist
        if rng != 0:
            quant = rng / 98
            hue = (int(round((distance - min_dist) / quant))) + 1
        else:
            hue = 1
        # print('grey{0}'.format(str(hue)))
        return 'grey{0}'.format(str(hue))

    def increase_search_radius_view(self):
        self.vc.increase_search_radius_cont()


class MyModel(object):
    def __init__(self, vc):
        self.vc = vc
        self.game_status = None
        self.lvls = {
            1: (500, 200),
            2: (700, 280),
            3: (900, 360),
            4: (1100, 400),
            5: (1300, 520),
            6: (1500, 600),
            7: (1700, 680),
        }
        self.diff_setting_model = 5
        self.window_dims = self.lvls[self.diff_setting_model]
        self.target_coords = (0, 0)
        self.search_radius = 5
        self.click_info = {}
        self.click_shown = False

    def second_configure(self):
        pass
        # self.target_coords = self.vc.get_canvas_dims()

    # region Search Radius##############################################################################################
    @property
    def search_radius(self) -> int:
        return self.__search_radius

    @search_radius.setter
    def search_radius(self, value: int):
        self.__search_radius = value

    # endregion ########################################################################################################

    # region Game Status ###############################################################################################
    @property
    def game_status(self):
        return self.__game_status

    @game_status.setter
    def game_status(self, value):
        self.__game_status = value

    # endregion ########################################################################################################

    # region Target Coordinates ########################################################################################
    @property
    def target_coords(self) -> Tuple[int, int]:
        return self.__target_coords

    @target_coords.setter
    def target_coords(self, tpl: Tuple[int, int]):
        # print("Target Coord Setter Acccessed")
        # print(tpl)
        t_coords = (randint(0, tpl[0]), randint(0, tpl[1]))
        print(t_coords)
        self.__target_coords = t_coords

    # endregion ########################################################################################################

    # region Difficulty ################################################################################################
    @property
    def diff_setting_model(self) -> int:
        return self.__diff_setting_model

    @diff_setting_model.setter
    def diff_setting_model(self, value: int):
        # print("diff_setting_model setter accessed")
        if isinstance(value, int):
            self.__diff_setting_model = value
            self.window_dims = 0
            # print("New Difficulty: " + str(self.__diff_setting_model))
        else:
            print("Difficulty not integer: " + str(type(value)))

    # endregion ########################################################################################################

    # region Window Dimensions #########################################################################################
    @property
    def window_dims(self) -> Tuple[int, int]:
        return self.__window_dims

    @window_dims.setter
    def window_dims(self, _):
        # print("window_dims setter accessed")

        # fetch the current level's width and height from the model's levels
        width, height = self.lvls[self.diff_setting_model]
        tpl = (width, height)
        # print(tpl)

        # Check typing
        error = False
        for _ in tpl:
            if not isinstance(_, int):
                error = True

        # If the values check out, set the window dimensions equal to the tuple
        if not error:
            self.__window_dims = (tpl[0], tpl[1])
            # print("New window dimensions: {0}X{1}".format(*tpl))
        else:
            print("tpl value error: ({0}, {1})".format(type(tpl[0]), type(tpl[1])))

    # endregion ########################################################################################################

    def distance(self, coords: Tuple[int, int]) -> int:
        return int(
            round(
                sqrt(
                    (
                        abs(self.target_coords[0] - coords[0])
                    ) ** 2
                    +
                    (
                        abs(self.target_coords[1] - coords[1])
                    ) ** 2
                )
            )
        )

    def clicking_model(self, click_coords: Tuple[int, int]) -> Dict[str, int]:
        tpl = (
            click_coords[0],
            click_coords[1],
            self.distance(click_coords),
            self.search_radius
        )

        self.click_info[(self.click_count() + 1)] = tpl

        info = dict(
            clickcount=self.click_count(),
            click_x=self.click_info[self.click_count()][0],
            click_y=self.click_info[self.click_count()][1],
            distance=self.click_info[self.click_count()][2]
        )

        if info["distance"] < self.search_radius:
            self.winning_model()
        return info

    def click_count(self) -> int:
        curr_count = 0
        for i in list(self.click_info.keys()):
            if i > curr_count:
                curr_count = i
        return curr_count

    def curr_s_radius_clicks(self):
        s_rad_count = 0
        for _, _, _, s_radius in self.click_info.values():
            if s_radius == self.search_radius:
                s_rad_count += 1
        return s_rad_count

    def winning_model(self):
        self.vc.winning_cont()

    def resize_model(self, tpl: Tuple[int, int]):
        # print("resize model")
        # print(tpl)
        self.target_coords = tpl
        self.click_info = {}
        self.click_shown = False
        self.search_radius = 5



def main():
    app = MyController()
    app.display()


if __name__ == '__main__':
    main()
