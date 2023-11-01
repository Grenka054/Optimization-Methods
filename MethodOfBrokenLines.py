# МЕТОД ЛОМАННЫХ
# Количество итераций зависит от точности (параметр sigma).
# Чтобы просмотреть все итерации, установите debug_mode=True

import numpy as np
import matplotlib.pyplot as plt

   
class BrokenLineMethod:
    """Метод ломаных, позволяющий найти минимум функции, удовлетворяющей условию Липшица
    """
    def __init__(self, func, x):
        self.f = func
        self.x = x
        self.y = f(x)
        self.local_min_points = None

    def find_min(self, sigma, L, debug_mode=False):
        # Границы рассматриваемого отрезка
        a = x[0]
        b = x[-1]
        
        # Крайние точки аппроксимирующей кривой
        self.local_min_points = [(a, self.f(a)), (b, self.f(b))]
        
        # Еще одна точка ломанной
        x_ = (f(a) - f(b) + L * (a + b)) * 0.5 / L
        p_ = (f(a) + f(b) + L * (a - b)) * 0.5
        self.local_min_points.append( (x_, p_) )
        
        counter = 0
        while True:
            counter += 1
            
            # Получить точку минимума ломанной
            x_, p_ = min(self.local_min_points, key=lambda point: point[1])
            
            # Отладочная информация
            if debug_mode:
                print(f'{counter}) {x_:.2f}, {f(x_):.2f}')
                self._plot(x_, f(x_))
            
            delta = (self.f(x_) - p_) * 0.5 / L
            
            # Условие остановки
            if 2 * L * delta <= sigma:
                if debug_mode:
                    plt.show()
                return x_, f(x_)
            
            # Поднимем точку минимума до графика
            self.local_min_points.remove((x_, p_))
            self.local_min_points.append((x_, self.f(x_)))
            
            # 2 новые точки ломанной
            x1 = x_ - delta
            x2 = x_ + delta
            p_ = (self.f(x_) + p_) * 0.5
            
            self.local_min_points.append((x1, p_))
            self.local_min_points.append((x2, p_))
            

    def plot(self, x, y):
        self.local_min_points = sorted(self.local_min_points, key=lambda point: point[0])
        plt.figure(figsize=(15, 4))
        plt.plot(self.x,self.y)
        px, py = zip(*self.local_min_points)
        plt.plot(px,py)
        plt.plot(x,y,'ro')
    

def f(x):
    return 0.1 * (x**3 - x) + 1

def plot_min(x, y, xmin, ymin):
    plt.figure(figsize=(15, 4))
    plt.plot(x,y)
    plt.plot(xmin,ymin,'ro')
    plt.show()
        
num = 1000
a = -1
b = 1
x = np.linspace(a, b, num)

blm = BrokenLineMethod(f, x)
xmin, ymin = blm.find_min(sigma=0.015, L=0.2, debug_mode=False)
blm.plot(xmin, ymin)
plt.show()
# plot_min(x, f(x), xmin, ymin)
print(f'Точка минимума: ({xmin:.2f}, {ymin:.2f})')
