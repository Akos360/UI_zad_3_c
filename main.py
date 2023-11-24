import random
from random import randrange
import matplotlib.pyplot as plot


def random_start_points(amount):
    for x in range(amount):
        coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        while coor in start_points_arr:  # avoid duplicates
            coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        start_points_arr.append(coor)
        all_points_arr.append(coor)
        print(x + 1, start_points_arr[x])


def generate_all_points():
    for i in range(all_points):
        point = random.choice(all_points_arr)                                   # choose random point to add offset to
        x_offset, y_offset = randrange(-offset, offset), randrange(-offset, offset)         # random offset
        new_point = [point[0] + x_offset, point[1] + y_offset]                  # add offset

        while new_point in all_points_arr:                                      # avoid duplicates
            x_offset, y_offset = randrange(-offset, offset), randrange(-offset, offset)     # new random offset
            new_point = [point[0] + x_offset, point[1] + y_offset]              # add new random offset

        all_points_arr.append(new_point)                                        # append ato all points

    for i in range(len(all_points_arr)):                                        # print
        print(f"{i+1} {all_points_arr[i]}")

    print("\nAll points: ", len(all_points_arr), "\n", all_points_arr)
    print("\nStarting points: ", len(start_points_arr), "\n", start_points_arr)


def euclidean_distance(coor1, coor2):
    x1, y1 = coor1
    x2, y2 = coor2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


def find_centroid(cluster):
    points = len(cluster)
    centroid_x = sum(x for x, y in cluster) / points
    centroid_y = sum(y for x, y in cluster) / points
    return centroid_x, centroid_y


def total_distance(coor, cluster):   # Total distance between the point and all other points in the cluster
    return sum(euclidean_distance(coor, other_point) for other_point in cluster)


def find_medoid(cluster):   # minimizes the sum of the distances between itself and all other points in the cluster
    medoid = cluster[0]
    total_dis_min = total_distance(medoid, cluster)

    for point in cluster:
        total_dis = total_distance(point, cluster)
        if total_dis < total_dis_min:   # Update medoid if the total distance is smaller
            medoid = point
            total_dis_min = total_dis
    return medoid


def clustering_centroid():
    pass


def clustering_medoid():
    pass


# VALUES #
seed_value = 10
random.seed(seed_value)

start_points = 20
start_points_arr = []
all_points = 20_000
all_points_arr = []
offset = 100

max_dis_from_mid = 500
distance_matrix = {}


# START #
print("Start points:")
random_start_points(start_points)
print("\nGenerated points:")
generate_all_points()

example_cluster = [(0, 0), (2, 0), (1, 1)]
print("\nExample Centroid for cluster:\n[(0, 0), (2, 0), (1, 1)]\n", find_centroid(example_cluster))
print("\nExample Medoid for cluster:\n[(0, 0), (2, 0), (1, 1)]\n", find_medoid(example_cluster))


# VISUALIZATION #
plot.gca().invert_yaxis()                   # origin to [0,0]
start_x, start_y = [i[0] for i in start_points_arr], [i[1] for i in start_points_arr]
all_x, all_y = [i[0] for i in all_points_arr], [i[1] for i in all_points_arr]

plot.scatter(all_x, all_y, c="black")       # all
for i in range(start_points):               # starting
    diff_color = f"C{i}" if f"C{i}" != "gray" else f"C{(i+1) % start_points}"       # f'C{i}' for a unique color
    plot.scatter(start_x[i], start_y[i], facecolor="none", edgecolor=diff_color)

plot.show()
