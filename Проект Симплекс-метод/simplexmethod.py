
""" Алгоритм СИМПЛЕКС-МЕТОДА """

from fractions import Fraction
import numpy as np
import copy
from tabulate import tabulate   # вывод в виде таблиц

def SimplexMethod(SimplexOgr, SimplexW, max_or_min):

    global sim_tab
    global num_iter
    global OTVET

    # Создаём заголовки (headers) для таблицы
    tabHeaders = []
    for i in range(len(SimplexW)):
        tabHeaders.append('X'+str(i+1))     # добавляем иксы
    tabHeaders.append('B')  # добавляем B


    OTVET = ''  # здесь будут все шаги решения

    # ИСХОДНАЯ МАТРИЦА
    OTVET += ('\nИсходная матрица...\n')
    OTVET += tabulate(tabular_data=SimplexOgr, headers=tabHeaders, tablefmt="fancy_grid")   # вывод в виде таблицы в нужном формате
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


    # Находим начальное базисное решение относительно базисных переменных с помощью метода Гаусса-Жордана.

    copySimplexOgr = copy.deepcopy(SimplexOgr)  # копия матрицы SimplexOgr

    for X in range(len(copySimplexOgr)):
        for A in range(len(SimplexOgr)):
            if A != X:
                for B in range(len(SimplexOgr[A])):
                    if SimplexOgr[X][X] == 0:
                        copySimplexOgr[A][B] = 0
                    else:
                        copySimplexOgr[A][B] = Fraction(SimplexOgr[A][B], 1) - Fraction(SimplexOgr[A][X] * SimplexOgr[X][B], SimplexOgr[X][X])

        for I_1 in range(len(SimplexOgr[X])):
            if SimplexOgr[X][X] == 0:
                copySimplexOgr[X][X] = 0
            else:
                copySimplexOgr[X][I_1] = Fraction(SimplexOgr[X][I_1], SimplexOgr[X][X])

        SimplexOgr = copy.deepcopy(copySimplexOgr)  # сохраняем изменения


    # Итоговая матрица
    OTVET += ('\nИтоговая матрица...\n')
    allTab = []
    for i in range(len(Num_baz)):
        allTab.append([Num_baz[i]] + firstBazisSimplexOgr[i])
    OTVET += tabulate(tabular_data=allTab, headers=firstBazisTabHeaders, tablefmt="fancy_grid")  # вывод в виде таблицы в нужном формате
    OTVET += ('\n')






