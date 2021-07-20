
""" Алгоритм СИМПЛЕКС-МЕТОДА """

from fractions import Fraction
import numpy as np
import copy
from tabulate import tabulate   # вывод в виде таблиц

def SimplexMethod(SimplexOgr, SimplexW, max_or_min):

    # Создаём заголовки (headers) для таблицы
    tabHeaders = []
    for i in range(len(SimplexW)):
        tabHeaders.append('X'+str(i+1))     # добавляем иксы
    tabHeaders.append('B')  # добавляем B


    OTVET = ''  # здесь будут все шаги решения

    # ИСХОДНАЯ МАТРИЦА
    OTVET += ('\nИсходная матрица...\n')
    OTVET += (tabulate(tabular_data=SimplexOgr, headers=tabHeaders, tablefmt="fancy_grid"))   # вывод в виде таблицы в нужном формате
    OTVET += ('\n\n')


    """ НАЧАЛЬНОЕ БАЗИСНОЕ РЕШЕНИЕ """
    # Находим базисные переменные. Минор матрицы, составленной из этих переменных, не должен быть равен 0.

    allNumsBaz = []  # в список allNumsBaz будут занесены все последовательности индексов столбцов матрицы

    for i in range(10**(len(SimplexOgr)-1), 10**len(SimplexOgr)):  # пробегаем диапозон от 1000 до 10000 (когда нужно 4 баз.пер.)
        nums = list(str(i))     # представляем число в виде массиве (разбиваем число на цифры)
        # Выставляем ограничения на первый и последний элементы списка
        if int(nums[0]) <= (len(SimplexOgr[0]))-len(nums) and int(nums[-1]) <= len(SimplexOgr[0])-1:
            counter = 0     # счётчик успехов
            for j in range(len(nums)-1):    # пробегаемся по соседним парам
                if nums[j] < nums[j+1]:     # если каждая рассматриваемая цифра меньше следующей, то
                    counter += 1    # увеличиваем значение счётчика
            if counter == len(nums)-1:  # если последовательность выполняет все условия, то
                allNumsBaz.append(nums)  # заносим её в список с последовательностями

    # Теперь проверяем каждый вариант последовательности из списка allNumsBaz. (пока не найдётся подходящий)
    # Если определитель, составленный из столбцов, будет не равен 0, то опорное решение найдено.
    Num_baz = None  # здесь будет список с базисными переменными
    for i in range(len(allNumsBaz)):
        MinorSimplexOgr = []    # здесь будет находится квадратная матрица, составленная из определённых столбцов
        for j in range(len(SimplexOgr)):
            MinorSimplexOgr.append([])
            for k in range(len(SimplexOgr)):
                MinorSimplexOgr[j].append(int(SimplexOgr[k][int(allNumsBaz[i][j])-1]))  # добавляем элемент из нужного столбца

        if int(np.linalg.det(np.array(MinorSimplexOgr))) != 0:  # если определитель получившейся матрицы не равен 0, то
            OTVET += ('Базисные переменные найдены:' + ' ')
            Num_baz = allNumsBaz[i]     # список с базесными переменными

            for j in range(len(SimplexOgr)):
                OTVET += ('X' + str(allNumsBaz[i][j]) + ' ')
            OTVET += ('\n')
            break   # если последовательность найдена, то выходим из цикла (заканчиваем поиск)


    # Создаём новую матрицу (на основе SimplexOgr), в которой столбцы с базисными переменными находятся в начале
    firstBazisSimplexOgr = []
    for i in range(len(SimplexOgr)):  # пробегаемся по строкам
        firstBazisSimplexOgr.append([])
        for j in range(len(SimplexOgr[0])):    # пробегаемся по столбцам
            if j < len(Num_baz):  # если рассматриваются базисные стобцы, то
                firstBazisSimplexOgr[i].append(SimplexOgr[i][int(Num_baz[j])-1])     # заполняем именно базисными столбцами
            else:   # если закончилось рассмотрение базисных столбцов, то
                firstBazisSimplexOgr[i].append(SimplexOgr[i][j])  # заполняем оставшимися столбцами

    # Переставляем заголовки (headers) для таблицы
    firstBazisTabHeaders = []
    for i in range(len(tabHeaders)-1):
        if i < len(Num_baz):  # если рассматриваются базисные стобцы, то
            firstBazisTabHeaders.append('X'+str(Num_baz[i]))  # заполняем именно базисными столбцами
        else:  # если закончилось рассмотрение базисных столбцов, то
            firstBazisTabHeaders.append('X'+str(i+1))  # заполняем оставшимися столбцами
    firstBazisTabHeaders.append('B')  # добавляем B
    # Добавляем к списку с заголовками для таблицы (headers) № баз. (в начале списка)
    firstBazisTabHeaders.insert(0, "№ баз.")
    tabHeaders.insert(0, "№ баз.")


    # Находим начальное базисное решение относительно базисных переменных с помощью метода Гаусса-Жордана.

    copySimplexOgr = copy.deepcopy(firstBazisSimplexOgr)  # копия матрицы SimplexOgr

    for X in range(len(copySimplexOgr)):
        for A in range(len(firstBazisSimplexOgr)):
            if A != X:
                for B in range(len(firstBazisSimplexOgr[A])):
                    if firstBazisSimplexOgr[X][X] == 0:
                        copySimplexOgr[A][B] = 0
                    else:
                        copySimplexOgr[A][B] = Fraction(firstBazisSimplexOgr[A][B], 1) - Fraction(firstBazisSimplexOgr[A][X] * firstBazisSimplexOgr[X][B], firstBazisSimplexOgr[X][X])

        for I_1 in range(len(firstBazisSimplexOgr[X])):
            if firstBazisSimplexOgr[X][X] == 0:
                copySimplexOgr[X][X] = 0
            else:
                copySimplexOgr[X][I_1] = Fraction(firstBazisSimplexOgr[X][I_1], firstBazisSimplexOgr[X][X])

        firstBazisSimplexOgr = copy.deepcopy(copySimplexOgr)  # сохраняем изменения


    # Матрица, преобразованная методом Гаусса-Жордана
    OTVET += ('\nМатрица, преобразованная методом Гаусса-Жордана...\n')
    allTab = []
    for i in range(len(Num_baz)):
        allTab.append([Num_baz[i]] + firstBazisSimplexOgr[i])
    OTVET += (tabulate(tabular_data=allTab, headers=firstBazisTabHeaders, tablefmt="fancy_grid"))  # вывод в виде таблицы в нужном формате
    OTVET += ('\n')


    # Общее решение
    OTVET += ('\nОбщее решение...\n')
    OTVET += ('\n')
    for i in range(len(Num_baz)):
        otvet = 'X' + str(Num_baz[i]) + ' = ' + str(firstBazisSimplexOgr[i][-1])
        for j in range(len(firstBazisSimplexOgr[i])-1):
            if (j >= len(Num_baz)) and firstBazisSimplexOgr[i][j] != 0:
                if firstBazisSimplexOgr[i][j] > 0:
                    otvet += ' - ' + str(firstBazisSimplexOgr[i][j]) + ' X' + str(j+1)
                if firstBazisSimplexOgr[i][j] < 0:
                    otvet += ' + ' + str(-(firstBazisSimplexOgr[i][j])) + ' X' + str(j+1)
        OTVET += (str(otvet) + '\n')


    # Базисное решение
    OTVET += ('\nБазисное решение...\n')
    OTVET += ('\n')
    for i in range(len(Num_baz)):
        OTVET += ('X' + str(Num_baz[i]) + ' = ' + str(firstBazisSimplexOgr[i][-1]) + '\n')



    # ПРОВЕРЯЕМ НАЙДЕННОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
    opornoe = None  # если True, то опорное решение найдено; если False, то нужно находить опорное решение
    for i in firstBazisSimplexOgr:
        if i[-1] < 0:
            OTVET += ('\nНайденное базисное решение - не опорное.\n')
            opornoe = False
            break
    else:
        OTVET += ('\nНайденное базисное решение - опорное.\n')
        opornoe = True


    # Ставим столбцы матрицы в правильном порядке (до этого базисные столбцы стояли в начале)
    SimplexOgr = []     # преобразованная матрица
    for i in range(len(firstBazisSimplexOgr)):      # пробегаемся по строкам
        SimplexOgr.append([])
        for j in range(len(firstBazisSimplexOgr[0])):   # пробегаемся по столбцам
            if str(j+1) in Num_baz:
                SimplexOgr[i].append(firstBazisSimplexOgr[i][Num_baz.index(str(j+1))])
            else:
                SimplexOgr[i].append(firstBazisSimplexOgr[i][j])

    # Матрица после перестановки столбцов в правильном порядке
    OTVET += ('\nМатрица после перестановки столбцов в правильном порядке...\n')
    allTab = []
    for i in range(len(Num_baz)):
        allTab.append([Num_baz[i]] + SimplexOgr[i])
    OTVET += (tabulate(tabular_data=allTab, headers=tabHeaders, tablefmt="fancy_grid"))  # вывод в виде таблицы в нужном формате
    OTVET += ('\n')



    """ ПРОЦЕДУРА ОДНОКРАТНОГО ЗАМЕЩЕНИЯ (АЛГОРИТМ ПОИСКА БАЗИСНОГО ОПОРНОГО РЕШЕНИЯ) """
    # Если найденное базисное решение - не опорное.
    num_iter = 1  # подсчёт кол-ва итераций для процедуры однократного замещения
    while not opornoe:  # цикл выполняется пока переменная opornoe не станет равна True

        # Находим наименьшее отрицательное число в столбце свободных членов (в столбце B).
        minInB = SimplexOgr[0][-1]    # отталкиваемся от элемента первой строки
        strokWithRazStol = 0     # отталкиваемся от элемента первой строки

        for i in range(len(SimplexOgr)):     # пробегаемся по строкам
            if SimplexOgr[i][-1] < minInB:   # если новый элемент из столбца B меньше, чем текущий минимум, то
                minInB = SimplexOgr[i][-1]   # этот элемент ставится текущим минимум
                strokWithRazStol = i     # отмечаем строку, в которой находится элемент разрешающего столбца

        # Находим индекс разрешающего столбца (наименьшее отрицательное число в строке).
        minInRazStrok = SimplexOgr[strokWithRazStol][0]    # отталкиваемся от первого элемента строки
        raz_stol = 0    # отталкиваемся от первого элемента строки
        for i in range(len(SimplexOgr[0])-1):     # пробегаемся по всем столбцам кроме последнего
            if SimplexOgr[strokWithRazStol][i] < minInRazStrok:  # если новый элемент строки меньше, чем текущий минимум, то
                minInRazStrok = SimplexOgr[strokWithRazStol][i]  # этот элемент ставится текущим минимум
                raz_stol = i    # столбец отмечаем как разрешающий

        if minInRazStrok >= 0:  # если в разрешающей строке нет отрицательных элементов, то
            OTVET += ('\nНет решения ЗЛП\n')    # нет решения ЗЛП
            break

        # Находим индекс разрешающей строки (наименьшее полижетельное отношение).
        minOtnInRazStol = Fraction(copySimplexOgr[0][-1], copySimplexOgr[0][raz_stol])  # отталкиваемся от первого отношения
        raz_strok = 0  # отталкиваемся от первого отношения

        for i in range(len(SimplexOgr)):  # пробегаемся по строкам
            # если отношение больше или равно 0 и меньше отношения, от которого отталкиваемся, то
            if 0 <= Fraction(copySimplexOgr[i][-1], copySimplexOgr[i][raz_stol]) < minOtnInRazStol:
                minOtnInRazStol = Fraction(copySimplexOgr[i][-1], copySimplexOgr[i][raz_stol])  # это отношение ставится текущим минимум
                raz_strok = i     # строку отмечаем как разрешающую

        # Выполняем процедуру однократного замещения.

        # ВЫПОЛНЯЕМ ИТЕРАЦИЮ
        # Воспользуемся методом Жордана-Гаусса относительно разрешающего элемента с координатами [raz_strok, raz_stol]

        # Создадим пустую матрицу
        copySimplexOgr = []
        # Заполняем матрицу пустыми массивами
        for i in range(len(SimplexOgr)):
            copySimplexOgr.append([])

        # Начнём процедуру.
        for i in range(len(SimplexOgr)):
            for j in range(len(SimplexOgr[i])):
                if i == raz_strok:
                    if SimplexOgr[raz_strok][raz_stol] == 0:
                        copySimplexOgr[i].append('∞')
                    else:
                        copySimplexOgr[i].append(Fraction(SimplexOgr[raz_strok][j], SimplexOgr[raz_strok][raz_stol]))
                else:
                    if SimplexOgr[raz_strok][raz_stol] == 0:
                        copySimplexOgr[i].append('-∞')
                    else:
                        copySimplexOgr[i].append(SimplexOgr[i][j] -
                                             (Fraction(SimplexOgr[raz_strok][j], SimplexOgr[raz_strok][raz_stol]) *
                                              SimplexOgr[i][raz_stol]))

        # Меняем столбец № баз. так как была получена новая базисная переменная
        Num_baz[raz_strok] = str(raz_stol+1)


        # Выводим матрицу.
        OTVET += ('\n')
        allTab = []
        for i in range(len(Num_baz)):
            allTab.append([Num_baz[i]] + copySimplexOgr[i])
        OTVET += ('\nОпорное базисное решение. Итерация №' + str(num_iter) + '\n')
        OTVET += (tabulate(tabular_data=allTab, headers=tabHeaders, tablefmt="fancy_grid"))  # вывод в виде таблицы в нужном формате
        OTVET += ('\n')

        # Заменяем значения матрицы "SimplexOgr" на значения матрицы "copySimplexOgr".
        SimplexOgr = copy.deepcopy(copySimplexOgr)

        # ПРОВЕРЯЕМ НОВОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
        for i in copySimplexOgr:
            if i[-1] < 0:
                OTVET += ('\nНовое базисное решение - не опорное.\n')
                num_iter += 1
                break
        else:
            OTVET += ('\nНовое базисное решение - опорное.\n')
            opornoe = True  # выходим из цикла



    """ НАХОДИМ ПРОМЕЖУТОЧНЫЕ ХАРАКТЕРИСТИКИ """

    # НАХОДИМ Cj и Ci

    Cj = []
    Ci = []

    OTVET += ('\n' + 'Cj = ')
    for i in range(len(SimplexW)):
        Cj.append(SimplexW[i])
        OTVET += (str(Cj[-1]) + ' ')

    OTVET += ('\n' + 'Ci = ')
    for i in range(len(SimplexOgr)):
        Ci.append(SimplexW[int(Num_baz[i])-1])
        OTVET += (str(Ci[-1]) + ' ')
    OTVET += ('\n')

    # НАХОДИМ ЗНАЧЕНИЕ КРИТЕРИАЛЬНОЙ ФУНКЦИИ

    TotalW = 0
    for i in range(len(Num_baz)):
        TotalW += SimplexOgr[i][-1] * Cj[int(Num_baz[i])-1]
    OTVET += str('\n' + 'TotalW = ' + str(TotalW) + '\n')


    # НАХОДИМ И ДОБАВЛЯЕМ В МАТРИЦУ ОЦЕНКИ ПЕРЕМЕННЫХ ОТНОСИТЕЛЬНО ВЫБРАННОГО БАЗИСА

    SimplexOgr.append([])  # будем заполнять строку оценок
    for i in range(len(SimplexOgr[0]) - 1):     # пробегаемся по всем столбцам кроме последнего
        Zj = 0
        for j in range(len(Ci)):    # пробегаемся по всем строкам кроме строки с оценками
            Zj += SimplexOgr[j][i] * Ci[j]
        SimplexOgr[-1].append(Zj - Cj[i])

    SimplexOgr[-1].append(TotalW)   # добавляем в самый конец строки значение TotalW (значение крит.функ.)


    # Создаём массив, который будет содержать результат отношения свободных членов и разрешающего столбца.
    Q = []

    # Перед началом работы симплекс-метода, все значения в массиве "Q" равны "-".
    for i in range(len(SimplexOgr)-1):
        Q.append('-')

    num_iter = 0  # подсчёт кол-ва итераций для симплекс-метода

    # Добавляем к списку с заголовками для таблицы (headers) θ (в конце списка)
    tabHeaders.append('θ')



    """ ПОСЛЕДНИЙ ЭТАП АЛГОРИТМА СИМПЛЕКС-МЕТОД """

    def LastSimplexAlg(SimplexOgr, num_iter, OTVET):

        # НАХОДИМ РАЗРЕШАЮЩИЙ СТОЛБЕЦ

        minInD = None   # минимальная оценка
        maxInD = None   # максимальная оценка
        raz_stol = 0    # индекс разрешающего столбца

        if max_or_min == "MAX":     # если задача на MAX
            minInD = SimplexOgr[-1][0]    # будем отталкиваться от первой оценки
            for i in range(len(SimplexOgr[-1]) - 1):    # пробегаемся по всем оценкам (кроме TotalW)
                if SimplexOgr[-1][i] <= minInD:     # если нашли оценку меньше или равную имеющегося минимума, то
                    minInD = SimplexOgr[-1][i]  # меняем старый минимум на новый
                    raz_stol = i    # отмечаем этот столбец как разрешающий

        if max_or_min == "MIN":     # если задача на MIN
            maxInD = SimplexOgr[-1][0]  # будем отталкиваться от первой оценки
            for i in range(len(SimplexOgr[-1]) - 1):    # пробегаемся по всем оценкам (кроме TotalW)
                if SimplexOgr[-1][i] >= maxInD:   # если нашли оценку больше или равную имеющегося минимума, то
                    maxInD = SimplexOgr[-1][i]  # меняем старый максимум на новый
                    raz_stol = i    # отмечаем этот столбец как разрешающий


        # НАХОДИМ РАЗРЕШАЮЩУЮ СТРОКУ

        Q = []  # отношение свободных членов к разрешающему столбцу

        for i in range(len(SimplexOgr) - 1):    # пробегаемся по всем строкам кроме последней (кроме строки с оценками)
            if SimplexOgr[i][raz_stol] == 0:    # если элемент из разрешающего столбца равен 0, то
                Q.append('∞')   # в столбец с отношениями добавляем '∞' (так как происходит деление на 0)
            else:   # если элемент из разрешающего столбца не равен 0, то
                Q.append(Fraction(SimplexOgr[i][-1], SimplexOgr[i][raz_stol]))  # добавляем их соотношение

        minInQ = None   # минимальный положительный элемент в столбце 'θ'
        raz_strok = None  # разрешающая строка

        for i in range(len(Q)):     # Находим значение, от которого будем отталкиваться в поисках минимума
            if Q[i] != '∞':
                if Q[i] >= 0:
                    minInQ = Q[i]

        for i in range(len(Q)):
            if Q[i] <= minInQ and Q[i] >= 0:
                minInQ = Q[i]
                raz_strok = i


        # ВЫПОЛНЯЕМ ИТЕРАЦИЮ
        # Воспользуемся методом Жордана-Гаусса относительно разрешающего элемента с координатами [raz_str, raz_stol].

        # Создадим пустую матрицу.
        copySimplexOgr = []
        for i in range(len(SimplexOgr)):
            copySimplexOgr.append([])

        # Начнём процедуру.
        for i in range(len(SimplexOgr)):
            for j in range(len(SimplexOgr[i])):
                if i == raz_strok:
                    if SimplexOgr[raz_strok][raz_stol] == 0:
                        copySimplexOgr[i].append('∞')
                    else:
                        copySimplexOgr[i].append(Fraction(SimplexOgr[raz_strok][j], SimplexOgr[raz_strok][raz_stol]))
                else:
                    if SimplexOgr[raz_strok][raz_stol] == 0:
                        copySimplexOgr[i].append('-∞')
                    else:
                        copySimplexOgr[i].append(SimplexOgr[i][j] - (
                                    Fraction(SimplexOgr[raz_strok][j], SimplexOgr[raz_strok][raz_stol]) * SimplexOgr[i][raz_stol]))


        # Устанавливаем новую базисную переменную в столбец № баз.
        Num_baz[raz_strok] = str(raz_stol+1)


        # Выводим матрицу.
        OTVET += ('\nИтерация №' + str(num_iter) + '\n')
        allTab = []
        for i in range(len(Num_baz)):
            allTab.append([Num_baz[i]]+copySimplexOgr[i]+[Q[i]])
        allTab.append([''] + copySimplexOgr[-1] + [''])
        OTVET += (tabulate(tabular_data=allTab, headers=tabHeaders, tablefmt="fancy_grid"))  # вывод в виде таблицы в нужном формате
        OTVET += ('\n')


        # Заменяем значения матрицы "SimplexOgr" на значения матрицы "copySimplexOgr".
        SimplexOgr = copy.deepcopy(copySimplexOgr)
        return SimplexOgr, OTVET



    # Выводим матрицу
    OTVET += ('\nИтерация №' + str(num_iter) + '\n')
    allTab = []
    for i in range(len(Num_baz)):
        allTab.append([Num_baz[i]] + SimplexOgr[i] + [Q[i]])
    allTab.append([''] + SimplexOgr[-1] + [''])
    OTVET += (tabulate(tabular_data=allTab, headers=tabHeaders, tablefmt="fancy_grid"))  # вывод в виде таблицы в нужном формате
    OTVET += ('\n')



    # ПРОВЕРЯЕМ НАЙДЕННОЕ РЕШЕНИЕ НА ОПТИМАЛЬНОСТЬ

    TheEnd = False  # когда решение становится оптимальным TheEnd = True
    while not TheEnd:
        for i in range(len(SimplexOgr[-1]) - 1):    # пробегаемся по оценкам переменных
            if SimplexOgr[-1][i] < 0 and max_or_min == "MAX":   # если находится оценка меньше 0 при условии MAX, то
                OTVET += ('\nРешение не оптимальное.\n')
                num_iter += 1
                SimplexOgr, OTVET = LastSimplexAlg(SimplexOgr, num_iter, OTVET)    # вызываем функцию, которая переразрешает матрицу
                break   # заканчиваем просмотр оценок

            if SimplexOgr[-1][i] > 0 and max_or_min == "MIN":   # если находится оценка больше 0 при условии MIN, то
                OTVET += ('\nРешение не оптимальное.\n')
                num_iter += 1
                SimplexOgr, OTVET = LastSimplexAlg(SimplexOgr, num_iter, OTVET)     # вызываем функцию, которая переразрешает матрицу
                break   # заканчиваем просмотр оценок

        # если пробежались по всем оценкам удачно, то оптимальное решение найдено
        else:
            OTVET += ('\nРешение оптимальное.\n')
            TheEnd = True   # выходим из основного цикла



    """ ОТВЕТ """

    OTVET += ('\nОТВЕТ...\n\n')
    for i in range(len(SimplexOgr[0])):     # пробегаемся по всем столбцам
        if i == len(SimplexOgr[0])-1:
            OTVET += ('\nTotalW = ' + str(SimplexOgr[-1][-1]) + '\n')
        else:
            if str(i+1) in Num_baz:
                OTVET += ('X' + str(i+1) + ' = ' + str(SimplexOgr[Num_baz.index(str(i+1))][-1]) + '\n')
            else:
                OTVET += ('X' + str(i+1) + ' = ' + str(0) + '\n')

    print(OTVET)

    return OTVET