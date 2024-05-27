from Connectors.Connector import Connector
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE

# Function to transform the data
def transform_data(input_df):
    # Select necessary features
    df_selected = input_df.loc[:, ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
                                   'Owned_Realty', 'Owned_Phone', 'Total_Children',
                                   'Total_Family_Members', 'Total_Income', 'Years_of_Working',
                                   'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
                                   'Education_Type', 'Applicant_Gender']]

    # Normalize 'Education_Type' column
    df_selected['Education_Type'] = df_selected['Education_Type'].str.strip()
    scale_mapper = {'Lower secondary': 0, 'Secondary / secondary special': 1,
                    'Incomplete higher': 2, 'Higher education': 3, 'Academic degree': 4}
    df_selected['Education_Type'] = df_selected['Education_Type'].replace(scale_mapper).astype(int)

    # Create dummy variables
    Applicant_Gender_dummies = pd.get_dummies(df_selected['Applicant_Gender'], prefix='Applicant_Gender')
    Income_Type_dummies = pd.get_dummies(df_selected['Income_Type'], prefix='Income_Type')

    # Concatenate dummy variables to the DataFrame
    df_selected = pd.concat([df_selected, Applicant_Gender_dummies, Income_Type_dummies], axis=1)

    # Drop unnecessary columns
    df_selected = df_selected.drop(['Applicant_Gender', 'Income_Type'], axis=1)

    # Split data into x and y
    y = df_selected.iloc[:, 0].values
    x = df_selected.iloc[:, 1:].values

    # Normalize the data
    sc = StandardScaler()
    x = sc.fit_transform(x)

    return x, y, sc, df_selected.columns[1:]

# Function to train the SVM model
def svm_model(x_train, x_test, y_train, y_test):
    # Apply SMOTE only on the training set
    smote = SMOTE(random_state=242)
    x_train_smote, y_train_smote = smote.fit_resample(x_train, y_train)

    # Train SVM model
    svm = LinearSVC(max_iter=1000, dual=False)  # dual=False to avoid FutureWarning
    svm.fit(x_train_smote, y_train_smote)

    # Predict on the test set
    y_pred = svm.predict(x_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    rocauc = roc_auc_score(y_test, y_pred)
    confusion_matrix_svm = confusion_matrix(y_test, y_pred)

    return svm, accuracy, recall, precision, rocauc, confusion_matrix_svm

# Connect to the database and retrieve data
connector = Connector(server="localhost", port=3306, database="credit_card", username="root", password="123456")
connector.connect()
sql = "SELECT * FROM application_data"
df = connector.queryDataset(sql)

x, y, sc, feature_names = transform_data(df)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=242)
svm_model, accuracy, recall, precision, rocauc, confusion_matrix_svm = svm_model(x_train, x_test, y_train, y_test)

print("Accuracy:", accuracy)
print("Recall:", recall)
print("Precision:", precision)
print("ROC AUC:", rocauc)
print("Confusion Matrix:", confusion_matrix_svm)

# Function to transform new customer data
def transform_new_customer_data(new_data, sc, feature_names):
    new_data_df = pd.DataFrame(new_data, columns=feature_names)

    # Create dummy variables
    Applicant_Gender_dummies = pd.get_dummies(new_data_df['Applicant_Gender'], prefix='Applicant_Gender')
    Income_Type_dummies = pd.get_dummies(new_data_df['Income_Type'], prefix='Income_Type')

    new_data_df = pd.concat([new_data_df, Applicant_Gender_dummies, Income_Type_dummies], axis=1)

    new_data_df = new_data_df.drop(['Applicant_Gender', 'Income_Type'], axis=1)

    # Ensure all columns are present in new data
    for col in feature_names:
        if col not in new_data_df.columns:
            new_data_df[col] = 0

    # Sort columns to match training data
    new_data_df = new_data_df[feature_names]

    # Normalize the new data
    new_data_standardized = sc.transform(new_data_df)

    return new_data_standardized
