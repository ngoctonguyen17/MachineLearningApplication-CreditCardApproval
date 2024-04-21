from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6 import QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QApplication
from Connectors.Connector import Connector
from UI.MainWindow import Ui_MainWindow

# Rest of the code remains the same

# Rest of the code remains the same

class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connector = Connector()
        self.selectedCompany = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.connectPushButton.clicked.connect(self.connectDatabase)
        self.viewDataPushButton.clicked.connect(self.viewData)

    def showCompany(self, table, df):
        table.setRowCount(0)
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(["Company or Corporation"])

        row = 0
        for _, item in df.iterrows():
            arr = item.values.tolist()
            table.insertRow(row)
            for j, data in enumerate(arr):
                table.setItem(row, j, QTableWidgetItem(str(data)))
            row += 1

    def connectDatabase(self):
        self.connector.server = self.serverHostLineEdit.text()
        self.connector.port = int(self.portLineEdit.text())
        self.connector.database = self.databaseLineEdit.text()
        self.connector.username = self.userLineEdit.text()
        self.connector.password = self.passwordLineEdit.text()

        if self.connector.connect():
            QMessageBox.information(
                self.MainWindow,
                "Connection Successful",
                "Database connected successfully."
            )
            try:
                sql = "SHOW TABLES"
                df = self.connector.queryDataset(sql)
                self.showCompany(self.companyTableWidget, df)
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Error", str(e))
        else:
            QMessageBox.critical(
                self.MainWindow,
                "Connection Error",
                "Failed to connect to the database."
            )

    def showDataIntoTableWidget(self, table, df):
        table.setRowCount(0)
        table.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            table.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for _, item in df.iterrows():
            arr = item.values.tolist()
            table.insertRow(row)
            for j, data in enumerate(arr):
                table.setItem(row, j, QTableWidgetItem(str(data)))
            row += 1

    def viewData(self):
        row = self.companyTableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self.MainWindow, "Error", "Please select a row before clicking View Data.")
            return

        reply = QMessageBox.question(self.MainWindow, 'Confirm',
                                     'Are you sure you want to view data of this company?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                company = self.companyTableWidget.item(row, 0).text()
                sql = f"SELECT * FROM {company}"
                df = self.connector.queryDataset(sql)
                self.showDataIntoTableWidget(self.dataTableWidget, df)
            except Exception as e:
                QMessageBox.warning(self.MainWindow, "Error", f"An error occurred: {str(e)}")

    def show(self):
        self.MainWindow.show()