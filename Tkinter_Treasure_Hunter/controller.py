from Tkinter_Treasure_Hunter.model import MyModel
from Tkinter_Treasure_Hunter.view import MyView

try:
    from tkinter import *
    from tkinter import messagebox
except ImportError:
    import Tkinter as tkinter
    from tkinter import *
    from tkinter import messagebox
from typing import List, Dict, Tuple


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
