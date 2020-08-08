import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton

from data import read_data
from interact import DirListObj
from setting import Setting
from view.ChartView import View_Chart
from view.ui.MainView_ui import Ui_MainWindow


class ViewMainWindow(QMainWindow, Ui_MainWindow):


    def __init__(self):
        super().__init__()
        self.directory = ''
        self.sizes = []
        self.files = []
        self.chart_views = []
        self.setupUi(self)

        # 打开工作空间按钮
        self.button_load_dir = QPushButton(self.widget_directory)
        self.button_load_dir.setText("打开新的工作空间")
        self.button_load_dir.clicked.connect(self.open_new_directory)
        self.verticalLayout_directory.addWidget(self.button_load_dir)

        # 渲染列表HTML
        self.dir_list_html = QWebEngineView(self.widget_directory)
        self.dir_list_channel = QWebChannel(self.dir_list_html.page())
        self.dir_list_obj = DirListObj()
        self.dir_list_obj.sig_file_item_clicked.connect(self.on_choose_file)
        self.dir_list_channel.registerObject("dir_list_obj", self.dir_list_obj)
        self.dir_list_html.page().setWebChannel(self.dir_list_channel)
        self.dir_list_html.load(QUrl.fromLocalFile(os.path.abspath('view/html/file_list.html')))
        self.verticalLayout_directory.addWidget(self.dir_list_html)
        self.dir_list_html.hide()

        # 打开工作空间按钮与函数绑定
        self.actionNew_Workspace.triggered.connect(self.open_new_directory)

        # 关闭工作空间按钮与函数绑定
        self.actionClose_Workspace.triggered.connect(self.clock_directory)

        # 加载配置文件按钮与函数绑定
        self.actionLoad_Setting.triggered.connect(self.select_setting_file)

        # 加载默认的配置文件
        self.setting = Setting("setting.json")

    def on_choose_file(self, file_id):
        """
        打开一个数据文件
        :param file_id: 文件在内存中的序号
        :return:
        """
        print("try to load", self.files[file_id])
        datas = read_data(os.path.join(self.directory, self.files[file_id]), self.setting.channels)

        # 删除之前存在的图表
        for chart_view in self.chart_views:
            self.verticalLayout_charts.removeWidget(chart_view)
            chart_view.deleteLater()
        self.chart_views.clear()

        # 创建新的图表
        for i in range(self.setting.channels):
            chart_view = View_Chart(self.setting.line_colors[i],
                                    self.setting.background_colors[i],
                                    self.setting.x_axis_colors[i],
                                    self.setting.y_axis_colors[i],
                                    self.setting.tooltip_colors[i],
                                    datas[i])
            self.chart_views.append(chart_view)
            self.verticalLayout_charts.addWidget(chart_view)

    def clock_directory(self):
        """
        关闭当前打开的工作空间
        :return:
        """
        self.dir_list_html.hide()
        self.button_load_dir.show()
        for chart_view in self.chart_views:
            self.verticalLayout_charts.removeWidget(chart_view)
            chart_view.deleteLater()
        self.chart_views.clear()

    def open_new_directory(self):
        """
        打开一个新的目录
        隐藏打开按钮
        显示新的文件列表
        :return:
        """
        self.on_change_directory()
        self.button_load_dir.hide()
        self.dir_list_html.show()

    def on_change_directory(self):
        """
        选择一个新的工作目录
        遍历其中以.data结尾的文件
        显示文件名和大小
        :return:
        """
        self.directory = QFileDialog.getExistingDirectory(self, "选择工作目录")
        if not os.path.exists(self.directory):
            return
        listdir = os.listdir(self.directory)
        self.files.clear()
        self.sizes.clear()
        for _dir in listdir:
            path = os.path.join(self.directory, _dir)
            if os.path.isfile(path) and path.endswith(".data"):
                self.files.append(_dir)
                self.sizes.append(os.path.getsize(path))
        self.dir_list_html.page().runJavaScript("updateList({0},{1})".format(self.files, self.sizes))

    def select_setting_file(self):
        """
        选择配置文件
        :return:
        """
        setting_file = QFileDialog.getOpenFileName(self, "选择配置文件", filter="JSON Files(*.json)")
        self.setting = Setting(setting_file[0])