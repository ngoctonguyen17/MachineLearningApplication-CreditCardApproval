import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC, LinearSVC

import MetricsResult
import MLModel
import TrainedModel
from Utils.FileUtil import FileUtil


class SVM(MLModel):
    def __init__(self, connector=None):
        super().__init__(connector=connector)
        self.le = LabelEncoder()
        self.sc_std = StandardScaler()

    def processTrain(self,columns_input,column_target,test_size,random_state):
        self.execPurchaseHistory()
        self.processTransform()
        y = self.df_selected.iloc[:, 0].values
        X = self.df_selected.iloc[:, 1:19].values
        print("X=", X)
        print("y=", y)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size,
                                                                                random_state=random_state)
        self.trainedmodel = TrainedModel()
        self.trainedmodel.X_train = self.X_train
        self.trainedmodel.X_test = self.X_test
        self.trainedmodel.y_train = self.y_train
        self.trainedmodel.y_test = self.y_test