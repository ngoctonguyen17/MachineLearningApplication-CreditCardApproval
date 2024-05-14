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
from UI.chartHandle import ChartHandle
from Models.Statistic import CreditCardStatistics

import traceback
import pandas as pd

class MainWindowEx(Ui_MainWindow):
    def __init__(self, connector=None):
        super().__init__()
        self.connector = Connector()
        self.lasted_df = None
        self.LoginEx = LoginEx()
        self.LoginEx.parent = self
        self.chartHandle = ChartHandle()
        self.Statistic = CreditCardStatistics()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.checkEnableWidget(False)
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.actionLogin.triggered.connect(self.openLoginScreen)

        self.pushButtonDistributionOfTotalGoodDebt.clicked.connect(self.showDistributionOfTotalGoodDebt)
        self.pushButtonDistributionOfTotalIncome.clicked.connect(self.showDistributionOfTotalIncome)
        self.pushButtonDistributionOfApplicantAge.clicked.connect(self.showDistributionOfApplicantAge)
        self.pushButtonDistributionOfYearOfWorking.clicked.connect(self.showDistributionOfYearOfWorking)

    def openLoginScreen(self):
        dbwindow = QMainWindow()
        self.LoginEx.setupUi(dbwindow)
        self.LoginEx.show()

    def show(self):
        self.MainWindow.show()

    def checkEnableWidget(self, flag=True):
        self.pushButtonDistributionOfTotalGoodDebt.setEnabled(flag)
        self.pushButtonDistributionOfTotalIncome.setEnabled(flag)
        self.pushButtonDistributionOfApplicantAge.setEnabled(flag)
        self.pushButtonDistributionOfYearOfWorking.setEnabled(flag)
        self.pushButtonHousingTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonEducationTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonFamilyTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonGenderTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonJobTitleTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonIncomeTypeByStatusOfApproval.setEnabled(flag)
        pass

    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)

        # self.pushButtonFullScreen = QPushButton(self.MainWindow)
        # self.pushButtonFullScreen.setText("Full Screen")
        # icon = QIcon()
        # icon.addPixmap(
        #     QPixmap("E:\\Elearning\\QT Designer\\MLBAProject\\UI\\../Images/ic_fullscreen.png"),
        #     QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # self.pushButtonFullScreen.setIcon(icon)
        # self.pushButtonFullScreen.setIconSize(QSize(16, 16))

        # self.toolbar.addWidget(self.pushButtonFullScreen)

        # graph_types = ["Line Graph", "Bar Chart", "Scatter Plot"]
        # self.graph_type_combobox = QComboBox(self.MainWindow)
        # self.graph_type_combobox.addItems(graph_types)
        # self.graph_type_combobox.currentIndexChanged.connect(self._on_graph_type_selected)
        # self.toolbar.addWidget(self.graph_type_combobox)

        # adding tool bar to the layout
        self.verticalLayoutPlot.addWidget(self.toolbar)
        # adding canvas to the layout
        self.verticalLayoutPlot.addWidget(self.canvas)

    def connectDatabase(self):
            self.connector.server = "localhost"
            self.connector.port = 3306
            self.connector.database = "credit_card"
            self.connector.username = "root"
            self.connector.password = "123456"
            self.connector.connect()

    def showDataIntoTableWidget(self, table, df):
        table.setRowCount(0)
        table.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            table.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for item in df.iloc:
            arr = item.values.tolist()
            table.insertRow(row)
            j = 0
            for data in arr:
                table.setItem(row, j, QTableWidgetItem(str(data)))
                j += 1
            row += 1

    def showDistributionOfTotalGoodDebt(self):
        self.connectDatabase()
        try:
            sql = "SELECT Total_Good_Debt, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Total_Good_Debt;"
            df = self.connector.queryDataset(sql)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df)
        except Exception as e:
            print("Error showing distribution of total good debt:", e)
    def showDistributionOfYearOfWorking(self):
        self.connectDatabase()
        try:
            sql3 = "SELECT Years_of_Working, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Years_of_Working;"
            df3 = self.connector.queryDataset(sql3)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df3)
        except Exception as e:
            print("Error:", e)
    def showDistributionOfApplicantAge(self):
        self.connectDatabase()
        try:
            sql2 = "SELECT Applicant_Age, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Applicant_Age;"
            df2 = self.connector.queryDataset(sql2)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df2)
        except Exception as e:
            print("Error:", e)
    def showDistributionOfTotalIncome(self):
        self.connectDatabase()
        try:
            sql1 = "SELECT Total_Income, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Total_Income;"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Total Income:", e)

