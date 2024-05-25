from Connectors.Connector import Connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, accuracy_score, confusion_matrix, precision_score, recall_score

# Kết nối đến cơ sở dữ liệu và lấy dữ liệu
connector = Connector(server="localhost", port=3306, database="credit_card", username="root", password="123456")
connector.connect()
sql = "SELECT * FROM application_data"
df = connector.queryDataset(sql)

# Chọn các thuộc tính cần thiết
df_selected = df.loc[:, ['Status', 'Applicant_ID', 'Applicant_Age', 'Owned_Car',
                          'Owned_Realty', 'Owned_Phone', 'Total_Children',
                          'Total_Family_Members', 'Total_Income', 'Years_of_Working',
                          'Total_Good_Debt', 'Total_Bad_Debt', 'Income_Type',
                          'Education_Type', 'Applicant_Gender']]

# Chuẩn hóa cột 'Education_Type'
df_selected['Education_Type'] = df_selected['Education_Type'].str.strip()
scale_mapper = {'Lower secondary': 0, 'Secondary / secondary special': 1,
                'Incomplete higher': 2, 'Higher education': 3, 'Academic degree': 4}
df_selected['Education_Type'] = df_selected['Education_Type'].replace(scale_mapper).astype(int)

# Tạo biến dummy
Applicant_Gender_dummies = pd.get_dummies(df_selected['Applicant_Gender'], prefix='Applicant_Gender')
Income_Type_dummies = pd.get_dummies(df_selected['Income_Type'], prefix='Income_Type')

# Nối các biến dummy vào DataFrame
df_selected = pd.concat([df_selected, Applicant_Gender_dummies, Income_Type_dummies], axis=1)

# Xóa các cột không cần thiết
df_selected = df_selected.drop(['Applicant_Gender', 'Income_Type'], axis=1)

print(df_selected.head())

# Chia dữ liệu thành x và y
y = df_selected.iloc[:, 0].values
x = df_selected.iloc[:, 1:].values

# Chuẩn hóa dữ liệu
sc = StandardScaler()
x = sc.fit_transform(x)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=242)

# Áp dụng SMOTE chỉ lên tập huấn luyện
smote = SMOTE(random_state=18)
x_train_smote, y_train_smote = smote.fit_resample(x_train, y_train)

# Huấn luyện mô hình SVM
svm = LinearSVC(max_iter=1000, dual=False)  # dual=False để tránh cảnh báo FutureWarning

svm.fit(x_train_smote, y_train_smote)
y_pred = svm.predict(x_test)

# # Đánh giá mô hình
# log_accuracy = accuracy_score(y_test, y_pred)
# log_recall = recall_score(y_test, y_pred)
# log_precision = precision_score(y_test, y_pred)
# log_rocauc = roc_auc_score(y_test, y_pred)
#
# print('{:.4f}'.format(log_accuracy), '- Log Accuracy')
# print('{:.4f}'.format(log_recall), '- Log Recall')
# print('{:.4f}'.format(log_precision), '- Log Precision')
# print('{:.4f}'.format(log_rocauc), '- Log ROC AUC')

# # Hiển thị ma trận nhầm lẫn
# confusion_matrix_svm = confusion_matrix(y_test, y_pred)
#
# plt.figure(figsize=(4, 4))
# sns.heatmap(confusion_matrix_svm, annot=True, fmt="d", cmap="Blues", cbar=False)
# plt.title('Support Vector Machines Confusion Matrix')
# plt.xlabel('Predicted Label')
# plt.ylabel('True Label')
# plt.show()

# # Vẽ biểu đồ ROC
# svm_roc_auc = roc_auc_score(y_test, svm.predict(x_test))
# fpr, tpr, thresholds = roc_curve(y_test, svm.decision_function(x_test))
# plt.figure()
# plt.plot(fpr, tpr, label='Support Vector Machines (area = %0.4f)' % svm_roc_auc)
#
# plt.plot([0, 1], [0, 1], 'r--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic')
# plt.legend(loc="lower right")
# plt.show()


# tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

# Print the metrics
# print('True Positives (TP):', tp)
# print('True Negatives (TN):', tn)
# print('False Positives (FP):', fp)
# print('False Negatives (FN):', fn)
#
# status_counts_before = pd.Series(y_train).value_counts()
# status_counts_after = pd.Series(y_train_smote).value_counts()
# print("Counts before SMOTE:")
# print("Status 0:", status_counts_before.get(0, 0))
# print("Status 1:", status_counts_before.get(1, 0))
# print("Counts after SMOTE:")
# print("Status 0:", status_counts_after.get(0, 0))
# print("Status 1:", status_counts_after.get(1, 0))

# Tạo một DataFrame chứa thông tin của khách hàng mới
new_customer_data = pd.DataFrame({
    'Applicant_Age': [53],
    'Owned_Car': [0],
    'Owned_Realty': [1],
    'Owned_Phone': [1],
    'Total_Children': [0],
    'Total_Family_Members': [3],
    'Total_Income': [270000],
    'Years_of_Working': [5],
    'Total_Good_Debt': [0],
    'Total_Bad_Debt': [1000],
    'Applicant_Gender_F': [0],
    'Applicant_Gender_M': [1],
    'Income_Type_Commercial associate': [0],
    'Income_Type_Pensioner': [0],
    'Income_Type_State servant': [0],
    'Income_Type_Student': [1],
    'Income_Type_Working': [1],
    'Education_Type': [3]
})

# Chuẩn hóa dữ liệu mới
new_customer_data_standardized = sc.transform(new_customer_data)

# Dự đoán
predicted_status = svm.predict(new_customer_data_standardized)

# In kết quả dự đoán
if predicted_status == 1:
    print("Khách hàng này được phê duyệt thẻ tín dụng.")
else:
    print("Khách hàng này không được phê duyệt thẻ tín dụng.")
