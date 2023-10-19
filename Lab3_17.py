import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import tabulate


data = pd.read_excel('lab17.xlsx', sheet_name = 'Lab17', usecols = [1])
data.head()

xgen = data['x'].tolist()
xgen = list(map(float, xgen))

print(xgen)

class Light_Velocity:

    def __init__(self, xgen, med):

        self.medium = med

        if (self.medium == 'air'):
            xbegin = 0
            xend = 10
            self.k = 1
            self.lm = 0
            self.x1 = 0

        elif (self.medium == 'water'):
            xbegin = 10
            xend = 20
            self.lm = 1
            self.k = 0
            self.x1 = xgen[31]/100

        elif (self.medium == 'resin'):
            xbegin = 20
            xend = 30
            self.lm = 0.285
            self.k = 0
            self.x1 = xgen[32]/100

        self.x = []

        for val in range(xbegin, xend):
            self.x.append(xgen[val]/100)


        print(self.x)

        self.frequency = 50.1e6

    def count_c(self, c_air = 0):
        self.c = []

        for val in self.x:
            self.c.append(self.lm * c_air/(2*(abs(val-self.x1)) + self.lm) + self.k*(val * self.frequency * 4))

        self.c_average = sum(self.c) / len(self.c)

        self.c_deflect = []

        for val in self.c:
            self.c_deflect.append(val - self.c_average)

        self.c_deflect_squared = np.square(self.c_deflect)

        self.t = 2.3

        self.delta_c = self.t * np.sqrt(sum(self.c_deflect_squared) / (len(self.c) * (len(self.c) - 1)))

        return self.c_average, self.delta_c


    def output(self, c_air = 0, delta_c_air = 0):

        print('Среда:', self.medium)

        for val in range(0,len(self.x)):
            self.x[val] -= self.x1

        table = pd.DataFrame({
            'Δx, m': self.x,
            'c, m/s': self.c,
            'c-<c>, m/s': self.c_deflect,
            '(c-<c>)², m²/s²': self.c_deflect_squared})

        print(table.to_markdown())

        print('Скорость света в', self.medium,'= (', "{:.2e}".format(self.c_average), '±', "{:.0e}".format(self.delta_c), ') m/s')

        if (self.medium != 'air'):
            self.n = c_air/self.c_average
            self.delta_n_otn = np.sqrt(np.square(self.delta_c/self.c_average) + np.square(delta_c_air/c_air))
            self.delta_n = self.n * self.delta_n_otn

            print('Показатель преломления в', self.medium, 'n =', "{:.3}".format(self.n), '±', "{:.2}".format(self.delta_n))

        print()




Air = Light_Velocity(xgen, 'air')
Water = Light_Velocity(xgen,'water')
Resin = Light_Velocity(xgen, 'resin')

c_air, delta_c_air = Air.count_c()
c_water = Water.count_c(c_air)
c_resin = Resin.count_c(c_air)

Air.output()
Water.output(c_air, delta_c_air)
Resin.output(c_air, delta_c_air)





