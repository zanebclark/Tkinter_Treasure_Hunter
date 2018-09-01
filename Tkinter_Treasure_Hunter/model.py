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
