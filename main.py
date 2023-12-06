import copy
import random
from random import randrange
import time
import tkinter as tk
from Cluster import Cluster


def random_start_points(amount):
    for x in range(amount):
        coor = (randrange(-5000, 5000), randrange(-5000, 5000))
        while coor in start_clusters:                                            # avoid duplicates
            coor = (randrange(-5000, 5000), randrange(-5000, 5000))

        cluster = Cluster([coor], coor)                                          # Cluster Object (points), center point

        start_clusters.append(cluster)                                                          # save starting points
        all_clusters.append(cluster)                                                            # add them to all points
        print(x + 1, start_clusters[x].center_point, start_clusters[x].coors)


def generate_all_points(amount):
    for i in range(amount):
        point = random.choice(all_clusters)                                       # choose random point to add offset to
        used_offset = offset

      #  if abs(point[0]) > 5000 - offset or abs(point[1]) > 5000 - offset:                 # lower offset when near edge
       #     used_offset = 50

        x_offset, y_offset = randrange(-used_offset, used_offset), randrange(-used_offset, used_offset)  # random offset
        new_coor = (point.center_point[0] + x_offset, point.center_point[1] + y_offset)                  # add offset
        new_cluster = Cluster([new_coor], new_coor)

        while new_cluster in all_clusters:                                                            # avoid duplicates
            x_offset, y_offset = randrange(-used_offset, used_offset), randrange(-used_offset, used_offset) # new offset
            new_coor = (point.center_point[0] + x_offset, point.center_point[1] + y_offset)                 # add offset
            new_cluster = Cluster([new_coor], new_coor)

        all_clusters.append(new_cluster)                                                  # append to all points

    for i in range(len(all_clusters)):                                                    # print
        print(f"{i+1} {all_clusters[i].center_point}")

    print("\nStarting points: ", len(start_clusters))
    print("All points: ", len(all_clusters))

def dis_between_clusters(A, B):
    center_of_A, center_of_B = A.center_point, B.center_point
    distance = euclidean_distance(center_of_A, center_of_B)
    return distance

def create_matrix(clusters):
    dis_matrix = []
    n  = len(clusters)

    for i in range(n):
        row = []
        for j in range(n):
            dis = dis_between_clusters(clusters[i], clusters[j])
            row.append(dis)
        dis_matrix.append(row)
    return dis_matrix

def clusters_to_merge(dis_matrix):      # gets closest clusters for merging
    n = len(dis_matrix)
    min1 = 0
    min2 = 0
    min_dis = float("inf")

    for i in range(n):
        row = dis_matrix[i]
        for j in range(len(row)):
            dis = row[j]
            if dis != 0 and dis < min_dis:
                min1 = i
                min2 = j
                min_dis = dis
    return [min1, min2]


def euclidean_distance(coor1, coor2):
    x1, y1 = coor1
    x2, y2 = coor2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

def find_centroid(cluster):         # centroid is not one of the points in the cluster but the center
    points = len(cluster)

    if points == 1:                 # if cluster has only 1 point return it as centroid
        return cluster[0]

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
        if total_dis < total_dis_min:               # Update medoid if the total distance is smaller
            medoid = point
            total_dis_min = total_dis
    return medoid


def average_dis_in_cluster(cluster):
    n = len(cluster.coors)
    total_dis = sum(euclidean_distance(cluster.center_point, coor) for coor in cluster.coors)
    average_dis = total_dis / n
    return average_dis

def still_OK_clusters(clusters):
    global all_clusters
    for i in clusters:
        if average_dis_in_cluster(i) > max_average_dis:
            print("Average distance of points from the center greater than 500!")
            # all_clusters = copy.deepcopy(backup_clusters)
            return False

    return True

