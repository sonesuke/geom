from math import sqrt
from PIL import Image
from PIL import ImageDraw


def get_unit_vector(line):
    p = line[0]
    q = line[1]
    uv = (q[0] - p[0], q[1] - p[1])
    k = sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)
    uv = (uv[0]/k, uv[1]/k)
    return uv


def get_normal_vector(v):
    return (-v[1], v[0])


def offset_line(line, offset):
    uv = get_unit_vector(line)
    nv = get_normal_vector(uv)
    p = line[0]
    q = line[1]
    p = (p[0] + offset * nv[0], p[1] + offset * nv[1])
    q = (q[0] + offset * nv[0], q[1] + offset * nv[1])
    return (p, q)


def cross_lines(pv, qv):
    s1 = ((qv[1][0] - qv[0][0]) * (pv[0][1] - qv[0][1]) - (qv[1][1] - qv[0][1]) * (pv[0][0] - qv[0][0])) / 2
    s2 = ((qv[1][0] - qv[0][0]) * (qv[0][1] - pv[1][1]) - (qv[1][1] - qv[0][1]) * (qv[0][0] - pv[1][0])) / 2
    x = pv[0][0] + (pv[1][0] - pv[0][0]) * s1 / (s1 + s2)
    y = pv[0][1] + (pv[1][1] - pv[0][1]) * s1 / (s1 + s2)
    return (x, y)


def is_cross(pv, qv):
    tc = (pv[0][0] - pv[1][0]) * (qv[0][1] - pv[0][1]) + (pv[0][1] - pv[1][1]) * (pv[0][0] - qv[0][0])
    td = (pv[0][0] - pv[1][0]) * (qv[1][1] - pv[0][1]) + (pv[0][1] - pv[1][1]) * (pv[0][0] - qv[1][0])
    return tc * td < 0


def point_to_simple_offset_lines(points, offset):
    res = []
    for i in range(len(points)):
        if i == len(points) - 1:
            break
        p, q = offset_line((points[i], points[i+1]), offset)
        res.append(("line", [p, q]))
    return res


def joint_lines(lines):
    res = []
    for i in range(len(lines)):
        idx1 = i
        idx2 = i + 1
        if i == len(lines) - 1:
            idx2 = 0
        cross = cross_lines(lines[idx1][1], lines[idx2][1])
        res.append((lines[idx1][0], [lines[idx1][1][0], cross]))
        if idx2 != 0:
            lines[idx2][1][0] = cross
        else:
            res[idx2][1][0] = cross
    return res


def is_cross_line_circle(center, radius, line):
    return (center[0] - line[1][0])**2 + (center[1] - line[1][1])**2 >= radius**2


def get_cross_line_circle(center, radius, line):
    uv = get_unit_vector(line)
    a = uv[0] * (center[0] - line[0][0]) + uv[1] * (center[1] - line[0][1])
    b = uv[0] * (center[1] - line[0][1]) - uv[1] * (center[0] - line[0][0])
    t = a + sqrt(radius**2 - b)
    return (line[0][0] + t * uv[0], line[0][1] + t * uv[1])


def generate_cycle_points(path, feed):
    res = []
    start = path[0][1][0]
    end = path[0][1][1]
    center = start
    res.append(center)
    line = (start, end)
    for i in range(len(path)):
        while is_cross_line_circle(center, feed, line):
            p = get_cross_line_circle(center, feed, line)
            start = p
            center = start
            res.append(center)
            line = (start, end)
            continue
        else:
            for j in range(i+1, len(path)):
                if is_cross_line_circle(center, feed, path[j][1]):
                    i = j
                    start = path[j][1][0]
                    end = path[j][1][1]
                    line = (start, end)
                    break
    return res


def points_to_path(points, offset):
    print points
    lines = point_to_simple_offset_lines(points, offset)
    print lines
    a = joint_lines(lines)
    print a
    return a


ps = [
        (100, 100),
        (100, 400),
        (400, 400),
        (300, 200),
        (400, 100),
        (100, 100)
        ]

path = points_to_path(ps, 20)
controls = generate_cycle_points(path, 10)

img = Image.new("RGB", (500, 500), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

draw.line(ps, (0, 0, 0, 0), 1)

for l in path:
    draw.line(l[1], (128, 128, 128, 0), 1)

for p in controls:
    draw.rectangle([p, (p[0] + 1, p[1] + 1)], (255, 0, 0, 0))

img.save("out.png")
