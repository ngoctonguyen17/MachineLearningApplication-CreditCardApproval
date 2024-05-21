from Connectors.Connector import Connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC

connector = Connector(server="localhost", port=3306, database="credit_card", username="root", password="123456")
connector.connect()
sql = "SELECT * FROM application_data"
df = connector.queryDataset(sql)
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
df_selected = df.loc[:, ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
                          'Owned_Realty', 'Owned_Phone', 'Total_Children',
                          'Total_Family_Members', 'Total_Income', 'Years_of_Working',
                          'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
                          'Education_Type', 'Applicant_Gender']]

df_selected['Education_Type'].unique()
# Map the attribute into ordinal numbers from 0-4
df_selected['Education_Type'] = df_selected['Education_Type'].str.strip()

scale_mapper = {'Lower secondary': 0, 'Secondary / secondary special': 1,
                'Incomplete higher': 2, 'Higher education': 3, 'Academic degree': 4}

df_selected['Education_Type'] = df_selected['Education_Type'].replace(scale_mapper).astype(int)
df_selected['Education_Type'].unique()
df_selected['Applicant_Gender'].unique()
df_selected['Income_Type'].unique()

# Create dummies/one-hot encoding on every nominal attribute in the DataFrame
Applicant_Gender_dummies = pd.get_dummies(df_selected['Applicant_Gender'], prefix='Applicant_Gender')
Income_Type_dummies = pd.get_dummies(df_selected['Income_Type'], prefix='Income_Type')

# Concatenate the dummies into the train dataset
df_selected = pd.concat([df_selected, Applicant_Gender_dummies, Income_Type_dummies], axis=1)

# Drop categorical attributes (before transformation)
df_selected = df_selected.drop(['Applicant_Gender', 'Income_Type'], axis=1)

print(df_selected.head())

y = df_selected.iloc[:, 0].values
x = df_selected.iloc[:, 1:19].values

smote = SMOTE()
x_smote, y_smote = smote.fit_resample(x, y)

sc = StandardScaler()
x_smote = sc.fit_transform(x_smote)

x_train, x_test, y_train, y_test = train_test_split(x_smote, y_smote, test_size =0.3, random_state = 18)

svm = LinearSVC(max_iter=1000)

svm.fit(x_train, y_train)
y_pred = svm.predict(x_test)

log_accuracy=accuracy_score(y_test, y_pred)
log_recall=recall_score(y_test,y_pred)
log_precision=precision_score(y_test,y_pred)
log_rocauc=roc_auc_score(y_test,y_pred)

print('{:.4f}'.format(log_accuracy), '- Log Accuracy')
print('{:.4f}'.format(log_recall), '- Log Recall')
print('{:.4f}'.format(log_precision), '- Log Precision')
print('{:.4f}'.format(log_rocauc), '- Log ROC AUC')

pd.crosstab(y_test,y_pred)
confusion_matrix_svm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(4, 4))
sns.heatmap(confusion_matrix_svm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title('Support Vector Machines Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()


svm_roc_auc = roc_auc_score(y_test, svm.predict(x_test))
fpr, tpr, thresholds = roc_curve(y_test, svm.decision_function(x_test))
plt.figure()
plt.plot(fpr, tpr, label='Support Vector Machines (area = %0.4f)' % svm_roc_auc)

plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.show()
