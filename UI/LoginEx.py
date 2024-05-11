from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from Connectors.Connector import Connector
from UI.Login import Ui_MainWindow
import traceback

class LoginEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connector = Connector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.pushButtonLogIn.clicked.connect(self.login)

    def connectDatabase(self):
        self.connector.server = "localhost"
        self.connector.port = 3306
        self.connector.database = "credit_card"
        self.connector.username = "root"
        self.connector.password = "123456"
        self.connector.connect()

    def login(self):
        self.connectDatabase()
        self.msg = QMessageBox()
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()

        sql = f"SELECT COUNT(*) FROM credit_card.employee WHERE username = '{username}' AND password = '{password}'"
        try:
            result = self.connector.queryDataset(sql)
            count = result.iloc[0, 0]
            if count == 1:
                self.MainWindow.close()
            else:
                self.msg.warning(self.MainWindow, "Login Error", "Incorrect username or password.")
            if self.parent != None:
                self.parent.checkEnableWidget(True)
        except Exception as e:
            traceback.print_exc()
            self.msg = QMessageBox()
            self.msg.setText("Login failed")
            self.msg.setWindowTitle("Info")
            self.msg.show()

    def show(self):
        self.MainWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.MainWindow.show()