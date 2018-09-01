try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    import Tkinter as tkinter
    from tkinter import *
    from tkinter import messagebox
from typing import List, Dict, Tuple


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
