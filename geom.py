import math


def adjust_angle(angle):
    if angle < 0:
        angle += 360
    return angle


def normalize_angle(angle):
    while 0 < angle:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle


def normalize_angles(angles):
    start_angle = normalize_angle(angles[0])
    end_angle = normalize_angle(angles[1])
    if start_angle > end_angle:
        end_angle += 360
    return (start_angle, end_angle)


# http://geom.web.fc2.com/geometry/circle-circle-intersection.html
def find_crossing_point_of_circle_and_arc(center, radius, arc):
    x1 = arc[1][0]
    y1 = arc[1][1]
    r1 = arc[2]
    x2 = center[0]
    y2 = center[1]
    r2 = radius

    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    a = math.atan2(y2 - y1, x2 - x1)
    theta = math.acos((d**2 + r1**2 - r2**2)/(2*d*r1))

    p1 = math.degrees(a + theta)
    p2 = math.degrees(a - theta)

    p1 = adjust_angle(p1)
    p2 = adjust_angle(p2)

    start_angle = arc[3][0]
    end_angle = arc[3][1]

    res = []
    if start_angle <= p1 and p1 <= end_angle:
        res.append(p1)
    if start_angle <= p2 and p2 <= end_angle:
        res.append(p2)

    return res


def generate_trajectory_arc(arc, start_point, feed):
    res = []
    while True:
        angles = find_crossing_point_of_circle_and_arc(start_point, feed, arc)
        if len(angles) == 0:
            break
        start_angle = angles[0]
        end_angle = arc[3][1]
        arc[3] = (start_angle, end_angle)
        arc[3] = normalize_angles(arc[3])

        r = arc[2]
        theta = math.radians(start_angle)
        center = arc[1]
        x = center[0] + r * math.cos(theta)
        y = center[1] + r * math.sin(theta)
        start_point = (x, y)
        res.append(start_point)
    return res


# http://shogo82148.github.io/homepage/memo/geometry/line-circle.html
def find_crossing_point_of_circle_and_line(center, radius, line):
    res = []

    p = line[1][0]
    q = line[1][1]
    uv = (q[0] - p[0], q[1] - p[1])
    a = uv[0] * (center[0] - p[0]) + uv[1] * (center[1] - p[1])
    b = uv[0] * (center[1] - p[1]) - uv[1] * (center[0] - p[0])

    c = uv[0]**2 + uv[1]**2
    if c == 0:
        return res

    t1 = a + math.sqrt(c * radius**2 - b)
    t2 = a - math.sqrt(c * radius**2 - b)
    t1 = t1 / c
    t2 = t2 / c

    res.append((p[0] + t1 * uv[0], p[1] + t1 * uv[1]))
    res.append((p[0] + t2 * uv[0], p[1] + t2 * uv[1]))

    return res


def generate_trajectory_line(line, start_point, feed):
    res = []
    while True:
        points = find_crossing_point_of_circle_and_line(start_point, feed, line)
        points = [p for p in points if is_point_on_line(p, line)]
        if len(points) == 0:
            break
        start_point = points[0]
        end_point = line[1][1]
        line[1] = (start_point, end_point)
        res.append(start_point)
    return res


def generate_trajectory(trajectory, start_point, feed):
    if trajectory[0] == "LINE":
        return generate_trajectory_line(
                trajectory,
                start_point,
                feed)
    elif trajectory[0] == "ARC":
        return generate_trajectory_arc(
                trajectory,
                start_point,
                feed)
    return []


def generate_trajectories(trajectory, start_point, feed):
    res = []
    for t in trajectory:
        res += generate_trajectory(t, start_point, feed)
        start_point = res[-1]
    return res


def get_unit_vector(line):
    p = line[1][0]
    q = line[1][1]
    uv = (q[0] - p[0], q[1] - p[1])
    c = math.sqrt(uv[0]**2 + uv[1]**2)
    return (uv[0]/c, uv[1]/c)


def get_normal_vector(line):
    uv = get_unit_vector(line)
    return (uv[1], -uv[0])


def offset_line(line, offset):
    nv = get_normal_vector(line)
    p = line[1][0]
    q = line[1][1]
    p = (p[0] + offset * nv[0], p[1] + offset * nv[1])
    q = (q[0] + offset * nv[0], q[1] + offset * nv[1])
    return ["LINE", (p, q)]


def offset_arc(arc, offset):
    start_angle = arc[3][0]
    end_angle = arc[3][1]
    radius = arc[2]
    center = arc[1]
    angles = (start_angle, end_angle)
    return ["ARC", center, radius + offset, normalize_angles(angles)]


def offset_trajectory(trajectory, offset):
    if trajectory[0] == "LINE":
        return offset_line(trajectory, offset)
    elif trajectory[0] == "ARC":
        return offset_arc(trajectory, offset)
    return []


def offset_trajectories(trajectories, offset):
    res = []
    for t in trajectories:
        res.append(offset_trajectory(t, offset))
    return res


def find_crossing_point_of_two_lines(line1, line2):
    pv = line1[1]
    qv = line2[1]
    s1 = ((qv[1][0] - qv[0][0]) * (pv[0][1] - qv[0][1]) - (qv[1][1] - qv[0][1]) * (pv[0][0] - qv[0][0])) / 2
    s2 = ((qv[1][0] - qv[0][0]) * (qv[0][1] - pv[1][1]) - (qv[1][1] - qv[0][1]) * (qv[0][0] - pv[1][0])) / 2
    x = pv[0][0] + (pv[1][0] - pv[0][0]) * s1 / (s1 + s2)
    y = pv[0][1] + (pv[1][1] - pv[0][1]) * s1 / (s1 + s2)
    return (x, y)


