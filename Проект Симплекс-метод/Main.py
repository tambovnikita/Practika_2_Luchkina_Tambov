
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFrame,\
    QGridLayout
import sys

from simplexdata import SimplexData

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(50, 50, 1030, 350)
        self.setWindowTitle('Симплекс-метод')

        # градиентный фон
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(240, 160, 160))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        # Для ввода только int-чисел и float-чисел
        self.validatorInt = QtGui.QIntValidator(self)
        self.validatorFloat = QtGui.QDoubleValidator(self)


        self.mainLbl = QLabel(self)     # Заголовок
        self.mainLbl.setFont(QtGui.QFont('Segoe print', 26))  # Изменяем шрифт
        self.mainLbl.setGeometry(QtCore.QRect(190, 80, 800, 50))  # Меняем размер и положение
        self.mainLbl.setText("С и м п л е к с  -  м е т о д")  # Меняем текст
        self.mainLbl.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.mainLbl1 = QLabel(self)
        self.mainLbl1.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.mainLbl1.setGeometry(QtCore.QRect(50, 150, 530, 50))  # Меняем размер и положение
        self.mainLbl1.setText("количество ограничений")  # Меняем текст
        self.mainLbl1.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.lineEdit1.setGeometry(QtCore.QRect(430, 160, 50, 35))  # Меняем размер и положение.
        self.lineEdit1.setStyleSheet("color: #7f4355")  # меняем цвет текста
        self.lineEdit1.setValidator(self.validatorInt)  # разрешается ввод только целых чисел

        self.mainLbl2 = QLabel(self)
        self.mainLbl2.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.mainLbl2.setGeometry(QtCore.QRect(550, 150, 530, 50))  # Меняем размер и положение
        self.mainLbl2.setText("количество переменных")  # Меняем текст
        self.mainLbl2.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.lineEdit2.setGeometry(QtCore.QRect(925, 160, 50, 35))  # Меняем размер и положение.
        self.lineEdit2.setStyleSheet("color: #7f4355")  # меняем цвет текста
        self.lineEdit2.setValidator(self.validatorInt)  # разрешается ввод только целых чисел

        self.mainBtn = QPushButton(self)
        self.mainBtn.setText("Продолжить")  # Меняем текст
        self.mainBtn.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
        self.mainBtn.setGeometry(QtCore.QRect(270, 230, 500, 50))  # Меняем размер и положение.
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

        self.infoBtn.clicked.connect(self.infoBtnClick)     # подключаем кнопку "Справка" к слоту

        self.frame = QFrame(self)   # создаём псевдо-область, которая при нажатии будет удаляться и создаваться новая
        self.frame.hide()   # скроем псевдо-область
        self.MainButton = QPushButton(self)     # создаём кнопку "Решить" заранее
        self.MainButton.hide()      # скроем пока кнопку "Решить"


    def infoBtnClick(self):     # вызывает диалоговое окно "Справка"
        formInfo = FormInfo(self)
        formInfo.exec_()


    def mainBtnClick(self):

        if self.lineEdit1.text() != '' and self.lineEdit2.text() != '':
            self.frame.deleteLater()
            self.frame = QFrame(self)
            self.setGeometry(50, 50, 1030, 910)     # делаем главное окно больше по высоте
            self.frame.show()   # показываем скрытую область
            self.MainButton.show()  # показываем скрытую кнопку "Решить"

            self.kol_str = int(self.lineEdit1.text())
            self.kol_stol = int(self.lineEdit2.text())

            self.frame.setGeometry(QtCore.QRect(65, 330, 900, 450))  # Меняем размер и положение.
            self.frame.setStyleSheet("background-color: rgba(230,230,230,0.4); border-radius: 20px")
            self.gridLayout = QGridLayout()  # Размещение виджетов по сетке.

            for i_1 in range(self.kol_str):
                for j_1 in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. в ограничениях).
                    le = QLineEdit()
                    le.setFixedHeight(35)
                    le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                    le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                    self.gridLayout.addWidget(le, i_1, j_1)

                self.comboBox = QComboBox()
                self.comboBox.setFixedHeight(30)
                self.comboBox.setFixedWidth(50)
                self.comboBox.setStyleSheet("border-radius: 10px")
                self.comboBox.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
                self.comboBox.addItem("⩽")
                self.comboBox.addItem("=")
                self.comboBox.addItem("⩾")
                self.gridLayout.addWidget(self.comboBox, i_1, self.kol_stol)  # Вставляем QComboBox ("<=", "=", ">=").

                le = QLineEdit()
                le.setFixedHeight(35)
                le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                self.gridLayout.addWidget(le, i_1, self.kol_stol + 1)  # Вставляем QLineEdit (свободные члены).


            for i_1 in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. крит. функции).
                le = QLineEdit()
                le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                le.setStyleSheet("margin-top: 30px")
                le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                self.gridLayout.addWidget(le, self.kol_str, i_1)

            self.label_strel = QLabel()
            self.label_strel.setText(' 🠖')
            self.label_strel.setFixedHeight(60)
            self.label_strel.setStyleSheet("border-radius: 10px; margin-top: 30px")
            self.label_strel.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
            self.gridLayout.addWidget(self.label_strel, self.kol_str, self.kol_stol)  # Вставляем '🠖'.

            self.comboBox_max_or_min = QComboBox()
            self.comboBox_max_or_min.setFixedHeight(70)
            self.comboBox_max_or_min.setFixedWidth(80)
            self.comboBox_max_or_min.setFont(QtGui.QFont('Century Gothic', 12))  # Изменяем шрифт.
            self.comboBox_max_or_min.addItem("MAX")
            self.comboBox_max_or_min.addItem("MIN")
            self.comboBox_max_or_min.setStyleSheet("border-radius: 10px; margin-top: 30px; padding-left: 15px")
            # Вставляем QComboBox ("max", "min").
            self.gridLayout.addWidget(self.comboBox_max_or_min, self.kol_str, self.kol_stol + 1)


            self.frame.setLayout(self.gridLayout)

            self.MainButton.setText("Решение")  # Меняем текст
            self.MainButton.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
            self.MainButton.setGeometry(QtCore.QRect(185, 825, 670, 50))  # Изменяем размер и положение
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

            self.MainButton.clicked.connect(self.toSimplexData)

    # Функция, вызывающая обработчик-сборщик введённых данных
    def toSimplexData(self):
        OTVET = SimplexData(self.kol_str, self.kol_stol, self.gridLayout)
        print(OTVET)


