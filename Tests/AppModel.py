from Connectors.Connector import Connector
from Models.MLModel import MLModel
from Models.Statistic import CreditCardStatistics
import pandas as pd

connector = Connector(server="localhost", port=3306, database="credit_card", username="root", password="123456")
connector.connect()

testModel = MLModel(connector)
testModel.execApplicationData()

dfTransform = testModel.processTransform()
dfTransform = dfTransform.infer_objects()
print(dfTransform['Applicant_Gender_dummies'].head(5))



# testModel.buildCorrelationMatrix(dfTransform)