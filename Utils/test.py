__author__ = 'arko1k'


import sys
# sys.path.append("/var/www/html/diptarko/Dionysus/build/bindings/python")


from pymongo import MongoClient
import traceback
import oauth2 as oauth
import simplejson as json
import pprint
import math
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt


# CONSUMER_KEY = 'UKiDv2fic9nlG2v85PkluM5Qn'
# CONSUMER_SECRET = 'awLaSyqmQu7m5Rr2AjH1xjIkM5ZKCL6lVeI99Wn5CYccH79Neg'
# ACCESS_TOKEN = '3221653195-Z5O4IzqMV96sjrvftKgBT44GXZV862roOz3V8kp'
# ACCESS_TOKEN_SECRET = 'NbaQbFm2zn7aIbLB2FgjuULeaSuulIiLACwitDNbVmHB4'
#
#
# consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
# access_token = oauth.Token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
# client = oauth.Client(consumer, access_token)
# reverse_geo = "https://api.twitter.com/1/geo/id/df51dec6f4ee2b2c.json"
# response, data = client.request(reverse_geo)
# print(response)
# pprint.pprint(json.loads(data))

# data = [306170602,306170602,306170602,306170602,306171322,306171322,306171322,306170602,306170602,306170602,306170602,306170602,306170602,306169161,306170602,306175644,306175644,306175644,306171322,306171322,306170602,306170602,306170602,306170602,306170602,306170602,306175644,306175644,306175644,306175644,306175644,306170602,306170602,306170602,306170602,306170602,306170602,306172042,306172042,306176364,306175644,306175644,306177084,306177084,306177084,306174923,306174923,306170602,306170602,306170602,306172042,306172042,306176364,306175644,306174923,306177084,306177084,306177084,306176364,306176364,306170602,306170602,306170602,306172042,306172042,306177084,306175644,306174923,306177084,306177084,306177084,306176364,306176364,306170602,306170602,306170602,306172042,306172042,306177084,306169161,306174923,306174923,306176364,306176364,306176364,306176364,306170602,306176364,306176364,306176364,306172042,306177084,306169161,306169161,306171322,306171322,306176364,306176364,306176364,306170602,306176364,306176364,306176364,306174923,306172042,306169161,306169161,306171322,306171322,306171322,306171322,306170602,306170602,306176364,306176364,306176364,306174923,306172042,306172042,306172042,306172042,306172042,306172042,306172042,306172042,306177084,306177084,306177084,306177084,306177084]
# print(len(data))

# p = [[cos(2*pi*t/10), sin(2*pi*t/10)] for t in xrange(10)]
# points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
# tri = Delaunay(points)
# plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
# plt.plot(points[:,0], points[:,1], 'o')
# plt.show()