# http://marupeke296.com/COL_2D_No2_PointToLine.html
def is_point_on_line(point, line):
    x0, y0 = line[1][0]
    x1, y1 = line[1][1]
    x2, y2 = point
    v1 = (x1 - x0, y1 - y0)
    v2 = (x2 - x0, y2 - y0)
    L1 = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    L2 = math.sqrt((x2-x0)**2 + (y2-y0)**2)
    return round(inner_product(v1, v2), 5) == round(L1*L2, 5) and L1 >= L2


def is_crossing_lines(line1, line2):
    point = find_crossing_point_of_two_lines(line1, line2)
    return is_point_on_line(point, line1) and is_point_on_line(point, line2)


def inner_product(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]


def get_angle_from_x_axis(p, q):
    v = (q[0] - p[0], q[1] - p[1])
    c = math.sqrt(v[0]**2 + v[1]**2)
    v = (v[0]/c, v[1]/c)
    cos_theta = inner_product((1, 0), v)
    theta = math.acos(cos_theta)
    if v[1] < 0:
        theta += math.pi
    return math.degrees(theta)


def joint_line_line(line1, line2, offset):
    if is_crossing_lines(line1, line2):
        point = find_crossing_point_of_two_lines(line1, line2)
        clipped_line1 = ["LINE", [line1[1][0], point]]
        clipped_line2 = ["LINE", [point, line2[1][1]]]
        return [clipped_line1, clipped_line2]
    else:
        nv = get_normal_vector(line1)
        end_point = line1[1][1]
        center = (end_point[0] - offset*nv[0], end_point[1] - offset*nv[1])
        radius = offset
        start_angle = get_angle_from_x_axis(center, line1[1][1])
        end_angle = get_angle_from_x_axis(center, line2[1][0])
        angles = (start_angle, end_angle)
        angles = normalize_angles(angles)
        arc = ["ARC", center, radius, angles]
        return [line1, arc, line2]


def find_crossing_point_of_arc_and_line(arc, line):
    points = find_crossing_point_of_circle_and_line(arc[1], arc[2], line)
    res = []
    for p in points:
        angle = get_angle_from_x_axis(arc[1], p)
        if arc[3][0] <= angle and angle <= arc[3][1]:
            res.append(p)
    return res


def joint_line_arc(line, arc, offset):
    points = find_crossing_point_of_arc_and_line(arc, line)
    p = [p for p in points if is_point_on_line(p, line)]
    if len(p) > 0:
        clipped_line = ["LINE", [line[1][0], p[0]]]
        return [clipped_line, arc]
    else:
        end_point = line[1][1]
        start_angle = get_angle_from_x_axis(arc[1], end_point)
        angles = (start_angle, arc[3][1])
        angles = normalize_angles(angles)
        arc = ["ARC", arc[1], arc[2], angles]
        return [line, arc]


def joint_arc_line(arc, line, offset):
    points = find_crossing_point_of_arc_and_line(arc, line)
    p = [p for p in points if is_point_on_line(p, line)]
    if len(p) > 0:
        clipped_line = ["LINE", [p[0], line[1][1]]]
        return [arc, clipped_line]
    else:
        start_point = line[1][0]
        end_angle = get_angle_from_x_axis(arc[1], start_point)
        angles = (arc[3][0], end_angle)
        angles = normalize_angles(angles)
        arc = ["ARC", arc[1], arc[2], angles]
        return [arc, line]


def joint_trajectory(trajectory1, trajectory2, offset):
    res = []
    if trajectory1[0] == "LINE" and trajectory2[0] == "LINE":
        res = joint_line_line(trajectory1, trajectory2, offset)
    elif trajectory1[0] == "LINE" and trajectory2[0] == "ARC":
        res = joint_line_arc(trajectory1, trajectory2, offset)
    elif trajectory1[0] == "ARC" and trajectory2[0] == "LINE":
        res = joint_arc_line(trajectory1, trajectory2, offset)
    else:
        assert False
    return res


def joint_trajectories(trajectories, offset):
    for i in range(len(trajectories)-1):
        res = joint_trajectory(trajectories[i], trajectories[i+1], offset)
        trajectories[i] = res[0]
        trajectories[i+1] = res[1]


def generate_toolpath(trajectories, offset, feed):
    res = offset_trajectories(trajectories, offset)
    joint_trajectories(res, offset)
    assert res[0][0] == "LINE"
    start_point = res[0][1][0]
    return generate_trajectories(res, start_point, feed)


import matplotlib.pyplot as plt

def find_start_point(traj):
    if traj[0] == "LINE":
        return traj[1][0]
    elif traj[0] == "ARC":
        c = traj[1]
        r = traj[2]
        sa = traj[3][0]
        return (c[0] + r * math.cos(math.radians(sa)), c[1] + r * math.sin(math.radians(sa)))

def printr(res, style):
    x = [r[0] for r in res]
    y = [r[1] for r in res]
    plt.plot(x, y, style)
    plt.show()

def printj(p, traj, style):
    res = []
    for t in traj:
        sp = find_start_point(t)
        res += generate_trajectory(t, sp, 0.1)
    x = [r[0] for r in res]
    y = [r[1] for r in res]
    p.plot(x, y, style)
    return p

traj = [
        ["LINE", [(0, 0), (10, 0)]],
        ["ARC", (0, 0), 10, (0, 90)],
        ["LINE", [(0, 10), (0, 8)]],
        ["ARC", (0, 6), 2, (90, 270)],
        ["LINE", [(0, 4), (0, 0)]],
        ]

traj = offset_trajectories(traj, 1)
print traj
joint_trajectories(traj, 1)
print traj
# printj(plt, traj, ".")
printj(plt, traj, "r.")
plt.show()


#res = generate_toolpath(traj, 5, 1)
#print_res(res, "r.")