class FormInfo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FormInfo, self).__init__(parent)
        self.setGeometry(1100, 80, 600, 900)
        self.setWindowTitle('Справка по Симплекс-методу')
        # градиентный фон
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(240, 160, 160))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)  # Только чтение.
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 580, 880))  # Меняем размер и положение.
        self.textEdit.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.textEdit.setHtml(
            "<font color='black' size='8' style='white-space: pre-wrap'><b>        Что такое Симплекс-метод?</b></font>"
            "<hr/>"
            "<font color='black' size='5' style='white-space: pre-wrap'>\n    В симплекс-методе реализуется упорядоченный процесс, при котором, начиная "
            "с некоторой исходной допустимой угловой точки осуществляются последовательные переходы от одной допустимой "
            "экстремальной точки к другой до тех пор, пока не будет найдена точка, соответствующая оптимальному решению.\n\n</font>"
            "<font color='black' size='5' style='white-space: pre-wrap'>    В задаче имеется n переменных и m независимых линейных ограничений, заданных "
            "в форме уравнений. Известно, что оптимальное решение (если такое имеется) достигается в одной из опорных "
            "точек (вершин ОДР), где по крайней мере k=n-m из переменных равны нулю. Выбираются какие-то k переменных "
            "в качестве свободных и выражаются через них остальные m базисных переменных. Решение может быть допустимым "
            "или недопустимым. Оно допустимо, если все свободные члены неотрицательны.\n\n</font>"
            "<font color='black' size='8' style='white-space: pre-wrap'><b>               Алгоритм решения:</b></font>"
            "<hr/>"
            "<font color='black' size='5' style='white-space: pre-wrap'>\n    1.    Приводим модель к канонической форме\n"
            "    2.    Находим начальное базисное "
            "решение\n   2.1    определяем базисные и свободные переменные\n   2.2.    Для нахождения общего решения СЛУ нам нужно "
            "базисные переменные выразить через свободные. Из каждого уравнения нам нужно исключить все базисные "
            "переменные кроме одной, т.е. базисную матрицу привести к единичной. Воспользуемся методом Гаусса-Жордана, "
            "в котором реализуются элементарные преобразования.\n   2.3    Приравниваем свободные переменные 0, находим базисные, "
            "таким образом получаем базисное решение системы (частное решение СЛУ при котором свободные переменные "
            "обращаются в 0)\n    3.    Проверяем начальное базисное решения на опорность.\n   3.1    Условие неотрицательности не "
            "выполняется. Решение базисное, но не опорное, не принадлежит ОДР.\n<b>   Применяем алгоритм поиска базисного "
            "опорного решения:</b>\n  1) Выбираем в столбце свободных членов B минимальный из отрицательных элементов. "
            "В соответствующей ему строке также выбираем наименьший отрицательный элемент. Этот столбец принимаем за "
            "разрешающий. Если таких элементов нет, значит нет решения ЗЛП т.е. при совместной системе ограничений вся "
            "ОДР не соответствует положительности переменных.\n  2) В разрешающем столбце выбираем элементы имеющие "
            "одинаковый знак с соответствующим свободным членом (правая часть ограничений) и ищем отношением к ним "
            "свободных членов . Из этих отношений выбираем минимальное. Эта строка будет разрешающей.\n  3) Проводим "
            "процедуру однократного замещения – взаимообмен переменных. (Переразрешаем систему относительно измененного "
            "базиса)\n  4) Процедура итерационная. Проводится до тех пор пока все переменные в решении не станут "
            "неотрицательные. Т.е. мы упорядоченно, целенаправленно «спускаемся» на ОДР.\n\n   3.2    Условие неотрицательности "
            "выполняется. Переходим к следующему пункту.\n    4.    Проверка полученного базисного опорного решения на "
            "оптимальность. Введем понятие: D – оценка переменной относительно выбранного базиса: D=Z-C\n    5.    Определяем "
            "включаемую в базис переменную.. Включаемой в базис переменной соответствует наибольшая по модулю "
            "отрицательная оценка D  (в задаче максимизации). В задаче минимизации должны остаться только отрицательные "
            "оценки, поэтому выбираем наибольшую положительную оценку.\n    6.    Условие допустимости. Определяем исключаемую "
            "из базиса переменную (т.е ту с которой поменяется местами включаемая переменная). В качестве таковой "
            "выбираем ту переменную текущего базиса, которая первой обращается в ноль при увеличении включаемой переменной "
            "вплоть до значения, соответствующего смежной базисной точке. Для этого в разрешающем столбце среди "
            "коэффициентов в ограничениях   выбираем положительные элементы и находим отношения к ним свободных членов "
            "(правых частей ограничений) . Будем обозначать это отношение  Q. Из этих отношений выбираем минимальное. "
            "Переменная ему соответствующая будет исключаемой из базиса, а строка разрешающей.\n    7.    Переразрешаем задачу "
            "относительно измененного базиса – проводим процедуру однократного замещения. Проводим итерационные вычисления "
            "до получения оптимального решения.</font>"
        )

app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())
