import numpy as np

# Данные задачи
C = [[3, 1, 2, 3],  # Стоимости перевозки
     [5, 4, 1, 5],
     [2, 4, 3, 2]]

a = [60, 65, 70]  # Запасы
b = [40, 60, 70, 25]  # Потребности


# Метод северо-западного угла для начального базисного решения
def nwcorner_method(a, b, C):
    x = [[0] * len(b) for _ in range(len(a))]  # Матрица перевозок


    for i in range(len(a)):  # кол-во производителей
        for j in range(len(b)):  # кол-во потребителей
            if a[i] > 0 and b[j] > 0:  # проверка есть ли ещё запас и есть ли потребность
                shipment = min(a[i], b[j])  # определяем сколько можем отправить
                x[i][j] = shipment  # заполняем кол-во отправл груза
                # уменьшаем запас и потребность на кол-во отправленного груза
                a[i] -= shipment
                b[j] -= shipment
    return x

# Начальное базисное решение
x_initial = nwcorner_method(a.copy(), b.copy(), C)
print("Начальная матрица перевозок (метод северо-западного угла):")
for row in x_initial:
    print(row)  # хранение текущей строки матрицы в процессе итерации


def potential_method(cost, transport, supply_amount, demand_amount):
    num_sources = len(transport)  # Количество источников


    num_destinations = len(transport[0])  # Количество пунктов назначения

    u = np.zeros(num_sources)  # Потенциалы источников
    v = np.zeros(num_destinations)  # Потенциалы пунктов назначения

    # Устанавливаем начальное значение для первого источника
    u[0] = 0

    # Вычисляем потенциалы
    for _ in range(num_sources + num_destinations):  # для обновления всех потенциалов
        for i in range(num_sources):
            for j in range(num_destinations):
                if transport[i][j] > 0:  # ячейка содержит пол. значение
                    if np.isnan(u[i]) and not np.isnan(v[j]):  # пот источника ещё не вычисл, но пот пункта уже вычисл
                        u[i] = cost[i][j] - v[j]  # вычисляем потенциал
                elif np.isnan(v[j]) and not np.isnan(u[i]):
                    v[j] = cost[i][j] - u[i]

    # Проверка на оптимальность
    while True:
        optimal = True
        for i in range(num_sources):
            for j in range(num_destinations):
                if transport[i][j] == 0:  # Если не базисная ячейка
                    reduced_cost = cost[i][j] - (u[i] + v[j])  # вычисляем уменьшенную стоимость для не базисной ячейки Если уменьшенная стоимость меньше нуля (reduced_cost < 0), это означает, что добавление груза в эту ячейку приведет к снижению общих затрат, и распределение не является оптимальным.
                if reduced_cost < 0:  # Если не оптимально
                    optimal = False

        if optimal:  # означает, что распределение явл оптимальным
            break

# Добавляем груз в не базисную ячейку
    for i in range(num_sources):
        for j in range(num_destinations):
            if transport[i][j] == 0 and cost[i][j] - (u[i] + v[j]) < 0:
                shipment = min(supply_amount[i], demand_amount[j])  # определяем сколько можно добавить груза
    transport[i][j] = shipment  # кол-во отправленного груза
    supply_amount[i] -= shipment
    demand_amount[j] -= shipment

    return transport

    # Оптимизация распределения с помощью метода потенциалов
    optimal_transport = potential_method(cost, X_initial, supply_amount, demand_amount)

    # Вывод оптимальной матрицы перевозок
    print("\nОптимальная матрица перевозок:")
    for row in optimal_transport:
        print(row)

    # Вычисляем минимальные затраты
    total_cost = np.sum(optimal_transport * cost)  # вычисление общей стоимости
    print("Минимальные затраты:", total_cost)




