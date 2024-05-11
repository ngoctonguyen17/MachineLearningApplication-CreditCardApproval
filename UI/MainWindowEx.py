import random
from random import random
import plotly.graph_objects as go
import pickle

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QDialog, QComboBox, QPushButton, QCheckBox, \
    QListWidgetItem
from PyQt6.QtWidgets import QMenu, QFileDialog

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Connectors.Connector import Connector

import random

from UI.MainWindow import Ui_MainWindow
from UI.LoginEx import LoginEx

import traceback

class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.LoginEx = LoginEx()
        self.LoginEx.parent = self

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.checkEnableWidget(False)
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.actionLogin.triggered.connect(self.openLoginScreen)

    def openLoginScreen(self):
        dbwindow = QMainWindow()
        self.LoginEx.setupUi(dbwindow)
        self.LoginEx.show()

    def show(self):
        self.MainWindow.show()

    def checkEnableWidget(self, flag=True):
        pass