# ================================= ОТСЮДА ПРОДОЛЖИТЬ =========================


    # Общее решение
    OTVET += ('\nОбщее решение...\n')
    OTVET += ('\n')
    for i in range(len(copySimplexOgr)):
        otvet = 'X' + str(i+1) + ' = ' + str(copySimplexOgr[i][-1])
        for j in range(len(copySimplexOgr[i])-(i+2)):
            if copySimplexOgr[i][i+(j+1)] != 0:
                if copySimplexOgr[i][i+(j+1)] > 0:
                    otvet += ' - ' + str(copySimplexOgr[i][i+(j+1)]) + ' X' + str(i+(j+1)+1)
                if copySimplexOgr[i][i+(j+1)] < 0:
                    otvet += ' + ' + str(-(copySimplexOgr[i][i+(j+1)])) + ' X' + str(i+(j+1)+1)
        OTVET += (str(otvet) + '\n')


    # Базисное решение
    OTVET += ('\nБазисное решение...\n')
    OTVET += ('\n')
    for i in range(len(copySimplexOgr)):
        OTVET += ('X' + str(i+1) + ' = ' + str(copySimplexOgr[i][-1]) + '\n')



    # ПРОВЕРЯЕМ НАЙДЕННОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
    for i_1 in copySimplexOgr:
        if i_1[-1] < 0:
            OTVET += ('\nНайденное базисное решение - не опорное.\n')
            yes_or_no = 0
            break
    else:
        OTVET += ('\nНайденное базисное решение - опорное.\n')
        yes_or_no = 1


    # Если найденное базисное решение - не опорное.
    num_iter = 1  # подсчёт кол-ва итераций для процедуры однократного замещения

    while yes_or_no != 1:

        # Находим наименьшее отрицательное число в столбце свободных членов (в столбце B).
        min_el = max(copySimplexOgr[0])
        raz_stol = 0

        for i_1 in range(len(copySimplexOgr)):
            if copySimplexOgr[i_1][-1] < min_el:
                min_el = copySimplexOgr[i_1][-1]
                raz_stol = i_1

        # Находим индекс разрешающего столбца (наименьшее отрицательное число в строке).
        min_el = max(copySimplexOgr[raz_stol])
        for i_1 in range(len(SimplexOgr[0])-1):
            if copySimplexOgr[raz_stol][i_1] < min_el:
                min_el = copySimplexOgr[raz_stol][i_1]

        raz_stol = copySimplexOgr[raz_stol].index(min_el)

        if min_el > 0:
            OTVET += ('\nНет решения ЗЛП\n')

        # Находим индекс разрешающей строки (наименьшее полижетельное отношение).
        min_el = Fraction(copySimplexOgr[0][-1], copySimplexOgr[0][raz_stol])
        raz_str = 0

        for i_1 in range(len(copySimplexOgr)):
            if 0 < Fraction(copySimplexOgr[i_1][-1], copySimplexOgr[i_1][raz_stol]) < min_el:
                min_el = Fraction(copySimplexOgr[i_1][-1], copySimplexOgr[i_1][raz_stol])
                raz_str = i_1

        # Выполняем процедуру однократного замещения.

        # ВЫПОЛНЯЕМ ИТЕРАЦИЮ
        # Воспользуемся методом Жордана-Гаусса относительно разрешающего элемента с координатами [raz_str, raz_stol].

        # Создадим пустую матрицу.
        SimplexOgr = []
        for i_1 in range(len(copySimplexOgr)):
            SimplexOgr.append([])

        # Начнём процедуру.
        for i_1 in range(len(copySimplexOgr)):
            for j_1 in range(len(copySimplexOgr[i_1])):
                if i_1 == raz_str:
                    if copySimplexOgr[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('∞')
                    else:
                        SimplexOgr[i_1].append(Fraction(copySimplexOgr[raz_str][j_1], copySimplexOgr[raz_str][raz_stol]))
                else:
                    if copySimplexOgr[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('-∞')
                    else:
                        SimplexOgr[i_1].append(copySimplexOgr[i_1][j_1] - (
                                    Fraction(copySimplexOgr[raz_str][j_1], copySimplexOgr[raz_str][raz_stol]) * copySimplexOgr[i_1][raz_stol]))

        # Выводим матрицу.
        OTVET += ('\nОпорное базисное решение. Итерация №' + str(num_iter) + '\n')
        OTVET += tabulate(tabular_data=SimplexOgr, headers=tabHeaders, tablefmt="fancy_grid")  # вывод в виде таблицы в нужном формате
        OTVET += '\n'
        # Заменяем значения матрицы "copySimplexOgr" на значения матрицы "SimplexOgr".
        copySimplexOgr = copy.deepcopy(SimplexOgr)

        # ПРОВЕРЯЕМ НОВОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
        for i_1 in copySimplexOgr:
            if i_1[-1] < 0:
                OTVET += ('\nНовое базисное решение - не опорное.\n')
                num_iter += 1
                break
        else:
            OTVET += ('\nНовое базисное решение - опорное.\n')
            yes_or_no = 1


    # НАХОДИМ ЗНАЧЕНИЕ КРИТЕРИАЛЬНОЙ ФУНКЦИИ

    W_zna = 0
    for i_1 in range(len(copySimplexOgr)):
        W_zna += copySimplexOgr[i_1][-1] * SimplexW[i_1]

    OTVET += str('\n' + 'SimplexW = ' + str(W_zna) + '\n')


    # НАХОДИМ Cj и Ci

    Cj = []
    Ci = []

    OTVET += ('\n' + 'Cj = ')
    for i_1 in range(len(SimplexW)):
        Cj.append(SimplexW[i_1])
        OTVET += (str(SimplexW[i_1]) + ' ')
    OTVET += ('\n')

    OTVET += ('\n' + 'Ci = ')
    for i_1 in range(len(copySimplexOgr)):
        Ci.append(SimplexW[i_1])
        OTVET += (str(SimplexW[i_1]) + ' ')
    OTVET += ('\n')

    sim_tab = copy.deepcopy(copySimplexOgr)  # копия матрицы copySimplexOgr


    # НАХОДИМ ОЦЕНКИ ПЕРЕМЕННЫХ ОТНОСИТЕЛЬНО ВЫБРАННОГО БАЗИСА

    sim_tab.append([])  # будем заполнять строку оценок
    for i_1 in range(len(copySimplexOgr[0]) - 1):
        Zj = 0
        for j_1 in range(len(copySimplexOgr)):
            Zj += copySimplexOgr[j_1][i_1] * Ci[j_1]
        sim_tab[-1].append(Zj - Cj[i_1])

    sim_tab[-1].append(W_zna)

    # Создаём массив, который будет содержать номера выбранных базисов.
    Num_baz = []

    # Создаём массив, который будет содержать результат отношения свободных членов и разрешающего столбца.
    Q = []

    # Перед началом работы симплекс-метода, все значения в массивах "Num_baz" и "Q" равны "-".
    for i_1 in range(len(sim_tab)-1):
        Num_baz.append('-')

    for i_1 in range(len(sim_tab)-1):
        Q.append('-')

    num_iter = 0  # подсчёт кол-ва итераций для симплекс-метода

    # Добавляем к списку с заголовками для таблицы (headers) θ (в конце списка)
    tabHeaders.append('θ')

    def sim_met():

        global sim_tab
        global num_iter
        global OTVET

        # НАХОДИМ РАЗРЕШАЮЩИЙ СТОЛБЕЦ

        if max_or_min == "MAX":
            raz_stol = max(sim_tab[-1])
            for i_1 in range(len(sim_tab[-1]) - 1):
                if sim_tab[-1][i_1] <= raz_stol:
                    raz_stol = sim_tab[-1][i_1]

        if max_or_min == "MIN":
            raz_stol = min(sim_tab[-1])
            for i_1 in range(len(sim_tab[-1]) - 1):
                if sim_tab[-1][i_1] >= raz_stol:
                    raz_stol = sim_tab[-1][i_1]

        raz_stol = sim_tab[-1].index(raz_stol)  # индекс минимального элемента в строке оценок


        # НАХОДИМ РАЗРЕШАЮЩУЮ СТРОКУ

        Q = []  # отношение свободных членов к разрешающему столбцу

        for i_1 in range(len(sim_tab) - 1):
            if sim_tab[i_1][raz_stol] == 0:
                Q.append('∞')
            else:
                Q.append(Fraction(sim_tab[i_1][-1], sim_tab[i_1][raz_stol]))

        raz_str = 0  # индекс минимального положительного элемента в столбце Q
        for i_1 in Q:
            if i_1 != '∞' and i_1 > 0:
                raz_str = i_1
                break

        for i_1 in Q:
            if i_1 != '∞':
                if 0 < i_1 <= raz_str:
                    raz_str = i_1

        raz_str = Q.index(raz_str)


        # ВЫПОЛНЯЕМ ИТЕРАЦИЮ
        # Воспользуемся методом Жордана-Гаусса относительно разрешающего элемента с координатами [raz_str, raz_stol].

        # Создадим пустую матрицу.
        SimplexOgr = []
        for i_1 in range(len(sim_tab)):
            SimplexOgr.append([])

        # Начнём процедуру.
        for i_1 in range(len(sim_tab)):
            for j_1 in range(len(sim_tab[i_1])):
                if i_1 == raz_str:
                    if sim_tab[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('∞')
                    else:
                        SimplexOgr[i_1].append(Fraction(sim_tab[raz_str][j_1], sim_tab[raz_str][raz_stol]))
                else:
                    if sim_tab[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('-∞')
                    else:
                        SimplexOgr[i_1].append(sim_tab[i_1][j_1] - (
                                    Fraction(sim_tab[raz_str][j_1], sim_tab[raz_str][raz_stol]) * sim_tab[i_1][raz_stol]))

        # Заполняем столбец Num_baz.
        for i_1 in range(len(SimplexOgr[0]) - 1):
            f = []  # столбец
            for j_1 in range(len(SimplexOgr)):
                if SimplexOgr[j_1][i_1] == 0 or SimplexOgr[j_1][i_1] == 1:
                    f.append(SimplexOgr[j_1][i_1])

            if sum(f) == 1 and len(f) == len(SimplexOgr):
                Num_baz[f.index(1)] = i_1 + 1

        # Выводим матрицу.
        OTVET += ('\nИтерация №' + str(num_iter) + '\n')
        allTab = []
        for i in range(len(Num_baz)):
            allTab.append([Num_baz[i]]+SimplexOgr[i]+[Q[i]])
        allTab.append([''] + SimplexOgr[-1] + [''])
        OTVET += tabulate(tabular_data=allTab, headers=tabHeaders, tablefmt="fancy_grid")  # вывод в виде таблицы в нужном формате
        OTVET += ('\n')


        # Заменяем значения матрицы "sim_tab" на значения матрицы "SimplexOgr".
        sim_tab = copy.deepcopy(SimplexOgr)


    # ПРОВЕРЯЕМ НАЙДЕННОЕ РЕШЕНИЕ НА ОПТИМАЛЬНОСТЬ

    X = 0
    while X == 0:
        for i_1 in range(len(sim_tab[-1]) - 1):
            if sim_tab[-1][i_1] < 0 and max_or_min == "MAX":
                OTVET += ('\nРешение не оптимальное.\n')
                num_iter += 1
                sim_met()
                break

            if sim_tab[-1][i_1] > 0 and max_or_min == "MIN":
                OTVET += ('\nРешение не оптимальное.\n')
                num_iter += 1
                sim_met()
                break
        else:
            OTVET += ('\nРешение оптимальное.\n')
            X = 1


    """ОТВЕТ"""

    ans = []

    for i_1 in range(len(sim_tab[0]) - 1):
        ans.append(0)

    for i_1 in range(len(Num_baz)):
        if Num_baz[i_1] != "-":
            ans[Num_baz[i_1] - 1] = sim_tab[i_1][-1]

    OTVET += ('\nОТВЕТ...\n\n')
    for i_1 in range(len(ans) + 1):
        if i_1 == len(ans):
            OTVET += ('SimplexW' + ' = ' + str(sim_tab[-1][-1]) + '\n')
        else:
            OTVET += ('X' + str(i_1 + 1) + ' = ' + str(ans[i_1]) + '\n')

    #print(OTVET)

    return OTVET