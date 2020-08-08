# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainView.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 638)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget_directory = QtWidgets.QWidget(self.splitter)
        self.widget_directory.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_directory.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget_directory.setObjectName("widget_directory")
        self.verticalLayout_directory = QtWidgets.QVBoxLayout(self.widget_directory)
        self.verticalLayout_directory.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_directory.setObjectName("verticalLayout_directory")
        self.widget_charts = QtWidgets.QWidget(self.splitter)
        self.widget_charts.setObjectName("widget_charts")
        self.verticalLayout_charts = QtWidgets.QVBoxLayout(self.widget_charts)
        self.verticalLayout_charts.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_charts.setObjectName("verticalLayout_charts")
        self.horizontalLayout.addWidget(self.splitter)
        self.horizontalLayout.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew_Workspace = QtWidgets.QAction(MainWindow)
        self.actionNew_Workspace.setObjectName("actionNew_Workspace")
        self.actionClose_Workspace = QtWidgets.QAction(MainWindow)
        self.actionClose_Workspace.setObjectName("actionClose_Workspace")
        self.actionEixt = QtWidgets.QAction(MainWindow)
        self.actionEixt.setObjectName("actionEixt")
        self.actionLoad_Setting = QtWidgets.QAction(MainWindow)
        self.actionLoad_Setting.setObjectName("actionLoad_Setting")
        self.menu.addAction(self.actionNew_Workspace)
        self.menu.addAction(self.actionClose_Workspace)
        self.menu.addSeparator()
        self.menu.addAction(self.actionLoad_Setting)
        self.menu.addSeparator()
        self.menu.addAction(self.actionEixt)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.actionEixt.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "软件构造—Chart"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.actionNew_Workspace.setText(_translate("MainWindow", "打开工作空间"))
        self.actionClose_Workspace.setText(_translate("MainWindow", "关闭工作空间"))
        self.actionEixt.setText(_translate("MainWindow", "退出"))
        self.actionLoad_Setting.setText(_translate("MainWindow", "加载配置文件"))

