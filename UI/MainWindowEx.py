import random
from random import random
import plotly.graph_objects as go
import pickle
import pyqtgraph as pg

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QDialog, QComboBox, QPushButton, QCheckBox, QListWidgetItem
from PyQt6.QtWidgets import QMenu, QFileDialog

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Connectors.Connector import Connector

from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, accuracy_score, confusion_matrix, precision_score, recall_score


import random

from UI.MainWindow import Ui_MainWindow
from UI.LoginEx import LoginEx
from UI.chartHandle import ChartHandle
from Models.Statistic import CreditCardStatistics
from Utils import FileUtil

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

        self.model_info = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.checkEnableWidget(False)
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.actionLogin.triggered.connect(self.openLoginScreen)
        # self.actionSave_Model.triggered.connect(self.saveModel)

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

        self.pushButtonViewData.clicked.connect(self.loadDataIntoTable)
        self.pushButtonTrain.clicked.connect(self.TrainModel)
        self.pushButtonEvaluate.clicked.connect(self.EvaluateModel)
        self.pushButtonPredict.clicked.connect(self.Prediction)

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
        self.pushButtonViewData.setEnabled(flag)
        self.pushButtonTrain.setEnabled(flag)
        self.pushButtonEvaluate.setEnabled(flag)
        self.pushButtonPredict.setEnabled(flag)


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
            sql1 = "SELECT Income_Type, Status, COUNT(*) AS Count, \
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
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


        ax1.set_title("Income Type (Status = 1)")
        ax2.set_title("Income Type (Status = 0)")

        ax1.set_ylabel('')
        ax1.legend(labels=df[df["Status"] == 1]["Income_Type"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Income Type (Status = 1)")

        ax2.set_ylabel('')
        ax2.legend(labels=df[df["Status"] == 0]["Income_Type"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Income Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())

        for i in reversed(range(self.verticalLayoutPlot.count())):
            self.verticalLayoutPlot.itemAt(i).widget().setParent(None)

        self.verticalLayoutPlot.addWidget(canvas)
        canvas.draw()
    def showJobTitlebyStatus(self):
        self.connectDatabase()
        try:
            sql = "SELECT * FROM application_data"
            df = self.connector.queryDataset(sql)
            sql1 = "SELECT Job_Title, Status, COUNT(*) AS Count, \
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
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

        ax1.set_ylabel('')
        ax1.legend(labels=df[df["Status"] == 1]["Job_Title"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Job_Title Type (Status = 1)")

        ax2.set_ylabel('')
        ax2.legend(labels=df[df["Status"] == 0]["Job_Title"].unique(), loc="center right", bbox_to_anchor=(0.4, 0.001),
                   title="Job_Title Type (Status = 0)")

        canvas = FigureCanvas(plt.gcf())


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
            sql1 = "SELECT Applicant_Gender, Status, COUNT(*) AS Count, \
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
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

        ax1.set_ylabel('')
        ax1.legend(labels=df[df["Status"] == 1]["Applicant_Gender"].unique(), loc="center right", bbox_to_anchor=(0.35, 0.001),
                   title="Gender Type (Status = 1)")

        ax2.set_ylabel('')
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
            sql1 = "SELECT Education_Type, Status, COUNT(*) AS Count, \
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
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
            sql1 = "SELECT Family_Status, Status, COUNT(*) AS Count, \
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
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
            sql1 = ("SELECT Housing_Type, Status, COUNT(*) AS Count, " \
                    "COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Status) AS Ratio \
                    FROM application_data \
                    GROUP BY Housing_Type, Status \
                    ORDER BY Status, Housing_Type")
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

    def loadDataIntoTable(self):
        self.connectDatabase()
        selected_Dataset = self.comboBoxDataset.currentText()

        if selected_Dataset == "Applicant Data":
            sql = "SELECT * FROM credit_card.application_data;"
        else:
            return
        df = self.connector.queryDataset(sql)
        self.showDataIntoTableWidget(self.tableWidgetData, df)

    def TrainModel(self):
        # Load data
        sql = "SELECT * FROM application_data"
        df = self.connector.queryDataset(sql)

        self.showDataIntoTableWidget(self.tableWidgetData, df)

        # Define features
        categorical_feature = ['Applicant_Gender', 'Owned_Car', 'Owned_Realty',
                               'Income_Type', 'Education_Type', 'Family_Status',
                               'Housing_Type', 'Owned_Mobile_Phone', 'Owned_Work_Phone',
                               'Total_Bad_Debt', 'Owned_Phone', 'Owned_Email',
                               'Job_Title']
        numerical_feature = ['Total_Children', 'Total_Income', 'Total_Family_Members',
                             'Applicant_Age', 'Years_of_Working', 'Total_Bad_Debt',
                             'Total_Good_Debt']

        # Select relevant columns
        self.df_selected = df.loc[:, ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
                                      'Owned_Realty', 'Owned_Phone', 'Total_Children',
                                      'Total_Family_Members', 'Total_Income', 'Years_of_Working',
                                      'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
                                      'Education_Type', 'Applicant_Gender']]

        # Map 'Education_Type' to numerical values
        self.df_selected['Education_Type'] = self.df_selected['Education_Type'].str.strip()
        scale_mapper = {'Lower secondary': 0, 'Secondary / secondary special': 1,
                        'Incomplete higher': 2, 'Higher education': 3, 'Academic degree': 4}
        self.df_selected['Education_Type'] = self.df_selected['Education_Type'].replace(scale_mapper)

        if 'Income_Type_Working' in self.df_selected.columns:
            self.df_selected['Income_Type_Working'] = self.df_selected['Income_Type_Working'].replace(
                {True: 1, False: 0})

        # Create dummy variables
        Applicant_Gender_dummies = pd.get_dummies(self.df_selected['Applicant_Gender'], prefix='Applicant_Gender')
        Income_Type_dummies = pd.get_dummies(self.df_selected['Income_Type'], prefix='Income_Type')

        # Concatenate dummies and drop original columns
        self.df_selected = pd.concat([self.df_selected, Applicant_Gender_dummies, Income_Type_dummies], axis=1)
        self.df_selected.drop(['Applicant_Gender', 'Income_Type'], axis=1, inplace=True)

        # Split data into x and y
        self.y = self.df_selected['Status'].values
        self.x = self.df_selected.drop(['Status', 'Applicant_ID'], axis=1).values

        # Standardize data
        sc = StandardScaler()
        self.x = sc.fit_transform(self.x)

        # Get test_size and random_state from input
        self.test_size = float(self.lineEditTestSize.text()) / 100
        self.random_state = int(self.lineEditRandomState.text())

        # Split data into training and test sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=self.test_size, random_state=self.random_state)

        # Apply SMOTE to training data
        smote = SMOTE(random_state=242)
        self.x_train_smote, self.y_train_smote = smote.fit_resample(self.x_train, self.y_train)

        # Train SVM model
        self.svm = LinearSVC(max_iter=1000, dual=False)  # dual=False để tránh cảnh báo FutureWarning
        self.model = self.svm.fit(self.x_train_smote, self.y_train_smote)

        QMessageBox.information(None, "Notification", "Model training has been completed.")


    def EvaluateModel(self):
        # Make predictions
        self.y_pred = self.svm.predict(self.x_test)

        # Evaluate model
        log_accuracy = round(accuracy_score(self.y_test, self.y_pred), 4)
        log_recall = round(recall_score(self.y_test, self.y_pred), 4)
        log_precision = round(precision_score(self.y_test, self.y_pred), 4)
        log_rocauc = round(roc_auc_score(self.y_test, self.y_pred), 4)
        tn, fp, fn, tp = confusion_matrix(self.y_test, self.y_pred).ravel()

        # Display results in GUI
        self.ResultTP.setText(str(tp))
        self.ResultFP.setText(str(fp))
        self.ResultTN.setText(str(tn))
        self.ResultFN.setText(str(fn))
        self.ResultAccuracy.setText(str(log_accuracy))
        self.ResultRecall.setText(str(log_recall))
        self.ResultPrecision.setText(str(log_precision))
        self.ResultROCAUC.setText(str(log_rocauc))

    def Prediction(self):
        # Gather input data from the UI elements
        applicant_age = float(self.Applicant_Age.text() or 0)
        owned_car = int(self.Owned_Car.text() or 0)
        owned_realty = int(self.Owned_Realty.text() or 0)
        gender = 1 if self.Gender.currentText() == 'Male' else 0  # Assuming 1 for Male and 0 for Female
        years_of_working = float(self.Years_of_Working.text() or 0)
        education_type = self.Education_Type.currentIndex()  # Convert to numeric index
        family_status = self.Family_Status.currentIndex()  # Convert to numeric index
        housing_type = self.Housing_Type.currentIndex()  # Convert to numeric index
        income_type = self.Income_Type.currentIndex()  # Convert to numeric index
        total_children = int(self.Total_Children.text() or 0)
        total_income = float(self.Total_Income.text() or 0)
        total_family_members = int(self.Total_Family_Members.text() or 0)
        total_bad_debt = float(self.Total_Bad_Debt.text() or 0)
        total_good_debt = float(self.Total_Good_Debt.text() or 0)
        owned_email = int(self.Owned_Email.text() or 0)
        owned_phone = int(self.Owned_Phone.text() or 0)
        owned_work_phone = int(self.Owned_Work_Phone.text() or 0)
        owned_mobile_phone = int(self.Owned_Mobile_Phone.text() or 0)

        # Perform any necessary preprocessing, scaling, or data formatting

        # Pass the input data to the trained model for prediction
        prediction = self.model.predict([[applicant_age, owned_car, owned_realty, gender, years_of_working,
                                          education_type, family_status, housing_type, income_type,
                                          total_children, total_income, total_family_members,
                                          total_bad_debt, total_good_debt, owned_email,
                                          owned_phone, owned_work_phone, owned_mobile_phone]])

        # Display the prediction result
        if prediction[0] == 1:
            self.ResultStatusPredict.setText("Approved")
        else:
            self.ResultStatusPredict.setText("Denied")



