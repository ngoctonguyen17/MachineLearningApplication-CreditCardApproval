from PyQt6.QtWidgets import QApplication, QMainWindow

from UI.MainWindowEx import MainWindowEx

qApp=QApplication([])
qmainWindow = QMainWindow()
myWindow=MainWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
qApp.exec()
