
from geom import *
import matplotlib.pyplot as plt

def print_res(res, style):
    x = [r[0] for r in res]
    y = [r[1] for r in res]
    plt.plot(x, y, style)
    plt.show()


trajectories = [
        ["LINE", [(0, 0), (10, 0)]],
        ["ARC", (0, 0), 10, (0, 90)],
        ]

res = generate_toolpath(trajectories, 5, 1)
print_res(res, "r.")


