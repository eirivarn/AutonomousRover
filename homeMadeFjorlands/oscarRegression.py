import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.gca().invert_yaxis()
"""
points = [(1, 2), (1, 3), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (5, 4), (6, 4), (6, 5), (7, 5),
          (8, 5), (8, 6), (9, 6), (9, 7), (10, 7), (10, 8), (10, 9), (10, 10), (11, 9), (11, 10), (2, 10)]
"""
points = [(1, 8), (1, 9), (2, 8), (2, 9), (3, 8), (3, 9),
          (4, 8), (4, 9), (5, 9), (6, 9), (6, 10), (7, 10)]
x_vals = list(map(lambda x: x[0], points))
y_vals = list(map(lambda x: x[1], points))

# polynomial regression
poly_reg = np.poly1d(np.polyfit(x_vals, y_vals, 4))
poly_line = np.linspace(1, np.max(x_vals), np.max(y_vals))

# linear regression
slope, intercept, r, p, std_err = stats.linregress(x_vals, y_vals)


def make_new_y_values(x):
    return slope * x + intercept


linear_reg = list(map(make_new_y_values, x_vals))


plt.scatter(x_vals, y_vals)
plt.plot(poly_line, poly_reg(poly_line))   # plot polynomial regression
plt.plot(x_vals, linear_reg)                # plot linear regression
plt.show()


# 48x64 grid
# Simulates here on 10x15 grid
