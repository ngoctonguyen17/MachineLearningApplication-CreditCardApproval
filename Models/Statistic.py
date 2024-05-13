from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


class CreditCardStatistics:
    def __init__(self, connector=None):
        self.connector = connector
        self.lasted_df = None

    def execApplicationData(self, tableName=None):
        if tableName is None:
            sql = "SELECT * FROM application_data"
        else:
            sql = "SELECT * FROM {}".format(tableName)
        self.df = self.connector.queryDataset(sql)
        self.lasted_df = self.df
        return self.df

    def printHead(self, row):
        print(self.df.head(row))
    def printTail(self, row):
        print(self.df.tail(row))
    def printInfo(self):
        print(self.df.info())
    def printDescribe(self):
        print(self.df.describe())
    def processGenderDistribution(self):
        gender_counts = self.df['Applicant_Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        self.lasted_df = gender_counts
        return gender_counts

    def processAgeDistribution(self):
        age_counts = self.df['Applicant_Age'].value_counts().reset_index().rename(
            columns={"index": "Age", "Applicant_Age": "Count"})
        age_counts.sort_values(by=['Age'], ascending=True, inplace=True)
        self.lasted_df = age_counts
        return age_counts

    def processIncomeDistribution(self):
        income_counts = self.df['Total_Income'].value_counts().reset_index().rename(columns={"index": "Income", "Total_Income": "Count"})
        income_counts.sort_values(by=['Income'], ascending=True, inplace=True)
        self.lasted_df = income_counts
        return income_counts

    def visualizePieChart(self, df, columnLabel, columnStatistic, title, legend=True):
        explode = [0.1] + [0] * (len(df[columnLabel]) - 1)
        plt.figure(figsize=(8, 6))
        plt.pie(df[columnStatistic], labels=df[columnLabel], autopct='%1.2f%%', explode=explode)
        if legend:
            plt.legend(df[columnLabel])
        plt.title(title)
        plt.show()

    def visualizeBarChart(self, df, columnX, columnY, title):
        plt.figure(figsize=(8, 6))
        plt.bar(df[columnX], df[columnY])
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.show()

    def visualizeScatterPlot(self, df, columnX, columnY, title):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x=columnX, y=columnY)
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.show()
