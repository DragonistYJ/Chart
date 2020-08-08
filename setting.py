import json
import os
from json import JSONDecodeError


def is_right_color(color: str):
    """
    判断颜色是否是正确的RGB色号
    :param color:
    :return:
    """
    if (not color.startswith("#")) or (len(color) != 7 and len(color) != 9):
        return False
    for c in color[1:]:
        if not ('0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'):
            return False
    return True


class Setting:
    channels = None
    line_colors = []
    background_colors = []
    x_axis_colors = []
    y_axis_colors = []
    tooltip_colors = []

    def __init__(self, setting_path):
        # 首先加载默认选项
        # 如果有异常可以直接退出
        self.load_default_setting()

        # 文件不存在
        if not os.path.exists(setting_path):
            print("Setting", "load", setting_path, "failed", "not exist")
            return

        with open(setting_path) as f:
            json_setting = f.read()
            try:
                json_setting = json.loads(json_setting)
            except JSONDecodeError:
                # 配置文件不是正确的json格式
                print("Setting", "load", setting_path, "failed", "parse json error")
                return

        self.load_channels(json_setting)
        self.load_color(json_setting, self.line_colors, "line_colors", "#000000")
        self.load_color(json_setting, self.background_colors, "background_colors", "#ffffff")
        self.load_color(json_setting, self.x_axis_colors, "x_axis_colors", "#000000")
        self.load_color(json_setting, self.y_axis_colors, "y_axis_colors", "#000000")
        self.load_color(json_setting, self.tooltip_colors, "tooltip_colors", "#8fffffff")

        print("Setting", "load", setting_path, "success")

    def load_default_setting(self):
        """
        加载默认的配置信息
        单信道
        :return:
        """
        self.channels = 1
        self.line_colors.append("#000000")
        self.background_colors.append("#ffffff")
        self.x_axis_colors.append("#000000")
        self.y_axis_colors.append("#000000")
        self.tooltip_colors.append("#8fffffff")

    def load_color(self, setting, color_position: list, color_name: str, default_color: str):
        """
        加载各种部位的颜色
        :param setting: 配置文件
        :param color_position: 颜色数组
        :param color_name: 颜色部位的名字
        :param default_color: 默认颜色
        :return:
        """
        color_position.clear()
        if color_name not in setting:
            for i in range(self.channels):
                color_position.append(default_color)
            return

        for i in range(len(setting[color_name])):
            color = str(setting[color_name][i])
            if is_right_color(color):
                color_position.append(color)
            else:
                color_position.append(default_color)
            if i == self.channels - 1:
                break

        for i in range(self.channels - len(setting[color_name])):
            color_position.append(default_color)

    def load_channels(self, setting):
        """
        加载通道数量，默认为1
        :param setting:
        :return:
        """
        if "channels" not in setting:
            self.channels = 1
            return

        channels = setting["channels"]
        self.channels = channels if 6 >= channels > 0 else 1
