import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, ion, show
import random
import configurator

def visualization(input_mass):
    result_mass = []
    number_of_criteria = len(input_mass[0])
    for i in range(number_of_criteria):
        result_mass.append([])
    for obj in input_mass:
        for i in range(number_of_criteria):
            result_mass[i].append(obj[i])
    names = configurator.get_setting('settings.ini', "core", "names")
    names_of_section = names.split(",")
    for i in range(len(result_mass)):
        title=configurator.get_setting('settings.ini', names_of_section[i+1], 'name')
        graphics(result_mass[i], title)

def graphics(ymass, title):
    length = len(ymass)

    # Желтый цвет
    yellow_max = np.linspace(95, 95, 95)
    yellow_min = np.linspace(60, 60, 60)

    #  Создаем "Figure" и "Axes":
    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(640 / dpi, 400/ dpi))
    fig.canvas.set_window_title('Результаты анализа')
    plt.subplots_adjust(hspace=0.40)
    plt.yticks(np.arange(0, 100, 5))
    plt.xticks(np.arange(1, length+1))

    # Желтый цвет
    plt.grid()
    plt.axis()
    plt.xlabel('Номер об\'єкту, №')
    plt.ylabel('Доля ознаки, %')
    plt.title(title)
    plt.scatter(np.arange(1, len(ymass)+1, 1), ymass, color='blue')
    #  Добавление заголовков:
    plt.savefig('graphics\\'+str(round(random.random(), 3))+'.jpg')

if __name__ == "__main__":
    visualization([[95.41, 4.34, 0.24], [60, 30, 10],
              [15, 60, 25], [50, 25, 25],[95.41, 4.34, 0.24], [60, 30, 10],
              [65, 15, 20], [50, 25, 25],[95.41, 4.34, 0.24], [60, 30, 10],
              [89, 10, 1], [50, 25, 25],[95.41, 4.34, 0.24], [60, 30, 10],
              [45, 30, 25], [50, 25, 25]])