def cluster_algo(dis_matrix, center):
    save = None
    saved_index = 0
    last_center_point = find_centroid if center == "centroid" else find_medoid
    # backup_clusters = copy.deepcopy(all_clusters)
    while still_OK_clusters(all_clusters):
        cluster_A_index, cluster_B_index = clusters_to_merge(dis_matrix)        # closest clusters

        if cluster_A_index < cluster_B_index:
            cluster_A_index, cluster_B_index = cluster_B_index, cluster_A_index

        A = all_clusters[cluster_A_index]           # first cluster
        B = all_clusters[cluster_B_index]           # second cluster

        save = B                                    # Save where to split cluster at the end
        saved_index = len(B.coors)

        B.coors = [*A.coors, *B.coors]                  # MERGE
        B.center_point = last_center_point(B.coors)     # recalculate center point
        all_clusters.pop(cluster_A_index)       # remove old cluster
        dis_matrix.pop(cluster_A_index)         # remove column
        # dis_matrix.pop(cluster_B_index)         # remove column

        # all_clusters.pop(cluster_B_index)       # remove old cluster

        # find center point for new coors
        # center_point = find_centroid(new_coors) if center == "centroid" else find_medoid(new_coors)

        # new_C = Cluster(new_coors, center_point)    # new merged cluster
        # all_clusters.append(new_C)                  # add new cluster
        # new_row = []

        for i in range(len(dis_matrix)):
            row = dis_matrix[i]

            if cluster_A_index < len(row):
                row.pop(cluster_A_index)
            # row.pop(cluster_B_index)

            row[cluster_B_index] = dis_between_clusters(all_clusters[i], B)
            # row.append(distance)
            # new_row.append(distance)

        # new_row.append(0)
        # dis_matrix.append(new_row)

        if len(all_clusters) % 25 == 0:
            print(f"clusters: {len(all_clusters)}")


    # LAST MERGE SPLIT to 2 clusters and find their center points
    new = save.coors[saved_index:]
    new_center = last_center_point(new)

    final_cluster = Cluster(new, new_center)        # create Cluster object
    all_clusters.append(final_cluster)              # add to all clusters

    save.coors = save.coors[:saved_index]
    save.center_point = last_center_point(save.coors)


# ########## VALUES ########## #
seed_value = 6969
random.seed(seed_value)

start_points = 20
start_clusters = []
all_clusters = []

offset = 100
max_average_dis = 500


# ########## GUI ########## #
def gui_for_clusters(root, clusters):
    canvas = tk.Canvas(root, width=600, height=600, background="white")
    cluster_colors = {idx: f'#{random.randint(0, 0xFFFFFF):06x}' for idx in range(len(clusters))}

    for idx, cluster in enumerate(clusters):
        color = cluster_colors[idx]

        for point in cluster.coors:
            # points in clusters
            x, y = point
            scaled_x = (x + 5000) / 20
            scaled_y = (y + 5000) / 20
            canvas.create_oval(scaled_x, scaled_y, scaled_x + 5, scaled_y + 5, fill=color, width=0)

        # center points of clusters
        x, y = cluster.center_point
        scaled_x = (x + 5000) / 20
        scaled_y = (y + 5000) / 20
        canvas.create_oval(scaled_x, scaled_y, scaled_x + 5, scaled_y + 5, fill="", width=1)

    canvas.pack()
    root.mainloop()


# ########## START ########## #
while True:
    choice = int(input("Choose center for clusters:\n ~ centroid 1\n ~ medoid 2\n ~~~ "))
    if choice == 1:
        all_points_for_centroid = int(input("\nInput num of points: "))

        start_gen = time.time()
        print("\nStarting points:")
        random_start_points(start_points)

        print("\nGenerated points:")
        generate_all_points(all_points_for_centroid)
        end_gen = time.time()

        print(f"\nGenerating time: {(end_gen - start_gen):.2f} s")
        print("-----------------------")

        distance_matrix = create_matrix(all_clusters)
        print("Distance Matrix calculated")

        print("\nClustering with centroid as middle:\n")
        start_algo = time.time()

        cluster_algo(distance_matrix, "centroid")

        print(f"Num of clusters: {len(all_clusters)}")
        end_algo = time.time()
        end_time = end_algo - start_algo
        print(f"\nClustering time for {all_points_for_centroid} points:\n"
              f"~ center is centroid:\n"
              f"~ {end_time:.2f} s\n"
              f"~ {(end_time/60):.2f} m\n"
              f"~ {((end_time/60)/60):.2f} h\n")

        # GUI
        root = tk.Tk()
        gui_for_clusters(root, all_clusters)
        break

    elif choice == 2:
        all_points_for_medoid = int(input("\nInput num of points: "))

        start_gen = time.time()
        print("\nStarting points:")
        random_start_points(start_points)

        print("\nGenerated points:")
        generate_all_points(all_points_for_medoid)
        end_gen = time.time()

        print(f"\nGenerating time: {(end_gen - start_gen):.2f} s")
        print("-----------------------")

        distance_matrix = create_matrix(all_clusters)
        print("Distance Matrix calculated")

        print("\nClustering with medoid as middle:\n")
        start_algo = time.time()

        cluster_algo(distance_matrix, "medoid")

        print(f"Num of clusters: {len(all_clusters)}")
        end_algo = time.time()
        end_time = end_algo - start_algo
        print(f"\nClustering time for {all_points_for_medoid} points:\n"
              f"~ center is medoid:\n"
              f"~ {end_time:.2f} s\n"
              f"~ {(end_time/60):.2f} m\n"
              f"~ {((end_time/60)/60):.2f} h\n")

        # GUI
        root = tk.Tk()
        gui_for_clusters(root, all_clusters)
        break

    else:
        print("Choose again!\n")