def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end"""

    x1, y1 = start[0], start[1]
    x2, y2 = end[0], end[1]
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = [y, x] if is_steep else [x, y]
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def complete_polygon(points):
    points_shifted = points[1:]
    points_shifted.append(points[0])
    complete_polygon = []
    for p1, p2 in zip(points, points_shifted):
        line = get_line(p1, p2)[:-1]
        for p in line:
            complete_polygon.append(p)
    return complete_polygon


def dist(x_arr, y_arr, ind_1, ind_2):
    return math.hypot(x_arr[ind_2] - x_arr[ind_1], y_arr[ind_2] - y_arr[ind_1])


def keep(x_arr, y_arr, simplex, k):
    ind_1 = simplex[0]
    ind_2 = simplex[1]
    ind_3 = simplex[2]
    if math.hypot(x_arr[ind_2] - x_arr[ind_1], y_arr[ind_2] - y_arr[ind_1]) > k:
        return False
    if math.hypot(x_arr[ind_3] - x_arr[ind_2], y_arr[ind_3] - y_arr[ind_2]) > k:
        return False
    if math.hypot(x_arr[ind_1] - x_arr[ind_3], y_arr[ind_1] - y_arr[ind_3]) > k:
        return False
    return True

def dist_points(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def shortestDistanceToSegment(p0, p1, p2):
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    return math.fabs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / math.hypot(x2 - x1, y2 - y1)

bends = []


with open("data_unordered.txt") as f:
    json_data = f.readline()
points = json.loads(json_data)
# polygon = complete_polygon(points)

with open("data.txt") as f:
    json_data = f.readline()
ordered_polygon = json.loads(json_data)

# tri = Delaunay(polygon)

x_arr = [p[0] for p in points]
y_arr = [-p[1] for p in points]

x_arr_ordered = [p[0] for p in ordered_polygon]
y_arr_ordered = [-p[1] for p in ordered_polygon]


def contains_bend(ind_1, ind_2):
    start = [x_arr[ind_1], y_arr[ind_1]]
    end = [x_arr[ind_2], y_arr[ind_2]]
    start_ordered_index, end_ordered_index = None, None
    for i in range(0, len(ordered_polygon)):
        p = ordered_polygon[i]
        if p[0] == start[0] and p[1] == start[1]:
            start_ordered_index = i
        if p[0] == end[0] and p[1] == end[1]:
            end_ordered_index = i

    if start_ordered_index and end_ordered_index:
        if start_ordered_index > end_ordered_index:
            temp = start_ordered_index
            start_ordered_index = end_ordered_index
            end_ordered_index = temp

        if end_ordered_index - start_ordered_index > 10:
            return False
        else:
            start_ordered = [x_arr_ordered[start_ordered_index], y_arr_ordered[start_ordered_index]]
            end_ordered = [x_arr_ordered[end_ordered_index], y_arr_ordered[end_ordered_index]]
            for i in range(start_ordered + 1, end_ordered):
                d = shortestDistanceToSegment([x_arr_ordered[i], x_arr_ordered[i]], start_ordered, end_ordered)
                if d > 2:
                    if i not in bends:
                        bends.append(i)
                    return True
            return False
    else:
        return False


def smoothen(jaggedPoly, k_normal, k_edge):
        size = len(jaggedPoly) - 1
        start = jaggedPoly[0]
        end = jaggedPoly[size]
        dmax = 0
        index = 0
        # dist = dist_points(start[0], start[1], end[0], end[1])
        for i in range(1, size):
            d = shortestDistanceToSegment(jaggedPoly[i], start, end)
            if (d > dmax):
                index = i
                dmax = d

        # if dmax > (epsilon * dist / dmax): # epsilon = 0.04;

        epsilon = k_normal
        if size <= 10 and dmax > 0.4:
            epsilon = k_edge
            bends.append(jaggedPoly[index])

        if (dmax > epsilon):
            recResults1 = smoothen(jaggedPoly[0:index + 1], k_normal, k_edge)
            recResults2 = smoothen(jaggedPoly[index:size + 1], k_normal, k_edge)
            return recResults1 + recResults2
        else:
            return [start, end]

# polygon = smoothen(points, 1, 0.01)


tri = Delaunay(points)

poly_len = len(points)

edge = [[[0, 0] for i in range(poly_len)] for j in range(poly_len)] # [count, dist]
for ind_1, ind_2, ind_3 in tri.simplices:
    if edge[ind_1][ind_2][0] == 0:
        edge[ind_1][ind_2][1] = dist(x_arr, y_arr, ind_1, ind_2)
    edge[ind_1][ind_2][0] += 1

    if edge[ind_2][ind_3][0] == 0:
        edge[ind_2][ind_3][1] = dist(x_arr, y_arr, ind_2, ind_3)
    edge[ind_2][ind_3][0] += 1

    if edge[ind_3][ind_1][0] == 0:
        edge[ind_3][ind_1][1] = dist(x_arr, y_arr, ind_3, ind_1)
    edge[ind_3][ind_1][0] += 1

# print(len(polygon))
# print(len(bends))
#
# x_arr = [p[0] for p in polygon]
# y_arr = [-p[1] for p in polygon]




alpha_edges = []
# def erode_edges(start, end, edges, x_arr, k_normal, k_edge):
#     if start >= end:
#         return
#
#     k = k_normal
#     if contains_bend(x_arr, y_arr, start, end):
#         k = k_edge
#
#     if edges[start][end][1] > 0 and edges[start][end][1] <= k:
#         alpha_edges.append([start, end])
#
#     erode_edges(start + 1, end, edges, x_arr, k_normal, k_edge)
#     erode_edges(start, end - 1, edges, x_arr, k_normal, k_edge)
#
#
k = 10
# erode_edges(0, len(x_arr) - 1, edge, x_arr, k, 2.2)
for i in range(poly_len):
    for j in range(poly_len):
        # if contains_bend(i, j):
        #     k = 0.9
        # else:
        #     k = 6
        if edge[i][j][1] > 0 and edge[i][j][1] <= k:
                alpha_edges.append([i, j])


# edge_count = len(alpha_edges)
# alpha_edges_boundary = []
# for i, j in alpha_edges:
#     if edge[i][j][0] < 2:
#         alpha_edges_boundary.append([i, j])

# for simplex in tri.simplices:
#     ind_1 = simplex[0]
#     ind_2 = simplex[1]
#     ind_3 = simplex[2]
#     if edge_count[ind_1][ind_2] > 1 or edge_count[ind_2][ind_1] > 1 or edge_count[ind_2][ind_3] > 1\
#             or edge_count[ind_3][ind_2] > 1 or edge_count[ind_3][ind_1] > 1 or edge_count[ind_1][ind_3] > 1:
#         alpha_simplices = np.delete(alpha_simplices, simplex, 0)

# k = 1000
# alpha_simplices = tri.simplices.copy()
# for simplex in alpha_simplices:
#     if not keep(x_arr, y_arr, simplex, k):
#         alpha_simplices = np.delete(alpha_simplices, simplex, 0)

# print(len(alpha_edges))
#
alpha_edges = np.array(alpha_edges)
# # alpha_edges_boundary_np = np.array(alpha_edges_boundary)
# bends_np = np.array(bends)
x_arr_np = np.array(x_arr)
y_arr_np = np.array(y_arr)

# x_arr_bend = [p[0] for p in bends]
# y_arr_bend = [-p[1] for p in bends]

# plt.triplot(x_arr, y_arr, alpha_simplices)
# plt.triplot(x_arr, y_arr, tri.simplices)
plt.plot(x_arr_np[alpha_edges.T], y_arr_np[alpha_edges.T], linestyle='-', color='g')
# plt.plot(x_arr_np[bends_np.T], y_arr_np[bends_np.T], 'o')
# plt.plot(x_arr, y_arr, 'o')
# plt.plot(x_arr_bend, y_arr_bend, 'o')
plt.show()





epsilon = 1



k = 5.2