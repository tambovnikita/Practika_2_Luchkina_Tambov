import time

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFrame, QGridLayout
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(50, 50, 1030, 900)
        self.setWindowTitle('Симплекс-метод')

        # градиентный фон
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(240, 160, 160))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        self.mainLbl = QLabel(self)     # Заголовок
        self.mainLbl.setFont(QtGui.QFont('Century Gothic', 24))  # Изменяем шрифт
        self.mainLbl.setGeometry(QtCore.QRect(250, 70, 600, 50))  # Меняем размер и положение
        self.mainLbl.setText("С и м п л е к с  -  м е т о д")  # Меняем текст
        self.mainLbl.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.mainLbl1 = QLabel(self)
        self.mainLbl1.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.mainLbl1.setGeometry(QtCore.QRect(50, 130, 530, 50))  # Меняем размер и положение
        self.mainLbl1.setText("количество ограничений")  # Меняем текст
        self.mainLbl1.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.lineEdit1.setGeometry(QtCore.QRect(430, 140, 50, 35))  # Меняем размер и положение.
        self.lineEdit1.setStyleSheet("color: #7f4355")  # меняем цвет текста

        self.mainLbl2 = QLabel(self)
        self.mainLbl2.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.mainLbl2.setGeometry(QtCore.QRect(550, 130, 530, 50))  # Меняем размер и положение
        self.mainLbl2.setText("количество переменных")  # Меняем текст
        self.mainLbl2.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.lineEdit2.setGeometry(QtCore.QRect(925, 140, 50, 35))  # Меняем размер и положение.
        self.lineEdit2.setStyleSheet("color: #7f4355")  # меняем цвет текста

        self.mainBtn = QPushButton(self)
        self.mainBtn.setText("Продолжить")  # Меняем текст
        self.mainBtn.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
        self.mainBtn.setGeometry(QtCore.QRect(350, 200, 300, 50))  # Меняем размер и положение.
        self.mainBtn.setStyleSheet("""
                QPushButton {
                    background-color: #f8ebf4;
                    color: #7f4355;
                    border-radius: 20px
                }
                QPushButton:hover {
                    background-color: #7f4355;
                    color: #f8ebf4;
                    border-radius: 20px
                }
                QPushButton:pressed {
                    background-color: #31102b;
                    color: #f8ebf4;
                    border-radius: 20px
                }
        """)  # меняем цвет фона
        self.mainBtn.clicked.connect(self.mainBtnClick)

        self.infoBtn = QPushButton(self)
        self.infoBtn.setText("Справка")  # Меняем текст
        self.infoBtn.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
        self.infoBtn.setGeometry(QtCore.QRect(800, 20, 200, 40))  # Меняем размер и положение.
        self.infoBtn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #7f4355;
                    border-radius: 20px
                }
                QPushButton:hover {
                    background-color: #7f4355;
                    color: white;
                    border-radius: 20px
                }
                QPushButton:pressed {
                    background-color: black;
                    color: white;
                    border-radius: 20px
                }
        """)  # меняем цвет фона
        self.infoBtn.clicked.connect(self.infoBtnClick)

        # теория
        """
        В симплекс-методе реализуется упорядоченный процесс, при котором, начиная с некоторой исходной допустимой угловой
        точки осуществляются последовательные переходы от одной допустимой экстремальной точки к другой до тех пор, пока
        не будет найдена точка, соответствующая оптимальному решению. 
        В задаче имеется n переменных и m независимых линейных ограничений, заданных в форме уравнений. Известно, что
        оптимальное решение (если такое имеется) достигается в одной из опорных точек (вершин ОДР), где по крайней мере
        k=n-m из переменных равны нулю. Выбираются какие-то k переменных в качестве свободных и выражаются через них
        остальные m базисных переменных. Решение может быть допустимым или недопустимым. Оно допустимо, если все
        свободные члены неотрицательны.
        Алгоритм решения:
        1.	Приводим модель к канонической форме
        2.	Находим начальное базисное решение
        2.1 определяем базисные и свободные переменные
        2.2.	Для нахождения общего решения СЛУ нам нужно базисные переменные выразить через свободные. Из каждого
        уравнения нам нужно исключить все базисные переменные кроме одной, т.е. базисную матрицу привести к единичной.
        Воспользуемся методом Гаусса-Жордана, в котором реализуются элементарные преобразования.
        2.3 Приравниваем свободные переменные 0, находим базисные, таким образом получаем базисное решение системы
        (частное решение СЛУ при котором свободные переменные обращаются в 0)
        3. Проверяем начальное базисное решения на опорность. 
        3.1 Условие неотрицательности не выполняется. Решение базисное, но не опорное, не принадлежит ОДР. Применяем
        алгоритм поиска базисного опорного решения: 
        1) Выбираем в столбце свободных членов B минимальный из отрицательных элементов. В соответствующей ему строке
        также выбираем наименьший отрицательный элемент. Этот столбец принимаем за разрешающий. Если таких элементов
        нет, значит нет решения ЗЛП т.е. при совместной системе ограничений вся ОДР не соответствует положительности переменных. 
        2) В разрешающем столбце выбираем элементы имеющие одинаковый знак с соответствующим свободным членом
        (правая часть ограничений) и ищем отношением к ним свободных членов . Из этих отношений выбираем минимальное.
        Эта строка будет разрешающей. 
        3) Проводим процедуру однократного замещения – взаимообмен переменных. (Переразрешаем систему относительно
        измененного базиса) 
        4) Процедура итерационная. Проводится до тех пор пока все переменные в решении не станут неотрицательные. Т.е.
        мы упорядоченно, целенаправленно «спускаемся» на ОДР. 
        3.2 Условие неотрицательности выполняется. Переходим к следующему пункту.
        4.	Проверка полученного базисного опорного решения на оптимальность.
        Введем понятие: D – оценка переменной относительно выбранного базиса: D=Z-C
        5.	Определяем включаемую в базис переменную.. Включаемой в базис переменной соответствует наибольшая по модулю
        отрицательная оценка D  (в задаче максимизации). В задаче минимизации должны остаться только отрицательные оценки,
        поэтому выбираем наибольшую положительную оценку.
        6.	Условие допустимости. Определяем исключаемую из базиса переменную (т.е ту с которой поменяется местами
        включаемая переменная). В качестве таковой выбираем ту переменную текущего базиса, которая первой обращается в
        ноль при увеличении включаемой переменной вплоть до значения, соответствующего смежной базисной точке. 
        Для этого в разрешающем столбце среди коэффициентов в ограничениях   выбираем положительные элементы и находим
        отношения к ним свободных членов (правых частей ограничений) . Будем обозначать это отношение  Q. Из этих
        отношений выбираем минимальное. Переменная ему соответствующая будет исключаемой из базиса, а строка разрешающей.
        7.	Переразрешаем задачу относительно измененного базиса – проводим процедуру однократного замещения
        Проводим итерационные вычисления до получения оптимального решения
        """

        self.frame = QFrame(self)
        self.TextEdit = QtWidgets.QTextEdit(self)
        self.MainButton = QtWidgets.QPushButton(self)

    def mainBtnClick(self):

        if self.lineEdit1.text() != '' and self.lineEdit2.text() != '':

            self.kol_str = int(self.lineEdit1.text())
            self.kol_stol = int(self.lineEdit2.text())

            self.frame.setGeometry(QtCore.QRect(40, 300, 950, 500))  # Меняем размер и положение.
            self.frame.setStyleSheet("background-color: rgba(230,230,230,0.5)")
            self.gridLayout = QGridLayout()  # Размещение виджетов по сетке.

            for i_1 in range(self.kol_str):
                for j_1 in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. в ограничениях).
                    self.gridLayout.addWidget(QLineEdit(), i_1, j_1)

                self.comboBox = QComboBox()
                self.comboBox.setFixedHeight(30)
                self.comboBox.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
                self.comboBox.addItem("<=")
                self.comboBox.addItem("=")
                self.comboBox.addItem(">=")
                self.gridLayout.addWidget(self.comboBox, i_1, self.kol_stol)  # Вставляем QComboBox ("<=", "=", ">=").

                self.gridLayout.addWidget(QLineEdit(), i_1, self.kol_stol + 1)  # Вставляем QLineEdit (свободные члены).

            self.label_zero = QLabel()
            self.label_zero.setFixedHeight(30)
            self.gridLayout.addWidget(self.label_zero, self.kol_str, 0)  # Вставляем пустую строку.

            for i_1 in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. крит. функции).
                self.gridLayout.addWidget(QLineEdit(), self.kol_str + 1, i_1)

            self.label_strel = QLabel()
            self.label_strel.setText('  🠖')
            self.label_strel.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
            self.gridLayout.addWidget(self.label_strel, self.kol_str + 1, self.kol_stol)  # Вставляем '🠖'.

            self.comboBox_max_or_min = QComboBox()
            self.comboBox_max_or_min.setFixedHeight(30)
            self.comboBox_max_or_min.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
            self.comboBox_max_or_min.addItem("MAX")
            self.comboBox_max_or_min.addItem("MIN")
            # Вставляем QComboBox ("max", "min").
            self.gridLayout.addWidget(self.comboBox_max_or_min, self.kol_str + 1, self.kol_stol + 1)


            self.frame.setLayout(self.gridLayout)

            self.MainButton.setText("Решение")  # Меняем текст
            self.MainButton.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
            self.MainButton.setGeometry(QtCore.QRect(350, 825, 300, 50))  # Изменяем размер и положение
            self.MainButton.setStyleSheet("""
                            QPushButton {
                                background-color: #f8ebf4;
                                color: #7f4355;
                                border-radius: 20px
                            }
                            QPushButton:hover {
                                background-color: #7f4355;
                                color: #f8ebf4;
                                border-radius: 20px
                            }
                            QPushButton:pressed {
                                background-color: #31102b;
                                color: #f8ebf4;
                                border-radius: 20px
                            }
                    """)  # меняем цвет фона
            self.MainButton.clicked.connect(self.mainBtnClick)





    def infoBtnClick(self):
        formInfo = FormInfo(self)
        formInfo.exec_()


class FormInfo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FormInfo, self).__init__(parent)
        self.setGeometry(1100, 80, 500, 900)
        self.setWindowTitle('Справка по Симплекс-методу')

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 480, 880))  # Меняем размер и положение.
        self.textEdit.setHtml("""<font color='black' size='8'>Симплекс-метод</font>
                              <hr/>
                              <font color='black' size='5'>И тут обычный текст</font>""")

app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())
