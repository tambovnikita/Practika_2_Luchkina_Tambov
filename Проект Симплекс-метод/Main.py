
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFrame,\
    QGridLayout, QScrollArea, QWidget, QFormLayout
import sys

from simplexdata import SimplexData

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(50, 50, 1030, 350)
        self.setWindowTitle('Симплекс-метод')   # Название окна
        self.setWindowIcon(QtGui.QIcon('MainIco.ico'))    # Иконка окна

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

        self.lblOgr = QLabel(self)
        self.lblOgr.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.lblOgr.setGeometry(QtCore.QRect(50, 150, 530, 50))  # Меняем размер и положение
        self.lblOgr.setText("количество ограничений")  # Меняем текст
        self.lblOgr.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.leOgr = QLineEdit(self)
        self.leOgr.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.leOgr.setGeometry(QtCore.QRect(430, 160, 50, 35))  # Меняем размер и положение.
        self.leOgr.setStyleSheet("color: #7f4355")  # меняем цвет текста
        self.leOgr.setValidator(self.validatorInt)  # разрешается ввод только целых чисел

        self.lblPer = QLabel(self)
        self.lblPer.setFont(QtGui.QFont('Century Gothic', 18))  # Изменяем шрифт
        self.lblPer.setGeometry(QtCore.QRect(550, 150, 530, 50))  # Меняем размер и положение
        self.lblPer.setText("количество переменных")  # Меняем текст
        self.lblPer.setStyleSheet("color: #C71585")  # меняем цвет текста

        self.lePer = QLineEdit(self)
        self.lePer.setFont(QtGui.QFont('Century Gothic', 15))  # Изменяем шрифт.
        self.lePer.setGeometry(QtCore.QRect(925, 160, 50, 35))  # Меняем размер и положение.
        self.lePer.setStyleSheet("color: #7f4355")  # меняем цвет текста
        self.lePer.setValidator(self.validatorInt)  # разрешается ввод только целых чисел

        self.btnContin = QPushButton(self)
        self.btnContin.setText("Продолжить")  # Меняем текст
        self.btnContin.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
        self.btnContin.setGeometry(QtCore.QRect(250, 230, 500, 50))  # Меняем размер и положение.
        self.btnContin.setStyleSheet("""
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
        self.btnContin.clicked.connect(self.btnContinClick)

        self.btnCleanFirst = QPushButton(self)  # Создаём кнопку Очистить
        self.btnCleanFirst.setText("Очистить")  # Меняем текст
        self.btnCleanFirst.setFont(QtGui.QFont('Century Gothic', 13))  # Изменяем шрифт.
        self.btnCleanFirst.setGeometry(QtCore.QRect(800, 235, 140, 40))  # Меняем размер и положение.
        self.btnCleanFirst.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(248, 143, 143, 0.5);
                            color: #000000;
                            border-radius: 20px;
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
        self.btnCleanFirst.clicked.connect(self.btnCleanFirstClick)

        self.btnExample = QPushButton(self)
        self.btnExample.setText("Пример")  # Меняем текст
        self.btnExample.setFont(QtGui.QFont('Century Gothic', 13))  # Изменяем шрифт.
        self.btnExample.setGeometry(QtCore.QRect(550, 20, 240, 40))  # Меняем размер и положение.
        self.btnExample.setStyleSheet("""
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

        self.btnExample.clicked.connect(self.btnExampleClick)  # подключаем кнопку "Пример" к слоту

        self.btnInfo = QPushButton(self)
        self.btnInfo.setText("Справка")  # Меняем текст
        self.btnInfo.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
        self.btnInfo.setGeometry(QtCore.QRect(800, 20, 200, 40))  # Меняем размер и положение.
        self.btnInfo.setStyleSheet("""
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

        self.btnInfo.clicked.connect(self.btnInfoClick)     # подключаем кнопку "Справка" к слоту

        self.frame = QFrame(self)   # создаём псевдо-область, которая при нажатии будет удаляться и создаваться новая
        self.frame.hide()   # скроем псевдо-область
        self.btnMain = QPushButton(self)     # создаём кнопку "Решить" заранее
        self.btnMain.hide()      # скроем пока кнопку "Решить"


    # Функция, вызывающая диалоговое окно "Справка"
    def btnInfoClick(self):
        formInfo = FormInfo(self)
        formInfo.exec_()

    def btnCleanFirstClick(self):
        self.leOgr.setText('')  # очищаем поле "кол-во ограничений"
        self.lePer.setText('')  # очищаем поле "кол-во переменных"

    # Функция, решающая пример задачи
    def btnExampleClick(self):
        self.leOgr.setText('4')     # заполняем поле "кол-во ограничений"
        self.lePer.setText('3')     # заполняем поле "кол-во переменных"
        self.btnContinClick()   # вызываем функцию для ввода данных

        ogrExample = [['4', '2', '5', '6'], ['1,6', '4', '2', '9'], ['24', '36', '42', '6'], ['2', '1', '1,6', '0,2']]  # ограничения
        wExample = ['6', '6', '8']  # крит.фун.

        # Устанавливаем левую часть ограничений
        for i in range(len(ogrExample)):    # пробегаемся по строкам
            for j in range(len(ogrExample[0])-1):   # пробегаемся почти по всем столбцам
                self.gridLayout.itemAtPosition(i, j).widget().setText(ogrExample[i][j])
        # Устанавливаем знаки и правую часть ограничений
        for i in range(len(ogrExample)):
            self.gridLayout.itemAtPosition(i, 3).widget().setCurrentIndex(0)   # по-умолчанию ставим "⩽"
            self.gridLayout.itemAtPosition(i, 4).widget().setText(ogrExample[i][-1])
        # Устанавливаем крит.функ. и значение MAX/MIN
        for i in range(len(wExample)):
            self.gridLayout.itemAtPosition(4, i).widget().setText(wExample[i])
        self.gridLayout.itemAtPosition(4, 4).widget().setCurrentIndex(0)  # по-умолчанию ставим "MAX"

        # Запускаем функцию, открывающую окно с решением
        self.toSimplexData()


    # Функция, открывающая поля ввода ограничений и крит.функ.
    def btnContinClick(self):

        if self.leOgr.text() != '' and self.lePer.text() != '':
            self.frame.deleteLater()
            self.frame = QFrame(self)
            self.setGeometry(50, 50, 1030, 910)     # делаем главное окно больше по высоте
            self.frame.show()   # показываем скрытую область
            self.btnMain.show()  # показываем скрытую кнопку "Решить"

            self.kol_str = int(self.leOgr.text())
            self.kol_stol = int(self.lePer.text())

            self.frame.setGeometry(QtCore.QRect(65, 330, 900, 450))  # Меняем размер и положение.
            self.frame.setStyleSheet("background-color: rgba(230,230,230,0.4); border-radius: 20px")
            self.gridLayout = QGridLayout()  # Размещение виджетов по сетке.

            for i in range(self.kol_str):
                for j in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. в ограничениях).
                    le = QLineEdit()
                    le.setFixedHeight(35)
                    le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                    le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                    self.gridLayout.addWidget(le, i, j)

                self.cbZnak = QComboBox()
                self.cbZnak.setFixedHeight(30)
                self.cbZnak.setFixedWidth(50)
                self.cbZnak.setStyleSheet("border-radius: 10px")
                self.cbZnak.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт.
                self.cbZnak.addItem("⩽")
                self.cbZnak.addItem("=")
                self.cbZnak.addItem("⩾")
                self.gridLayout.addWidget(self.cbZnak, i, self.kol_stol)  # Вставляем cbZnak ("<=", "=", ">=").

                le = QLineEdit()
                le.setFixedHeight(35)
                le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                self.gridLayout.addWidget(le, i, self.kol_stol + 1)  # Вставляем QLineEdit (свободные члены).


            for i in range(self.kol_stol):  # Вставляем QLineEdit (коэфф. крит. функции).
                le = QLineEdit()
                le.setFont(QtGui.QFont('Century Gothic', 14))  # Изменяем шрифт
                le.setStyleSheet("margin-top: 30px")
                le.setValidator(self.validatorFloat)  # разрешается ввод только чисел
                self.gridLayout.addWidget(le, self.kol_str, i)

            self.lblStrel = QLabel()
            self.lblStrel.setText(' 🠖')
            self.lblStrel.setFixedHeight(60)
            self.lblStrel.setStyleSheet("border-radius: 10px; margin-top: 30px")
            self.lblStrel.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
            self.gridLayout.addWidget(self.lblStrel, self.kol_str, self.kol_stol)  # Вставляем '🠖'.

            self.cbMaxOrMin = QComboBox()
            self.cbMaxOrMin.setFixedHeight(70)
            self.cbMaxOrMin.setFixedWidth(80)
            self.cbMaxOrMin.setFont(QtGui.QFont('Century Gothic', 12))  # Изменяем шрифт.
            self.cbMaxOrMin.addItem("MAX")
            self.cbMaxOrMin.addItem("MIN")
            self.cbMaxOrMin.setStyleSheet("border-radius: 10px; margin-top: 30px; padding-left: 15px")
            # Вставляем QComboBox ("max", "min").
            self.gridLayout.addWidget(self.cbMaxOrMin, self.kol_str, self.kol_stol + 1)


            self.frame.setLayout(self.gridLayout)

            self.btnMain.setText("Решение")  # Меняем текст
            self.btnMain.setFont(QtGui.QFont('Century Gothic', 16))  # Изменяем шрифт.
            self.btnMain.setGeometry(QtCore.QRect(125, 825, 670, 50))  # Изменяем размер и положение
            self.btnMain.setStyleSheet("""
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

            self.btnMain.clicked.connect(self.toSimplexData)

            self.btnCleanSecond = QPushButton(self)
            self.btnCleanSecond.setText("Очистить")  # Меняем текст
            self.btnCleanSecond.setFont(QtGui.QFont('Century Gothic', 13))  # Изменяем шрифт.
            self.btnCleanSecond.setGeometry(QtCore.QRect(840, 830, 140, 40))  # Меняем размер и положение.
            self.btnCleanSecond.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgba(248, 143, 143, 0.7);
                                        color: #000000;
                                        border-radius: 20px;
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
            self.btnCleanSecond.clicked.connect(self.btnCleanSecondClick)
            self.btnCleanSecond.show()  # показываем кнопку


    # Функция, очищающая поля ввода
    def btnCleanSecondClick(self):
        # Очищаем левую часть ограничений
        for i in range(int(self.kol_str)):  # пробегаемся по строкам
            for j in range(int(self.kol_stol)):  # пробегаемся почти по всем столбцам
                self.gridLayout.itemAtPosition(i, j).widget().setText('')
        # Устанавливаем знаки и правую часть ограничений
        for i in range(int(self.kol_str)):
            self.gridLayout.itemAtPosition(i, int(self.kol_stol)).widget().setCurrentIndex(0)  # по-умолчанию ставим "⩽"
            self.gridLayout.itemAtPosition(i, int(self.kol_stol)+1).widget().setText('')
        # Устанавливаем крит.функ. и значение MAX/MIN
        for i in range(int(self.kol_stol)):
            self.gridLayout.itemAtPosition(int(self.kol_str), i).widget().setText('')
        self.gridLayout.itemAtPosition(int(self.kol_str), int(self.kol_stol)+1).widget().setCurrentIndex(0)  # по-умолчанию ставим "MAX"

    # Функция, открывающая окно Решение
    def toSimplexData(self):
        formOtvet = FormOTVET(self)     # создаём объект класса FormOTVET (открываем окно с Решением)
        formOtvet.exec_()



class FormInfo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FormInfo, self).__init__(parent)

        self.setGeometry(930, 80, 965, 900)
        self.setWindowTitle('Справка по Симплекс-методу')
        self.setWindowIcon(QtGui.QIcon('InfoIco.svg'))    # Иконка окна
        # градиентный фон
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(240, 160, 160))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        self.formLayout = QFormLayout(self)     # создаём контейнер для виджетов


        self.teInfo1 = QTextEdit(self)       # создаём текстовую форму
        self.teInfo1.setReadOnly(True)  # Только чтение.
        self.teInfo1.setFixedHeight(380)     # фиксируем высоту
        self.teInfo1.setFixedWidth(895)      # фиксируем ширину
        self.teInfo1.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.teInfo1.setStyleSheet("""
                        QTextEdit {
                            background-color: rgba(230,230,230,0.6);
                            border-radius: 10px;
                            padding: 10px;
                        }
                        """)  # внешнее оформление (установка стиля)

        self.teInfo1.setHtml(
            "<font color='black' size='8' style='white-space: pre-wrap'><b>                         Что такое Симплекс-метод?</b></font>"
            "<hr/>"
            "<font color='black' size='5' style='white-space: pre-wrap'>\n    В симплекс-методе реализуется упорядоченный процесс, при котором, начиная "
            "с некоторой исходной допустимой угловой точки осуществляются последовательные переходы от одной допустимой "
            "экстремальной точки к другой до тех пор, пока не будет найдена точка, соответствующая оптимальному решению.\n\n</font>"
            "<font color='black' size='5' style='white-space: pre-wrap'>    В задаче имеется n переменных и m независимых линейных ограничений, заданных "
            "в форме уравнений. Известно, что оптимальное решение (если такое имеется) достигается в одной из опорных "
            "точек (вершин ОДР), где по крайней мере <b>k=n-m</b> из переменных равны нулю. Выбираются какие-то <b>k</b> переменных "
            "в качестве свободных и выражаются через них остальные m базисных переменных. Решение может быть допустимым "
            "или недопустимым. Оно допустимо, если все свободные члены неотрицательны.</font>"
        )
        self.formLayout.addWidget(self.teInfo1)      # добавляем виджет в контейнер

        self.teInfo2 = QTextEdit(self)  # создаём текстовую форму
        self.teInfo2.setReadOnly(True)  # Только чтение.
        self.teInfo2.setFixedHeight(430)     # фиксируем высоту
        self.teInfo2.setFixedWidth(895)      # фиксируем ширину
        self.teInfo2.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.teInfo2.setStyleSheet("""
                                QTextEdit {
                                    background-color: rgba(230,230,230,0.6);
                                    border-radius: 10px;
                                    padding: 10px;
                                }
                                """)  # внешнее оформление (установка стиля)

        self.teInfo2.setHtml(
            "<font color='black' size='8' style='white-space: pre-wrap'><b>                                 Алгоритм решения:</b></font>"
            "<hr/>"
            "<font color='black' size='5' style='white-space: pre-wrap'>\n"
            "  1. Приводим ЗЛП к стандартному (каноническому) виду.\n\n"
            "  2. Находим начальное базисное решение.\n\n"
            "     2.1   Выделяем свободные и базисные переменные.\n"
            "     2.2   Переразрешаем систему относительно выбранного базиса (используем алгоритм Гаусса-Жордана).\n"
            "     2.3   Приравниваем свободные переменные 0, находим базисные переменные и значение критериальной функции.\n\n"
            "  Все элементы решения (полученные коэффициенты при переменных в ограничениях, "
            "значение критериальной функции и вектор решения) записываем в виде начальной симплекс-таблицы (Таблица 1):"
        )
        self.formLayout.addWidget(self.teInfo2)  # добавляем виджет в контейнер

        self.pixmap = QtGui.QPixmap("1.png")  # загружаем картинку
        self.pixmap = self.pixmap.scaledToWidth(900)
        self.img1 = QLabel(self)  # создаём холст для картинки
        self.img1.setPixmap(self.pixmap)  # передаём холсту картинку
        self.img1.setGeometry(QtCore.QRect(50, 700, 550, 580))  # меняем размер и положение
        self.formLayout.addWidget(self.img1)  # добавляем виджет в контейнер

        self.teInfo3 = QTextEdit(self)  # создаём текстовую форму
        self.teInfo3.setReadOnly(True)  # Только чтение.
        self.teInfo3.setFixedHeight(840)  # фиксируем высоту
        self.teInfo3.setFixedWidth(895)  # фиксируем ширину
        self.teInfo3.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.teInfo3.setStyleSheet("""
                                        QTextEdit {
                                            background-color: rgba(230,230,230,0.6);
                                            border-radius: 10px;
                                            padding: 10px;
                                        }
                                        """)  # внешнее оформление (установка стиля)

        self.teInfo3.setHtml(
            "<font color='black' size='5' style='white-space: pre-wrap'>"
            "  3. Проверяем начальное базисное решения на опорность (принадлежность ОДР). "
            "Проверяем все элементы столбца <b>B</b> - они должны быть неотрицательными.\n\n"
            "     3.1   Условие неотрицательности не выполняется. Решение базисное, но не опорное, не принадлежит ОДР.\n"
            "<b>     Применяем алгоритм поиска базисного опорного решения:</b> \n"
            "           1) Выбираем в столбце свободных членов <b>B</b> минимальный из отрицательных элементов. "
            "В соответствующей ему строке также выбираем наименьший отрицательный элемент. "
            "Этот столбец принимаем за разрешающий. Если таких элементов нет, значит нет решения ЗЛП "
            "т.е. при совместной системе ограничений вся ОДР не соответствует положительности переменных.\n"
            "           2) В разрешающем столбце выбираем элементы имеющие одинаковый знак с соответствующим свободным членом (правая часть ограничений) и ищем отношением к ним свободных членов. "
            "Из этих отношений выбираем минимальное. Эта строка будет разрешающей.\n"
            "           3) Проводим процедуру однократного замещения – взаимообмен переменных. "
            "(Переразрешаем систему относительно измененного базиса).\n"
            "           4) Процедура итерационная. Проводится до тех пор пока все переменные в решении не станут неотрицательные. "
            "Т.е. мы упорядоченно, целенаправленно «спускаемся» на ОДР.\n\n"
            "     3.2   Условие неотрицательности выполняется. Переходим к следующему пункту.\n\n"
            "  4. Проверка полученного базисного опорного решения на оптимальность.\n"
            "    Введем понятие: <b>D</b> – оценка переменной относительно выбранного базиса: <b>D=Z-C</b>\n\n"
            "<b>  Критерий оптимальности:</b> если среди оценок переменных относительно выбранного базиса D в задаче максимизации нет отрицательных"
            " (в задаче минимизации нет положительных), то полученное базисное решение оптимально (Таблица № 2).\n\n"
            "<b>  Замечание:</b> оценки базисных переменных всегда равны 0.\n\n"
            "  Если решение не оптимально (отрицательные оценки есть), то переходим к смежной точке."
            "Смежные точки отличаются одной базисной и одной свободной переменной.</font>"
        )
        self.formLayout.addWidget(self.teInfo3)  # добавляем виджет в контейнер

        self.pixmap = QtGui.QPixmap("2.png")  # загружаем картинку
        self.pixmap = self.pixmap.scaledToWidth(900)
        self.img2 = QLabel(self)  # создаём холст для картинки
        self.img2.setPixmap(self.pixmap)  # передаём холсту картинку
        #self.img2.setGeometry(QtCore.QRect(50, 700, 550, 580))  # меняем размер и положение
        self.formLayout.addWidget(self.img2)  # добавляем виджет в контейнер

        self.teInfo4 = QTextEdit(self)  # создаём текстовую форму
        self.teInfo4.setReadOnly(True)  # Только чтение.
        self.teInfo4.setFixedHeight(400)  # фиксируем высоту
        self.teInfo4.setFixedWidth(895)  # фиксируем ширину
        self.teInfo4.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.teInfo4.setStyleSheet("""
                                                QTextEdit {
                                                    background-color: rgba(230,230,230,0.6);
                                                    border-radius: 10px;
                                                    padding: 10px;
                                                }
                                                """)  # внешнее оформление (установка стиля)

        self.teInfo4.setHtml(
            "<font color='black' size='5' style='white-space: pre-wrap'>"
            "  5. Определяем включаемую в базис переменную (при включении в базис переменная увеличивается, становится отличной от нуля). "
            "Включаемой в базис переменной соответствует наибольшая по модулю отрицательная оценка <b>D</b> (в задаче максимизации). "
            "В задаче минимизации должны остаться только отрицательные оценки, поэтому выбираем наибольшую положительную оценку. (Таблица 2)\n\n"
            "  6. Условие допустимости. Определяем исключаемую из базиса переменную (т.е ту с которой поменяется местами включаемая переменная). "
            "В качестве таковой выбираем ту переменную текущего базиса, которая первой обращается в ноль при увеличении включаемой переменной вплоть до значения, соответствующего смежной базисной точке.\n"
            "Для этого в разрешающем столбце среди коэффициентов в ограничениях выбираем положительные элементы и находим отношения к ним свободных членов (правых частей ограничений). "
            "Будем обозначать это отношение  <b>𝜃</b>. Из этих отношений выбираем минимальное (Таблица 3). "
            "Переменная ему соответствующая будет исключаемой из базиса, а строка разрешающей.</font>"
        )
        self.formLayout.addWidget(self.teInfo4)  # добавляем виджет в контейнер

        self.pixmap = QtGui.QPixmap("3.png")  # загружаем картинку
        self.pixmap = self.pixmap.scaledToWidth(900)
        self.img3 = QLabel(self)  # создаём холст для картинки
        self.img3.setPixmap(self.pixmap)  # передаём холсту картинку
        # self.img3.setGeometry(QtCore.QRect(50, 700, 550, 580))  # меняем размер и положение
        self.formLayout.addWidget(self.img3)  # добавляем виджет в контейнер

        self.teInfo5 = QTextEdit(self)  # создаём текстовую форму
        self.teInfo5.setReadOnly(True)  # Только чтение.
        self.teInfo5.setFixedHeight(280)  # фиксируем высоту
        self.teInfo5.setFixedWidth(895)  # фиксируем ширину
        self.teInfo5.setFont(QtGui.QFont('Arial'))  # Изменяем шрифт.
        self.teInfo5.setStyleSheet("""
                                                        QTextEdit {
                                                            background-color: rgba(230,230,230,0.6);
                                                            border-radius: 10px;
                                                            padding: 10px;
                                                        }
                                                        """)  # внешнее оформление (установка стиля)

        self.teInfo5.setHtml(
            "<font color='black' size='5' style='white-space: pre-wrap'>  7. Переразрешаем задачу "
            "относительно измененного базиса – проводим процедуру однократного замещения.\n" 
            "Проводим итерационные вычисления до получения оптимального решения.\n\n"
            "  Таблица 3 соответствует полному и окончательному виду симплекс-таблицы. "
            "Элементы таблицы, выделенные желтым цветом, на каждой итерации могут находиться по процедуре Гаусса-Жордана. "
            "Для проверки (на начальных этапах изучения и для отладки программы) необходимо оценки и значение критериальной функции <b>W</b> искать еще и по формулам. "
            "Значение <b>𝜃</b> ищется всегда только по формуле и для удобства представления заносится в симплекс-таблицу.</font>"
        )
        self.formLayout.addWidget(self.teInfo5)  # добавляем виджет в контейнер


        self.w = QWidget(self)      # создаём общий виджет (нужно для QScrollArea)
        self.w.setLayout(self.formLayout)   # передаём виджету наш контейнер

        self.scroll = QScrollArea(self)     # создаём возможность скролла
        self.scroll.setWidget(self.w)   # наделяем наш общий виджет функцией скролла
        self.scroll.setWidgetResizable(True)    # позволяем расстягивать виджет
        self.scroll.setGeometry(5, 5, 955, 880)   # положение и размер




# Класс окна с Решением задачи
class FormOTVET(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FormOTVET, self).__init__(parent)
        self.setGeometry(200, 80, 1400, 900)
        self.setWindowTitle('Решение задачи')
        self.setWindowIcon(QtGui.QIcon('MainIco.ico'))    # Иконка окна
        # градиентный фон
        p = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor(240, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(240, 160, 160))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(p)

        self.teOTVET = QTextEdit(self)
        self.teOTVET.setReadOnly(True)  # Только чтение.
        self.teOTVET.setGeometry(QtCore.QRect(10, 10, 1380, 880))  # Меняем размер и положение.
        self.teOTVET.setFont(QtGui.QFont('Consolas', 12))  # Изменяем шрифт.
        self.teOTVET.setStyleSheet("""
                QTextEdit {
                    background-color: rgba(230,230,230,0.7);
                    border-radius: 10px;
                    padding: 20px;
                }
                """)    # внешнее оформление (установка стиля)

        # Функция, вызывающая обработчик-сборщик введённых данных
        OTVET = SimplexData(win.kol_str, win.kol_stol, win.gridLayout)
        self.teOTVET.setText(OTVET)    # вставляем решение в окошко для текста






app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())
