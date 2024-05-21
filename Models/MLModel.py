from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd

from Models.Statistic import CreditCardStatistics

class MLModel(CreditCardStatistics):
    def __init__(self, connector=None):
        super().__init__(connector)
        self.le = LabelEncoder()

    def processTransformByColumns(self, df, columns):
        for col in columns:
            df[col] = self.le.fit_transform(df[col])

    def processTransform(self):
        sql = "SELECT * FROM application_data"
        df = self.connector.queryDataset(sql)
        categorical_feature = ['Applicant_Gender', 'Owned_Car', 'Owned_Realty',
                               'Income_Type', 'Education_Type', 'Family_Status',
                               'Housing_Type', 'Owned_Mobile_Phone', 'Owned_Work_Phone',
                               'Total_Bad_Debt', 'Owned_Phone', 'Owned_Email',
                               'Job_Title']
        numerical_feature = ['Total_Children', 'Total_Income', 'Total_Family_Members',
                             'Applicant_Age', 'Years_of_Working', 'Total_Bad_Debt',
                             'Total_Good_Debt']

        dropping = ['Applicant_ID']
        result = ['Status']
        self.df_selected = df.loc[:, ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
                                      'Owned_Realty', 'Owned_Phone', 'Total_Children',
                                      'Total_Family_Members', 'Total_Income', 'Years_of_Working',
                                      'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
                                      'Education_Type', 'Applicant_Gender']]
        self.df_selected['Education_Type'].unique()

        # Strip whitespace from 'Education_Type' and map to numerical values
        # Map the atribute into ordinal numbers from 0-4
        self.df_selected['Education_Type'] = self.df_selected['Education_Type'].str.strip()

        scale_mapper = {'Lower secondary': 0, 'Secondary / secondary special': 1,
                        'Incomplete higher': 2, 'Higher education': 3, 'Academic degree': 4}

        self.df_selected['Education_Type'] = self.df_selected['Education_Type'].replace(scale_mapper)

        if 'Income_Type_Working' in self.df_selected.columns:
            self.df_selected['Income_Type_Working'] = self.df_selected['Income_Type_Working'].replace({True: 1, False: 0})

        self.df_selected['Education_Type'].unique()
        self.df_selected['Applicant_Gender'].unique()
        self.df_selected['Income_Type'].unique()

        # Create dummy variables for 'Applicant_Gender' and 'Income_Type'
        Applicant_Gender_dummies = pd.get_dummies(self.df_selected['Applicant_Gender'], prefix='Applicant_Gender')
        Income_Type_dummies = pd.get_dummies(self.df_selected['Income_Type'], prefix='Income_Type')

        # Concatenate dummies and drop original columns
        self.df_selected = pd.concat([self.df_selected, Applicant_Gender_dummies, Income_Type_dummies], axis=1)
        self.df_selected.drop(['Applicant_Gender', 'Income_Type'], axis=1, inplace=True)
        return self.df_selected

    def buildCorrelationMatrix(self, df):
        sql = "SELECT * FROM application_data"
        df = self.connector.queryDataset(sql)
        self.df_selected = df[
            ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
             'Owned_Realty', 'Owned_Phone', 'Total_Children',
             'Total_Family_Members', 'Total_Income', 'Years_of_Working',
             'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
             'Education_Type', 'Applicant_Gender']
        ]
        plt.figure(figsize=(18, 15))
        df_corr = self.df_selected.corr(numeric_only=True)
        ax = sns.heatmap(df_corr, annot=True, vmin=-1.0, cmap='mako')
        plt.title('Correlation Heatmap')
        plt.show()