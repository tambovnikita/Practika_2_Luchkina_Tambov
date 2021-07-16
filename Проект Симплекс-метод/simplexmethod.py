
""" Алгоритм СИМПЛЕКС-МЕТОДА """

from fractions import Fraction
import numpy as np
import copy

def SimplexMethod(SimplexOgr, SimplexW, max_or_min):

    global sim_tab
    global num_iter
    global OTVET

    OTVET = ''

    # НАЧАЛЬНОЕ БАЗИСНОЕ РЕШЕНИЕ
    # Находим базисные переменные. Минор матрицы, составленной из этих переменных, не должен быть равен 0.
    # В списке maybe_num_baz будут находится индексы столбцов матрицы SimplexOgr, которые возможно будут являться базисными.

    maybe_num_baz = []
    for i_1 in range(10**(len(SimplexOgr)-1), 10**len(SimplexOgr)):
        nums = list(str(i_1))
        counter = 0
        for j_1 in range(len(nums)):
            if int(nums[0]) <= len(SimplexOgr[0])-(len(SimplexOgr)-2) and int(nums[-1]) <= len(SimplexOgr[0])-1:
                if j_1 != len(nums)-1:
                    if nums[j_1] < nums[j_1+1]:
                        counter += 1

        if counter == len(SimplexOgr)-1:
            maybe_num_baz.append(nums)

    # Теперь проверяем, минор матрицы, составленной из столбцов, будет равен 0 или нет.
    for i_1 in range(len(maybe_num_baz)):
        mat2 = []
        for j_1 in range(len(SimplexOgr)):
            mat2.append([])
            for k_1 in range(len(SimplexOgr)):
                mat2[j_1].append(int(SimplexOgr[k_1][int(maybe_num_baz[i_1][j_1])-1]))

        baz = np.array(mat2)

        if int(np.linalg.det(baz)) != 0:
            OTVET += ('Базисное переменные найдены:' + ' ')
            for j_1 in range(len(SimplexOgr)):
                OTVET += ('X' + str(maybe_num_baz[i_1][j_1]) + ' ')
            OTVET += ('\n')
            break

    # Находим начальное базисное решение с помощью метода Гаусса-Жордана.
    mat2 = copy.deepcopy(SimplexOgr)  # копия матрицы mat

    for X_1 in range(len(SimplexOgr)):

        SimplexOgr = copy.deepcopy(mat2)  # копия матрицы mat2

        for A_1 in range(len(SimplexOgr)):
            if A_1 != X_1:
                for B_1 in range(len(SimplexOgr[A_1])):
                    if SimplexOgr[X_1][X_1] == 0:
                        mat2[A_1][B_1] = 0
                    else:
                        mat2[A_1][B_1] = Fraction(SimplexOgr[A_1][B_1], 1) - Fraction(SimplexOgr[A_1][X_1] * SimplexOgr[X_1][B_1], SimplexOgr[X_1][X_1])

        for I_1 in range(len(SimplexOgr[X_1])):
            if SimplexOgr[X_1][X_1] == 0:
                mat2[X_1][X_1] = 0
            else:
                mat2[X_1][I_1] = Fraction(SimplexOgr[X_1][I_1], SimplexOgr[X_1][X_1])

    # Итоговая матрица

    OTVET += ('\nИтоговая матрица...\n')
    OTVET += ('\n')
    for i_1 in range(len(mat2)):
        for j_1 in range(len(mat2[i_1])):
            if j_1 == len(mat2[i_1])-1:
                OTVET += ('|' + ' ')
                OTVET += (str(mat2[i_1][j_1]))
            else:
                OTVET += (str(mat2[i_1][j_1]) + ' ')
        OTVET += ('\n')

    # Общее решение

    OTVET += ('\nОбщее решение...\n')
    OTVET += ('\n')
    for i_1 in range(len(mat2)):
        otvet = 'X' + str(i_1+1) + ' = ' + str(mat2[i_1][-1])
        for j_1 in range(len(mat2[i_1])-(i_1+2)):
            if mat2[i_1][i_1+(j_1+1)] != 0:
                if mat2[i_1][i_1+(j_1+1)] > 0:
                    otvet += ' - ' + str(mat2[i_1][i_1+(j_1+1)]) + ' X' + str(i_1+(j_1+1)+1)
                if mat2[i_1][i_1+(j_1+1)] < 0:
                    otvet += ' + ' + str(-(mat2[i_1][i_1+(j_1+1)])) + ' X' + str(i_1+(j_1+1)+1)
        OTVET += (str(otvet) + '\n')

    # Базисное решение

    OTVET += ('\nБазисное решение...\n')
    OTVET += ('\n')
    for i_1 in range(len(mat2)):
        OTVET += ('X' + str(i_1+1) + ' = ' + str(mat2[i_1][-1]) + '\n')


    # ПРОВЕРЯЕМ НАЙДЕННОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
    for i_1 in mat2:
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
        min_el = max(mat2[0])
        raz_stol = 0

        for i_1 in range(len(mat2)):
            if mat2[i_1][-1] < min_el:
                min_el = mat2[i_1][-1]
                raz_stol = i_1

        # Находим индекс разрешающего столбца (наименьшее отрицательное число в строке).
        min_el = max(mat2[raz_stol])
        for i_1 in range(len(SimplexOgr[0])-1):
            if mat2[raz_stol][i_1] < min_el:
                min_el = mat2[raz_stol][i_1]

        raz_stol = mat2[raz_stol].index(min_el)

        if min_el > 0:
            OTVET += ('\nНет решения ЗЛП\n')

        # Находим индекс разрешающей строки (наименьшее полижетельное отношение).
        min_el = Fraction(mat2[0][-1], mat2[0][raz_stol])
        raz_str = 0

        for i_1 in range(len(mat2)):
            if 0 < Fraction(mat2[i_1][-1], mat2[i_1][raz_stol]) < min_el:
                min_el = Fraction(mat2[i_1][-1], mat2[i_1][raz_stol])
                raz_str = i_1

        # Выполняем процедуру однократного замещения.

        # ВЫПОЛНЯЕМ ИТЕРАЦИЮ
        # Воспользуемся методом Жордана-Гаусса относительно разрешающего элемента с координатами [raz_str, raz_stol].

        # Создадим пустую матрицу.
        SimplexOgr = []
        for i_1 in range(len(mat2)):
            SimplexOgr.append([])

        # Начнём процедуру.
        for i_1 in range(len(mat2)):
            for j_1 in range(len(mat2[i_1])):
                if i_1 == raz_str:
                    if mat2[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('∞')
                    else:
                        SimplexOgr[i_1].append(Fraction(mat2[raz_str][j_1], mat2[raz_str][raz_stol]))
                else:
                    if mat2[raz_str][raz_stol] == 0:
                        SimplexOgr[i_1].append('-∞')
                    else:
                        SimplexOgr[i_1].append(mat2[i_1][j_1] - (
                                    Fraction(mat2[raz_str][j_1], mat2[raz_str][raz_stol]) * mat2[i_1][raz_stol]))

        # Выводим матрицу.
        OTVET += ('\nОпорное базисное решение. Итерация №' + str(num_iter) + '\n')
        for i_1 in range(len(SimplexOgr)):
            for j_1 in range(len(SimplexOgr[0])):
                OTVET += (str(SimplexOgr[i_1][j_1]) + ' ')
            OTVET += ('\n')

        # Заменяем значения матрицы "mat2" на значения матрицы "SimplexOgr".
        mat2 = copy.deepcopy(SimplexOgr)

        # ПРОВЕРЯЕМ НОВОЕ БАЗИСНОЕ РЕШЕНИЕ НА ОПОРНОСТЬ
        for i_1 in mat2:
            if i_1[-1] < 0:
                OTVET += ('\nНовое базисное решение - не опорное.\n')
                num_iter += 1
                break
        else:
            OTVET += ('\nНовое базисное решение - опорное.\n')
            yes_or_no = 1


    # НАХОДИМ ЗНАЧЕНИЕ КРИТЕРИАЛЬНОЙ ФУНКЦИИ

    W_zna = 0
    for i_1 in range(len(mat2)):
        W_zna += mat2[i_1][-1] * SimplexW[i_1]

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
    for i_1 in range(len(mat2)):
        Ci.append(SimplexW[i_1])
        OTVET += (str(SimplexW[i_1]) + ' ')
    OTVET += ('\n')

    sim_tab = copy.deepcopy(mat2)  # копия матрицы mat2


    # НАХОДИМ ОЦЕНКИ ПЕРЕМЕННЫХ ОТНОСИТЕЛЬНО ВЫБРАННОГО БАЗИСА

    sim_tab.append([])  # будем заполнять строку оценок
    for i_1 in range(len(mat2[0]) - 1):
        Zj = 0
        for j_1 in range(len(mat2)):
            Zj += mat2[j_1][i_1] * Ci[j_1]
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
        for i_1 in range(len(SimplexOgr)):
            if i_1 <= len(Q) - 1:
                OTVET += (str(Num_baz[i_1]) + ' ')
                for j_1 in range(len(SimplexOgr[0])):
                    OTVET += (str(SimplexOgr[i_1][j_1]) + ' ')
                OTVET += (str(Q[i_1]) + '\n')
            else:
                OTVET += (' ' + ' ' + ' ')
                for j_1 in range(len(SimplexOgr[0])):
                    OTVET += (str(SimplexOgr[i_1][j_1]) + ' ')
                OTVET += (' ' + '\n')

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