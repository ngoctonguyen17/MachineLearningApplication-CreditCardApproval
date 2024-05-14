import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Connectors.Connector import Connector
from Models.Statistic import CreditCardStatistics

connector = Connector(server="localhost", port=3306, database="credit_card", username="root", password="123456")
connector.connect()

# test = CreditCardStatistics(connector=connector)
# test.execApplicationData()
# df = test.processApplicantAgeDistribution()
# print(df)
# test.visualizeDistribution("Applicant_Age", 'Applicant_Age', 'Distribution of Applicant Age')

# test = CreditCardStatistics(connector=connector)
# test.execApplicationData()
# df = test.processTotalGoodDebtDistribution()
# print(df)
# test.visualizeDistribution("Total_Good_Debt", 'Total_Good_Debt', 'Distribution of Total Good Debt')

# test = CreditCardStatistics(connector=connector)
# test.execApplicationData()
# df = test.processYearsOfWorkingDistribution()
# print(df)
# test.visualizeDistribution("Years_of_Working", 'Years_of_Working', 'Distribution of Years of Working')

test = CreditCardStatistics(connector=connector)
test.execApplicationData()
df = test.processTotalIncomeDistribution()
print(df)
test.visualizeDistribution("Total_Income", 'Total_Income', 'Distribution of Total Income')