import random
from random import randrange
import time
import tkinter as tk


def random_start_points(amount):
    for x in range(amount):
        coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        while coor in start_points_arr:  # avoid duplicates
            coor = [randrange(-5000, 5000), randrange(-5000, 5000)]
        start_points_arr.append(coor)
        all_points_arr.append(coor)
        print(x + 1, start_points_arr[x])


def generate_all_points(amount):
    for i in range(amount):
        point = random.choice(all_points_arr)                                   # choose random point to add offset to

        used_offset = offset
        if abs(point[0]) > 5000 - offset or abs(point[1]) > 5000 - offset:
            used_offset = 50                                                    # lower offset when near edge

        x_offset, y_offset = randrange(-used_offset, used_offset), randrange(-used_offset, used_offset)  # random offset
        new_point = [point[0] + x_offset, point[1] + y_offset]                              # add offset

        while new_point in all_points_arr:                                                  # avoid duplicates
            x_offset, y_offset = randrange(-used_offset, used_offset), randrange(-used_offset, used_offset) # new offset
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
    merged_cluster = cluster_1 + cluster_2                                        # merge them
    merged_centroid = ((centroid_1[0] + centroid_2[0]) / 2,                       # find new centroid X
                       (centroid_1[1] + centroid_2[1]) / 2)                       # find new centroid Y
    merged_cluster.append(merged_centroid)                                        # add as new point for representation
    return merged_cluster


def merging_for_medoid(cluster_1, cluster_2):
    merged_cluster = cluster_1 + cluster_2                                        # merge them
    merged_medoid = find_medoid(merged_cluster)                                   # find new medoid
    merged_cluster.append(merged_medoid)                                          # add as new point for representation
    return merged_cluster


# TODO distance matrix could improve speed so it calculates it only once
def clustering(clusters, center, max_average_dis):
    count = 1
    while len(clusters) > 1:
        min_dis = float("inf")                  # min distance -> infinity (to find a smaller later)
        merge_these_clusters = (0, 0)           # merge these clusters

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
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

        # MERGING
        if center == "centroid":
            print(count)
            print(f"Cluster 1: {clusters[merge_these_clusters[0]]}")
            print(f"Cluster 2: {clusters[merge_these_clusters[1]]}")

            merged_cluster = merging_for_centroid(clusters[merge_these_clusters[0]], clusters[merge_these_clusters[1]])
            clusters.pop(merge_these_clusters[1])
            clusters[merge_these_clusters[0]] = merged_cluster
            print(f"Merged Cluster: {merged_cluster}\n")

        elif center == "medoid":
            print(count)
            print(f"Cluster 1: {clusters[merge_these_clusters[0]]}")
            print(f"Cluster 2: {clusters[merge_these_clusters[1]]}")

            merged_cluster = merging_for_medoid(clusters[merge_these_clusters[0]], clusters[merge_these_clusters[1]])
            clusters.pop(merge_these_clusters[1])
            clusters[merge_these_clusters[0]] = merged_cluster
            print(f"Merged Cluster: {merged_cluster}\n")

        for cluster in clusters:
            total_dis = 0
            if center == "centroid":
                center_point = find_centroid(cluster)
                for point in cluster:
                    dis = euclidean_distance(point, center_point)
                    total_dis += dis

                average_distance = total_dis / len(cluster)
                if average_distance > max_average_dis:
                    print(f"\nAverage distance between clusters exceeded {max_average_dis}!")
                    return clusters

            elif center == "medoid":
                center_point = find_medoid(cluster)
                for point in cluster:
                    dis = euclidean_distance(point, center_point)
                    total_dis += dis

                average_distance = total_dis / len(cluster)
                if average_distance > max_average_dis:
                    print(f"\nAverage distance between clusters exceeded {max_average_dis}!")
                    return clusters

        # print(f"Num of clusters: {len(clusters)}")
        # print(f"Average Distance: {average_distance:.2f}\n")

        count += 1

    return clusters


# VALUES #
seed_value = 10
random.seed(seed_value)

start_points = 20
start_points_arr = []
all_points_for_centroid = 20_000        # 20 000
all_points_for_medoid = 5000            # 5000
all_points_arr = []

offset = 100
max_average_dis = 500


# GUI #
def gui_for_clusters(root, clusters):
    canvas = tk.Canvas(root, width=1000, height=1000, background="white")
    canvas.pack()
    cluster_colors = {idx: f'#{random.randint(0, 0xFFFFFF):06x}' for idx in range(len(clusters))}
    for idx, cluster in enumerate(clusters):
        color = cluster_colors[idx]
        for point in cluster:
            x, y = point
            scaled_x = (x + 5000) / 10
            scaled_y = (y + 5000) / 10
            if point == cluster[:-1]:
                canvas.create_oval(scaled_x, scaled_y, scaled_x + 5, scaled_y + 5, fill="black")
            canvas.create_oval(scaled_x, scaled_y, scaled_x + 5, scaled_y + 5, fill=color)

    root.mainloop()


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
        print(f"\nGenerating time: {(end_gen - start_gen):.2f} s")
        print("-----------------------")

        print("\nClustering with centroid as middle:\n")
        start_algo = time.time()
        algo = clustering(clusters_C, "centroid", max_average_dis)
        print(f"Final cluster (centroid): {algo}\nNum of clusters: {len(algo)}")
        end_algo = time.time()
        end_time = end_algo - start_algo
        print(f"\nClustering time for {all_points_for_centroid} points:\n"
              f"~ center is centroid:\n"
              f"~ {end_time:.2f} s\n"
              f"~ {(end_time/60):.2f} m\n"
              f"~ {((end_time/60)/60):.2f} h\n")

        for cluster in algo:                        # add centroid to color it differently in gui
            center_p = find_centroid(cluster)
            cluster.append(center_p)

        root = tk.Tk()
        gui_for_clusters(root, algo)
        break

    elif choice == 2:
        start_gen = time.time()
        random_start_points(start_points)
        print("\nGenerated points:")
        clusters_M = generate_all_points(all_points_for_medoid)
        end_gen = time.time()
        print(f"\nGenerating time: {(end_gen - start_gen):.2f} s")
        print("-----------------------")

        print("\nClustering with medoid as middle:\n")
        start_algo = time.time()
        algo_2 = clustering(clusters_M, "medoid", max_average_dis)
        print(f"Final cluster (medoid): {algo_2}\nNum of clusters: {len(algo_2)}")
        end_algo = time.time()
        end_time = end_algo - start_algo
        print(f"\nClustering time for {all_points_for_medoid} points:\n"
              f"~ center is medoid:\n"
              f"~ {end_time:.2f} s\n"
              f"~ {(end_time/60):.2f} m\n"
              f"~ {((end_time/60)/60):.2f} h\n")

        for cluster in algo_2:                              # add medoid to gui
            center_p = find_centroid(cluster)
            cluster.append(center_p)

        root = tk.Tk()
        gui_for_clusters(root, algo_2)
        break

    else:
        print("Choose again!\n")
