
import matplotlib.pyplot as plt
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

    def processTotalGoodDebtDistribution(self):
        df_status_0 = self.df[self.df['Status'] == 0]
        df_status_1 = self.df[self.df['Status'] == 1]
        age_counts_0 = df_status_0['Applicant_Age'].value_counts().reset_index()
        age_counts_0.columns = ['Applicant_Age', 'Status 0 Count']
        age_counts_1 = df_status_1['Applicant_Age'].value_counts().reset_index()
        age_counts_1.columns = ['Applicant_Age', 'Status 1 Count']
        merged_df = pd.merge(age_counts_0, age_counts_1, on='Applicant_Age', how='outer').fillna(0)
        self.dfTotalGoodDebt = merged_df
        return self.dfTotalGoodDebt
    def processYearsOfWorkingDistribution(self):
        df_status_0 = self.df[self.df['Status'] == 0]
        df_status_1 = self.df[self.df['Status'] == 1]
        age_counts_0 = df_status_0['Years_of_Working'].value_counts().reset_index()
        age_counts_0.columns = ['Years_of_Working', 'Status 0 Count']
        age_counts_1 = df_status_1['Years_of_Working'].value_counts().reset_index()
        age_counts_1.columns = ['Years_of_Working', 'Status 1 Count']
        merged_df = pd.merge(age_counts_0, age_counts_1, on='Years_of_Working', how='outer').fillna(0)
        self.dfYearsOfWorking = merged_df
        return self.dfYearsOfWorking

    def processTotalIncomeDistribution(self):
        df_status_0 = self.df[self.df['Status'] == 0]
        df_status_1 = self.df[self.df['Status'] == 1]
        age_counts_0 = df_status_0['Total_Income'].value_counts().reset_index()
        age_counts_0.columns = ['Total_Income', 'Status 0 Count']
        age_counts_1 = df_status_1['Total_Income'].value_counts().reset_index()
        age_counts_1.columns = ['Total_Income', 'Status 1 Count']
        merged_df = pd.merge(age_counts_0, age_counts_1, on='Total_Income', how='outer').fillna(0)
        self.dfTotalIncome = merged_df
        return self.dfTotalIncome

    def processApplicantAgeDistribution(self):
        df_status_0 = self.df[self.df['Status'] == 0]
        df_status_1 = self.df[self.df['Status'] == 1]
        age_counts_0 = df_status_0['Applicant_Age'].value_counts().reset_index()
        age_counts_0.columns = ['Applicant_Age', 'Status 0 Count']
        age_counts_1 = df_status_1['Applicant_Age'].value_counts().reset_index()
        age_counts_1.columns = ['Applicant_Age', 'Status 1 Count']
        merged_df = pd.merge(age_counts_0, age_counts_1, on='Applicant_Age', how='outer').fillna(0)
        self.dfApplicantAge = merged_df
        return self.dfApplicantAge

    def visualizeDistribution(self, column, xlabel, title):
        plt.figure()
        sns.distplot(self.df.loc[self.df["Status"] == 1, column], hist=False, label="status 1")
        sns.distplot(self.df.loc[self.df["Status"] == 0, column], hist=False, label="status 0")
        plt.xlabel(xlabel)
        plt.ylabel('Density')
        plt.title(title)
        plt.legend()
        plt.show()




