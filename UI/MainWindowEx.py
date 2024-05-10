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
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Connectors.Connector import Connector

from UI.chartHandle import ChartHandle
from UI.LoginEx import LoginEx
from UI.MainWindow import Ui_MainWindow
from Models.SVM import SVM

import traceback


import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random

class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.SVM = SVM()
        self.LoginEx = LoginEx()
        self.LoginEx.parent = self
        self.chartHandle = ChartHandle()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setupPlot()
        self.actionLogin.triggered.connect(self.openLoginScreen)



    def checkEnableWidget(self, flag=True):
        self.pushButtonPurchaseRatesByGender.setEnabled(flag)
        self.pushButtonPurchaseRatesByAgeGroup.setEnabled(flag)
        self.pushButtonPurchaseCountingByCategory.setEnabled(flag)
        self.pushButtonPurchaseValueByCategory.setEnabled(flag)
        self.pushButtonPurchaseByCategoryAndGender.setEnabled(flag)
        self.pushButtonPaymentMethod.setEnabled(flag)
        self.pushButtonPurchaseRatesByShoppingMall.setEnabled(flag)

        self.pushButtonProductSpendingByGender.setEnabled(flag)
        self.pushButtonPurchaseFrequenceByAge.setEnabled(flag)
        self.pushButtonSalesFluctuationsByMonth.setEnabled(flag)
        self.pushButtonSalesFlucuationsByYearAndMonth.setEnabled(flag)
        if flag == True:
            self.loadTablesName()

    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)

        self.pushButtonFullScreen = QPushButton(self.MainWindow)
        self.pushButtonFullScreen.setText("Full Screen")

        icon = QIcon()
        icon.addPixmap(
            QPixmap("E:\\Elearning\\QT Designer\\MLBAProject\\UI\\../Images/ic_fullscreen.png"),
            QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonFullScreen.setIcon(icon)
        self.pushButtonFullScreen.setIconSize(QSize(16, 16))

        self.toolbar.addWidget(self.pushButtonFullScreen)

        graph_types = ["Line Graph", "Bar Chart", "Scatter Plot"]
        self.graph_type_combobox = QComboBox(self.MainWindow)
        self.graph_type_combobox.addItems(graph_types)
        self.graph_type_combobox.currentIndexChanged.connect(self._on_graph_type_selected)
        self.toolbar.addWidget(self.graph_type_combobox)

        # adding tool bar to the layout
        self.verticalLayoutPlot.addWidget(self.toolbar)
        # adding canvas to the layout
        self.verticalLayoutPlot.addWidget(self.canvas)

    def _on_graph_type_selected(self):
        # Create a new graph based on the selected type from the drop-down menu
        graph_type = self.graph_type_combobox.currentText()
        fig = self.canvas.figure
        n_plots = len(fig.get_axes())

        for ax in fig.get_axes():
            ax.remove()

        # Set the subplot grid to 1 row and 1 column
        n_new_rows, n_new_cols = 1, 1

        if graph_type == "Line Graph":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            new_ax.plot([1, 2, 3], [4, 2, 6], color='blue')  # Set color to blue
            new_ax.set_title('Line Graph')

        elif graph_type == "Bar Chart":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            bars = new_ax.bar(['A', 'B', 'C'], [3, 7, 2],
                              color=['red', 'green', 'blue'])  # Set colors to red, green, and blue
            new_ax.set_title('Bar Chart')

        elif graph_type == "Scatter Plot":
            new_ax = fig.add_subplot(n_new_rows, n_new_cols, 1)
            new_ax.scatter([1, 2, 3], [4, 2, 6], color='orange')  # Set color to orange
            new_ax.set_title('Scatter Plot')

        fig.canvas.draw()

    def show(self):
        super().show()
        self.MainWindow.show()


    def openLoginScreen(self):
            dbwindow = QMainWindow()
            self.LoginEx.setupUi(dbwindow)
            self.LoginEx.show()

    def showDataIntoTableWidget(self, df):
        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            self.tableWidgetStatistic.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for item in df.iloc:
            arr = item.values.tolist()
            self.tableWidgetStatistic.insertRow(row)
            j = 0
            for data in arr:
                self.tableWidgetStatistic.setItem(row, j, QTableWidgetItem(str(data)))
                j = j + 1
            row = row + 1
