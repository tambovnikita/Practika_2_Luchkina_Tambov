from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Симплекс-метод')
        self.setStyleSheet("background-color: #2a343d")  # меняем цвет фона

        self.mainLbl = QLabel(self)     # Заголовок
        self.mainLbl.setFont(QtGui.QFont('Arial Black', 20))  # Изменяем шрифт
        self.mainLbl.setGeometry(QtCore.QRect(250, 10, 530, 50))  # Меняем размер и положение
        self.mainLbl.setText("С и м п л е к с  -  м е т о д")  # Меняем текст
        self.mainLbl.setStyleSheet("color: white")  # меняем цвет фона

        self.lineEdit1 = QtWidgets.QLineEdit(self)
        self.lineEdit1.setFont(QtGui.QFont('Times New Roman', 14))  # Изменяем шрифт.
        self.lineEdit1.setGeometry(QtCore.QRect(315, 100, 40, 30))  # Меняем размер и положение.

        self.mainBtn = QtWidgets.QPushButton(self)
        self.mainBtn.setText("Решить")  # Меняем текст
        self.mainBtn.setFont(QtGui.QFont('Times New Roman', 12))  # Изменяем шрифт.
        self.mainBtn.setGeometry(QtCore.QRect(700, 220, 200, 35))  # Меняем размер и положение.
        self.mainBtn.setStyleSheet("background-color: white")  # меняем цвет фона



app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())
