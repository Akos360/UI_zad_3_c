import random
from random import randrange
import matplotlib.pyplot as plot
import time


def random_start_points(amount):
    for x in range(amount):
        coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        while coor in start_points_arr:  # avoid duplicates
            coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        start_points_arr.append(coor)
        all_points_arr.append(coor)
        print(x + 1, start_points_arr[x])


# TODO lower offset if near edge
def generate_all_points(amount):
    for i in range(amount):
        point = random.choice(all_points_arr)                                   # choose random point to add offset to

        x_offset, y_offset = randrange(-offset, offset), randrange(-offset, offset)         # random offset
        new_point = [point[0] + x_offset, point[1] + y_offset]                              # add offset

        while new_point in all_points_arr:                                                  # avoid duplicates
            x_offset, y_offset = randrange(-offset, offset), randrange(-offset, offset)     # new random offset
            new_point = [point[0] + x_offset, point[1] + y_offset]                          # add new random offset

        all_points_arr.append(new_point)                                                  # append to all points

    for i in range(len(all_points_arr)):                                                    # print
        print(f"{i+1} {all_points_arr[i]}")

    all_tuple_list = [[tuple(point)] for point in all_points_arr]      # needed the tuples in separate lists (clusters)
    start_tuple_list = [[tuple(point)] for point in start_points_arr]

    print("\nAll points: ", len(all_points_arr), "\n", all_tuple_list)
    print("\nStarting points: ", len(start_points_arr), "\n", start_tuple_list)

    return all_tuple_list


def euclidean_distance(coor1, coor2):
    x1, y1 = coor1
    x2, y2 = coor2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


def find_centroid(cluster):
    points = len(cluster)

    # if points == 1:
    #    return cluster[0]

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


def merging_for_centroid(cluster_1, cluster_2):
    centroid_1, centroid_2 = find_centroid(cluster_1), find_centroid(cluster_2)   # find the centroid of 2 clusters
    print("\ncluster 1: ", cluster_1, "\ncluster 2: ", cluster_2)
    merged_cluster = cluster_1 + cluster_2                                        # merge them
    print("merged cluster 1 + 2: ", merged_cluster, "\n")
    merged_centroid = ((centroid_1[0] + centroid_2[0]) / 2,                       # find new centroid X
                       (centroid_1[1] + centroid_2[1]) / 2)                       # find new centroid Y
    merged_cluster.append(merged_centroid)                                        # add as new point for representation
    return merged_cluster


def merging_for_medoid(cluster_1, cluster_2):
    print("\ncluster 1: ", cluster_1, "\ncluster 2: ", cluster_2)
    merged_cluster = cluster_1 + cluster_2                                        # merge them
    print("merged cluster 1 + 2: ", merged_cluster, "\n")
    merged_medoid = find_medoid(merged_cluster)                                   # find new medoid
    merged_cluster.append(merged_medoid)                                          # add as new point for representation
    return merged_cluster


# TODO add limit for Average distance between clusters is more than 500 (that is the amount of clusters at that point)
def clustering(clusters, center):
    count = 1
    while len(clusters) > 1:
        min_dis = float("inf")                  # min distance -> infinity (to find a smaller later)
        merge_these_clusters = (0, 0)           # merge these clusters

        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                if center == "centroid":
                    distance = euclidean_distance(find_centroid(clusters[i]), find_centroid(clusters[j]))
                    if distance < min_dis:
                        min_dis = distance
                        merge_these_clusters = (i, j)

                elif center == "medoid":
                    distance = euclidean_distance(find_medoid(clusters[i]), find_medoid(clusters[j]))
                    if distance < min_dis:
                        min_dis = distance
                        merge_these_clusters = (i, j)

        if center == "centroid":
            print(count)
            merged_cluster = merging_for_centroid(clusters[merge_these_clusters[0]], clusters[merge_these_clusters[1]])
            clusters.pop(merge_these_clusters[1])
            clusters[merge_these_clusters[0]] = merged_cluster
        elif center == "medoid":
            merged_cluster = merging_for_medoid(clusters[merge_these_clusters[0]], clusters[merge_these_clusters[1]])
            clusters.pop(merge_these_clusters[1])
            clusters[merge_these_clusters[0]] = merged_cluster
        count += 1
    return clusters[0]


# VALUES #
seed_value = 10
random.seed(seed_value)

start_points = 20
start_points_arr = []
all_points_for_centroid = 20_000
all_points_for_medoid = 2000
all_points_arr = []
offset = 100

max_average_dis = 500

# TODO use PYPY in Pycharm
# START #
while 1:
    choice = int(input("Choose center for clusters:\n ~ centroid 1\n ~ medoid 2\n ~~~ "))
    if choice == 1:
        start_gen = time.time()
        print("\nStarting points:")
        random_start_points(start_points)
        print("\nGenerated points:")
        clusters_C = generate_all_points(all_points_for_centroid)
        end_gen = time.time()
        print(f"Generating time: {end_gen - start_gen} s")

        print("\nClustering with centroid as middle:")
        start_algo = time.time()
        algo = clustering(clusters_C, "centroid")
        print("centroid ", algo)
        end_algo = time.time()
        print(f"Clustering time for centroid: {end_algo - start_algo} s")
        break
    elif choice == 2:
        start_gen = time.time()
        random_start_points(start_points)
        print("\nGenerated points:")
        clusters_M = generate_all_points(all_points_for_medoid)
        end_gen = time.time()
        print(f"Generating time: {end_gen - start_gen} s")

        print("\nClustering with medoid as middle:")
        start_algo = time.time()
        algo_2 = clustering(clusters_M, "medoid")
        print("medoid ", algo_2)
        end_algo = time.time()
        print(f"Clustering time for medoid: {end_algo - start_algo} s")
        break
    else:
        print("Choose again!\n")

# example_cluster = [(0, 0), (2, 0), (1, 1)]
# print("\nExample Centroid for cluster:\n[(0, 0), (2, 0), (1, 1)]\n", find_centroid(example_cluster))
# print("\nExample Medoid for cluster:\n[(0, 0), (2, 0), (1, 1)]\n", find_medoid(example_cluster))

# TODO visualization maybe in tkinter maybe not
# TODO color them as clusters not middle points somehow brev
# VISUALIZATION #
plot.gca().invert_yaxis()                   # origin to [0,0]

start_x, start_y = [i[0] for i in start_points_arr], [i[1] for i in start_points_arr]
all_x, all_y = [i[0] for i in all_points_arr], [i[1] for i in all_points_arr]

plot.scatter(all_x, all_y, c="black")       # all
for i in range(start_points):               # starting
    diff_color = f"C{i}" if f"C{i}" != "gray" else f"C{(i+1) % start_points}"       # f'C{i}' for a unique color
    plot.scatter(start_x[i], start_y[i], facecolor="none", edgecolor=diff_color)

plot.show()
