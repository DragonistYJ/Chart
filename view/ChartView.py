import random

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QCursor
from PyQt5.QtWidgets import QWidget

padding_left = 50
padding_bottom = 30
padding_top = 20
padding_right = 50


class View_Chart(QWidget):
    def __init__(self, line_color, background_color, x_axis_colors, y_axis_colors, tooltip_colors, data):
        super().__init__()
        self.line_color = line_color
        self.background_color = background_color
        self.x_axis_colors = x_axis_colors
        self.y_axis_colors = y_axis_colors
        self.tooltip_colors = tooltip_colors
        self.data = data

        self.x_show_interval = 1
        self.x_plot_interval = 25
        self.x_min = 0
        self.x_max = 0

        self.y_plot_interval = 15
        self.y_max = 32767
        self.y_min = -32768
        self.y_plot_mid = None
        self.y_scatters = []

        self.drag_chart_flag = False
        self.toolTip_index = 0
        self.setMouseTracking(True)

    def paintEvent(self, event) -> None:
        painter = QPainter()
        self.brush_background(painter)
        self.calculate_y_scatters()
        self.draw_xaxis(painter)
        self.draw_yaxis(painter)
        self.draw_points(painter)
        self.draw_xaxis(painter)
        self.show_tool_tip(painter)

    def brush_background(self, painter: QPainter):
        """
        填充背景颜色
        :param painter:
        :return:
        """
        painter.begin(self)
        painter.setPen(QColor(self.background_color))
        painter.setBrush(QColor(self.background_color))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.end()

    def calculate_y_scatters(self):
        """
        计算所有应该显示的y轴坐标的位置
        :return:
        """
        self.y_scatters.clear()
        min_y = padding_top
        max_y = self.size().height() - padding_bottom
        mid_y = (min_y + max_y) // 2

        index = mid_y - self.y_plot_interval
        while index >= min_y:
            self.y_scatters.append(index)
            index -= self.y_plot_interval
        index = mid_y + self.y_plot_interval
        while index <= max_y:
            self.y_scatters.append(index)
            index += self.y_plot_interval
        self.y_scatters.append(mid_y)
        self.y_plot_mid = mid_y
        self.y_scatters.sort()

    def draw_yaxis(self, painter: QPainter):
        pen = QPen(QColor(self.y_axis_colors), 2, Qt.SolidLine)

        # 画y轴
        painter.begin(self)
        painter.setPen(pen)
        painter.drawLine(padding_left, padding_top, padding_left, self.size().height() - padding_bottom)
        painter.end()

        # 画y轴的坐标点
        painter.begin(self)
        painter.setPen(pen)
        for i in range(len(self.y_scatters)):
            # 上半部分
            if self.y_scatters[i] <= self.y_plot_mid:
                number = int((self.y_plot_mid - self.y_scatters[i]) / (self.y_plot_mid - self.y_scatters[0]) * self.y_max)
            # 下半部分
            else:
                ll = len(self.y_scatters) - 1
                number = int((self.y_scatters[i] - self.y_plot_mid) / (self.y_scatters[ll] - self.y_plot_mid) * self.y_min)
            painter.drawText(padding_left - 40, self.y_scatters[i], str(number))
        painter.end()

    def draw_xaxis(self, painter: QPainter):
        pen = QPen(QColor(self.x_axis_colors), 2, Qt.SolidLine)

        painter.begin(self)
        painter.setPen(QColor(self.background_color))
        painter.setBrush(QColor(self.background_color))
        painter.drawRect(10, self.size().height() - padding_bottom, self.width(), padding_bottom)
        painter.end()

        painter.begin(self)
        painter.setPen(pen)
        painter.drawLine(padding_left, self.size().height() - padding_bottom, self.size().width() - padding_right,
                         self.size().height() - padding_bottom)
        painter.end()

        # 画x轴的坐标
        # y_show_interval 每隔多少个点显示一个坐标
        # y_plot_interval 每隔多少像素显示一个坐标
        painter.begin(self)
        painter.setPen(pen)
        x = padding_left
        index = self.x_min
        while x <= self.size().width() - padding_right:
            painter.drawText(x, self.size().height() - padding_bottom + 12, str(index))
            index += self.x_show_interval
            x += self.x_plot_interval
        self.x_max = index - self.x_show_interval
        painter.end()

    def draw_points(self, painter: QPainter):
        if len(self.data) == 0:
            return

        pen = QPen(QColor(self.line_color), 1, Qt.SolidLine)
        painter.begin(self)
        painter.setPen(pen)

        x_plot_len = (self.x_max - self.x_min) // self.x_show_interval * self.x_plot_interval
        last_x = padding_left
        last_y = (self.y_max - self.data[self.x_min]) / (self.y_max - self.y_min) * (
                self.y_scatters[len(self.y_scatters) - 1] - self.y_scatters[0]) + self.y_scatters[0]
        for i in range(self.x_min, min(self.x_max + 1, len(self.data))):
            x = int((i - self.x_min) / (self.x_max - self.x_min) * x_plot_len) + padding_left
            y = (self.y_max - self.data[i]) / (self.y_max - self.y_min) * (
                    self.y_scatters[len(self.y_scatters) - 1] - self.y_scatters[0]) + self.y_scatters[0]
            # painter.drawPoint(x, y)
            painter.drawLine(last_x, last_y, x, y)
            last_x = x
            last_y = y
        painter.end()

    def show_tool_tip(self, painter: QPainter):
        if len(self.data) == 0:
            return
        if self.toolTip_index == 0:
            return

        x = (self.toolTip_index - self.x_min) // self.x_show_interval * self.x_plot_interval + padding_left
        y = int((self.y_max - self.data[self.toolTip_index]) / (self.y_max - self.y_min) * (
                self.y_scatters[len(self.y_scatters) - 1] - self.y_scatters[0]) + self.y_scatters[0])

        painter.begin(self)
        pen = QPen(QColor(self.line_color), 1, Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QColor(self.tooltip_colors))
        painter.drawLine(x, padding_top, x, self.height() - padding_bottom)
        painter.drawRect(x, y, 40, 20)
        painter.drawText(x + 5, y + 15, str(self.data[self.toolTip_index]))
        painter.end()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.LeftButton and e.pos().x() >= padding_left and e.pos().y() <= self.size().height() - padding_bottom:
            self.drag_chart_flag = True
            self.drag_chart_x1 = e.pos().x()
            self.drag_x_min = self.x_min
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        # 拖拽
        if self.drag_chart_flag:
            bias = (self.drag_chart_x1 - e.pos().x()) // self.x_plot_interval * self.x_show_interval  # 移动距离
            self.x_min = bias + self.drag_x_min
            if self.x_min < 0:
                self.x_min = 0
            if self.x_min >= len(self.data):
                self.x_min = len(self.data) - 1
            self.update()
            return

        # 鼠标移动，显示提示
        if self.width() - padding_right >= e.pos().x() >= padding_left and self.size().height() - padding_bottom >= e.pos().y() >= padding_top:
            tooltip_index = (e.pos().x() - padding_left) // self.x_plot_interval * self.x_show_interval + self.x_min
            if self.toolTip_index != tooltip_index and tooltip_index < len(self.data):
                self.toolTip_index = tooltip_index
                self.update()
            return

        self.toolTip_index = 0
        self.update()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.LeftButton and self.drag_chart_flag:
            self.drag_chart_flag = False
            self.setCursor(QCursor(Qt.ArrowCursor))

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        # 鼠标指针位于x轴范围内
        if e.pos().x() >= padding_left and e.pos().y() >= self.size().height() - padding_bottom:
            if e.angleDelta().y() > 0:
                if self.x_show_interval > 1:
                    self.x_show_interval -= 1
                else:
                    self.x_plot_interval += 1
            else:
                if self.x_plot_interval > 25:
                    self.x_plot_interval -= 1
                else:
                    self.x_show_interval += 1

        # 鼠标指针位于y轴范围内
        if e.pos().x() <= padding_left and e.pos().y() <= self.size().height() - padding_bottom:
            interval = random.randint(200, 500)  # 随机增减y轴坐标
            if e.angleDelta().y() > 0:
                self.y_max -= interval
                if self.y_max < 1023:
                    self.y_max = 1023
                self.y_min += interval
                if self.y_min > -1024:
                    self.y_min = -1024
            else:
                self.y_max += interval
                if self.y_max > 32767:
                    self.y_max = 32767
                self.y_min -= interval
                if self.y_min < -32768:
                    self.y_min = -32768

        self.update()
