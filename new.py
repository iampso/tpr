import numpy as np

# Данные задачи
C = np.array([[3, 1, 2, 3],  # Стоимости перевозки
              [5, 4, 1, 5],
              [2, 4, 3, 2]])

a = [60, 65, 70]  # Запасы
b = [40, 60, 70, 25]  # Потребности

# Метод северо-западного угла для начального базисного решения
def nwcorner_method(a, b, C):
    x = np.zeros((len(a), len(b)))  # Матрица перевозок

    for i in range(len(a)):  # кол-во производителей
        for j in range(len(b)):  # кол-во потребителей
            if a[i] > 0 and b[j] > 0:  # проверка на наличие запаса и потребности
                shipment = min(a[i], b[j])  # определяем сколько можем отправить
                x[i][j] = shipment  # заполняем количество отправляемого груза
                # уменьшаем запас и потребность на количество отправленного груза
                a[i] -= shipment
                b[j] -= shipment
    return x

# Начальное базисное решение
x_initial = nwcorner_method(a.copy(), b.copy(), C)
print("Начальная матрица перевозок (метод северо-западного угла):")
for row in x_initial:
    print(row)  # вывод начальной матрицы перевозок

# Оптимизация распределения с помощью метода потенциалов
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
                if transport[i][j] > 0:  # ячейка содержит положительное значение
                    if np.isnan(u[i]) and not np.isnan(v[j]):  # потенциал источника ещё не вычислен, но потенциал пункта уже вычислен
                        u[i] = cost[i][j] - v[j]  # вычисляем потенциал источника
                    elif np.isnan(v[j]) and not np.isnan(u[i]):
                        v[j] = cost[i][j] - u[i]

    # Проверка на оптимальность
    while True:
        optimal = True
        for i in range(num_sources):
            for j in range(num_destinations):
                if transport[i][j] == 0:  # Если не базисная ячейка
                    reduced_cost = cost[i][j] - (u[i] + v[j])  # вычисляем уменьшенную стоимость
                    # Если уменьшенная стоимость меньше нуля
                    if reduced_cost < 0:
                        optimal = False

                        # Добавляем груз в не базисную ячейку
                        shipment = min(supply_amount[i], demand_amount[j])  # определяем сколько можно добавить груза
                        transport[i][j] = shipment  # количество отправленного груза
                        supply_amount[i] -= shipment
                        demand_amount[j] -= shipment

        if optimal:
            break  # Выход из цикла, если распределение является оптимальным

    return transport

# Оптимизация начального распределения
optimal_transport = potential_method(C, x_initial, a.copy(), b.copy())

# Вывод оптимальной матрицы перевозок
print("\nОптимальная матрица перевозок:")
for row in optimal_transport:
    print(row)

# Вычисляем минимальные затраты
total_cost = np.sum(optimal_transport * C)  # вычисление общей стоимости
print("Минимальные затраты:", total_cost)
