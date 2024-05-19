import random
from random import random
import plotly.graph_objects as go
import pickle
import pyqtgraph as pg

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
        self.pushButtonIncomeTypeByStatusOfApproval.clicked.connect(self.showIncomeTypebyStatus)
        self.pushButtonJobTitleByStatusOfApproval.clicked.connect(self.showJobTitlebyStatus)
        self.pushButtonGenderTypeByStatusOfApproval.clicked.connect(self.showGenderTypebyStatus)
        self.pushButtonEducationTypeByStatusOfApproval.clicked.connect(self.showEducationTypebyStatus)
        self.pushButtonFamilyTypeByStatusOfApproval.clicked.connect(self.showFamilyTypebyStatus)
        self.pushButtonHousingTypeByStatusOfApproval.clicked.connect(self.showHousingTypeByStatus)


    def openLoginScreen(self):
        dbwindow = QMainWindow()
        self.LoginEx.setupUi(dbwindow)
        self.LoginEx.show()

    def show(self):
        self.MainWindow.show()

    def checkEnableWidget(self, flag=True):
        self.pushButtonDistributionOfTotalGoodDebt.setEnabled(flag)
        self.pushButtonDistributionOfTotalIncome.setEnabled(flag)
        self.pushButtonDistributionOfYearOfWorking.setEnabled(flag)
        self.pushButtonDistributionOfApplicantAge.setEnabled(flag)
        self.pushButtonIncomeTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonJobTitleByStatusOfApproval.setEnabled(flag)
        self.pushButtonGenderTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonEducationTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonFamilyTypeByStatusOfApproval.setEnabled(flag)
        self.pushButtonHousingTypeByStatusOfApproval.setEnabled(flag)

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
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Total_Good_Debt, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Total_Good_Debt;"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of total good debt:", e)

        #figure
        plt.figure()
        sns.distplot(df.loc[df["Status"] == 1, 'Total_Good_Debt'], hist=False, label="status 1")
        sns.distplot(df.loc[df["Status"] == 0, 'Total_Good_Debt'], hist=False, label="status 0")
        plt.xlabel('Number of Debt')
        plt.ylabel('Density')
        plt.title('Distribution of Total Good Debt')
        plt.legend()
        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()

    def showDistributionOfYearOfWorking(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Years_of_Working, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Years_of_Working;"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error:", e)

        #figure
        plt.figure()
        sns.distplot(df.loc[df["Status"] == 1, 'Years_of_Working'], hist=False, label="status 1")
        sns.distplot(df.loc[df["Status"] == 0, 'Years_of_Working'], hist=False, label="status 0")
        plt.xlabel('Working Years')
        plt.ylabel('Density')
        plt.title('Distribution of Years of working')
        plt.legend()
        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()


    def showDistributionOfApplicantAge(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Applicant_Age, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Applicant_Age;"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error:", e)

        #figure
        plt.figure()
        sns.distplot(df.loc[df["Status"] == 1, 'Applicant_Age'], hist=False, label="status 1")
        sns.distplot(df.loc[df["Status"] == 0, 'Applicant_Age'], hist=False, label="status 0")
        plt.xlabel('Age')
        plt.ylabel('Density')
        plt.title('Distribution of Applicant Age')
        plt.legend()
        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()

    def showDistributionOfTotalIncome(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Total_Income, \
                    SUM(CASE WHEN Status = 1 THEN 1 ELSE 0 END) AS Status_1_Count,\
                    SUM(CASE WHEN Status = 0 THEN 1 ELSE 0 END) AS Status_0_Count\
                    FROM application_data\
                    GROUP BY Total_Income;"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Total Income:", e)

        #figure
        plt.figure()
        sns.distplot(df.loc[df["Status"] == 1, 'Total_Income'], hist=False, label="status 1")
        sns.distplot(df.loc[df["Status"] == 0, 'Total_Income'], hist=False, label="status 0")
        plt.xlabel('Income')
        plt.ylabel('Density')
        plt.title('Distribution of Total Income')
        plt.legend()
        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()

    def showIncomeTypebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Income_Type, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Income_Type, Status \
                    ORDER BY Status, Income_Type"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Income Type by Status:", e)

        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Income_Type"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Income_Type"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Income Type (Status = 1)")
        ax2.set_title("Income Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Income_Type"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Income Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Income_Type"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Income Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()

    def showJobTitlebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Job_Title, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Job_Title, Status \
                    ORDER BY Status, Job_Title"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Job Title Type by Status:", e)
        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Job_Title"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Job_Title"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Job_Title Type (Status = 1)")
        ax2.set_title("Job_Title Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Job_Title"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Job_Title Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Job_Title"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Job_Title Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())



        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()


    def showGenderTypebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Applicant_Gender, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Applicant_Gender, Status \
                    ORDER BY Status, Applicant_Gender"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Gender Type by Status:", e)

        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Applicant_Gender"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Applicant_Gender"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Gender Type (Status = 1)")
        ax2.set_title("Gender Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Applicant_Gender"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Gender Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Applicant_Gender"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Gender Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())


        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()
    def showEducationTypebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Education_Type, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Education_Type, Status \
                    ORDER BY Status, Education_Type"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Education Type by Status:", e)

        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Education_Type"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Education_Type"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Education_Type (Status = 1)")
        ax2.set_title("Education_Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Education_Type"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Education Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Education_Type"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Education Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())


        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()
    def showFamilyTypebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Family_Status, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Family_Status, Status \
                    ORDER BY Status, Family_Status"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Family Status by Status:", e)

        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Family_Status"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Family_Status"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Family_Status Type (Status = 1)")
        ax2.set_title("Family_Status Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Family_Status"].unique(), loc="center right",
                   bbox_to_anchor=(0.35, 0.001),
                   title="Family_Status Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Family_Status"].unique(), loc="center right",
                   bbox_to_anchor=(0.4, 0.001),
                   title="Family_Status Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()
    def showHousingTypeByStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Housing_Type, Status, COUNT(*) AS Count, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Housing_Type, Status \
                    ORDER BY Status, Housing_Type"
            df1 = self.connector.queryDataset(sql1)
            self.showDataIntoTableWidget(self.tableWidgetStatistic, df1)
        except Exception as e:
            print("Error showing distribution of Housing_Type by Status:", e)

        # figure
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

        df[df["Status"] == 1]["Housing_Type"].value_counts().plot(kind="pie", ax=ax1, autopct='%1.3f%%', labels=None)
        df[df["Status"] == 0]["Housing_Type"].value_counts().plot(kind="pie", ax=ax2, autopct='%1.3f%%', labels=None)

        # Set titles
        ax1.set_title("Housing Type (Status = 1)")
        ax2.set_title("Housing Type (Status = 0)")

        ax1.set_ylabel('')  # Clear ylabel
        ax1.legend(labels=df[df["Status"] == 1]["Housing_Type"].unique(), loc="center right",
                   bbox_to_anchor=(0.35, 0.001),
                   title="Housing_Type (Status = 1)")

        ax2.set_ylabel('')  # Clear ylabel
        ax2.legend(labels=df[df["Status"] == 0]["Housing_Type"].unique(), loc="center right",
                   bbox_to_anchor=(0.4, 0.001),
                   title="Housing_Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())

        # Clear previous widgets in the layout
        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        # Add the canvas to the layout
        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()


