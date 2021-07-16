
from fractions import Fraction

# После нажатия на кнопку "Решить", введённые данные будут обрабатываться
def SimplexData(kol_str, kol_stol, gridLayout):

    SimplexOgr = []
    SimplexW = []


    # Первый этап (сохраняем левые части ограничений и критериальной функции)
    for i in range(kol_str):
        SimplexOgr.append([])
        for j in range(kol_stol):
            if gridLayout.itemAtPosition(i, j).widget().text() == '':
                SimplexOgr[i].append(0)
            else:
                # Условие, когда в числе есть запятая (преобразователь для float)
                if ',' in gridLayout.itemAtPosition(i, j).widget().text():
                    SimplexOgr[i].append(float((gridLayout.itemAtPosition(i, j).widget().text()).replace(',', '.')))
                else:
                    SimplexOgr[i].append(float(gridLayout.itemAtPosition(i, j).widget().text()))

    for i in range(kol_stol):
        if (gridLayout.itemAtPosition(kol_str, i)).widget().text() == '':
            SimplexW.append(0)
        else:
            # Условие, когда в числе есть запятая (преобразователь для float)
            if ',' in gridLayout.itemAtPosition(kol_str, i).widget().text():
                SimplexW.append(float((gridLayout.itemAtPosition(kol_str, i).widget().text()).replace(',', '.')))
            else:
                SimplexW.append(float(gridLayout.itemAtPosition(kol_str, i).widget().text()))


    # Второй этап (приводим систему к каноническому виду)
    for i in range(kol_str):
        if gridLayout.itemAtPosition(i, kol_stol).widget().currentText() == '⩽':
            for j in range(kol_str):
                if j == i:
                    SimplexOgr[j].append(1)
                else:
                    SimplexOgr[j].append(0)

    for i in range(kol_str):
        if gridLayout.itemAtPosition(i, kol_stol).widget().currentText() == '⩾':
            for j in range(kol_str):
                if j == i:
                    SimplexOgr[j].append(-1)
                else:
                    SimplexOgr[j].append(0)

    len_W = int(len(SimplexW))

    for i in range(len(SimplexOgr[0]) - len_W):
        SimplexW.append(0)


    # Третий этап (добавляем правую часть ограничений)
    for i in range(kol_str):
        # Условие, когда в числе есть запятая (преобразователь для float)
        if ',' in gridLayout.itemAtPosition(i, kol_stol+1).widget().text():
            SimplexOgr[i].append(float((gridLayout.itemAtPosition(i, kol_stol + 1).widget().text()).replace(',', '.')))
        else:
            SimplexOgr[i].append(float(gridLayout.itemAtPosition(i, kol_stol+1).widget().text()))


    # Четвёртый этап (представляем все данные в виде дробей (Fraction))
    for i in range(len(SimplexOgr)):
        for j in range(len(SimplexOgr[0])):
            SimplexOgr[i][j] = Fraction(str(SimplexOgr[i][j]))
    for i in range(len(SimplexW)):
        SimplexW[i] = Fraction(str(SimplexW[i]))

    # Определяем и получаем значение MAX или MIN
    max_or_min = gridLayout.itemAtPosition(kol_str, kol_stol + 1).widget().currentText()

    """ Все данные для дальнийших математических преобразований готовы! """
    return SimplexOgr, SimplexW, max_or_min