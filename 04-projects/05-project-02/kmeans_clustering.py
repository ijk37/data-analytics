"""
Project 02: K-Means Clustering
Chapter 5 - Clustering
Data Analytics Course

Implements K-means clustering from scratch:
  - Euclidean distance
  - Assignment and update steps
  - SSE computation
  - K-means++ initialization
  - Elbow method for choosing K
  - Exercise Q1 step-by-step verification
  - Full Friends dataset with K=4
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================

import math
import random
import csv
import os


# =============================================================================
# SECTION 2: DATA LOADING
# =============================================================================

def load_csv(filepath):
    """
    Load a CSV file and return columns as a dictionary of lists.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    tuple : (columns, n_rows)
        columns : dict
            Keys are column headers, values are lists of values.
            Numeric columns are stored as floats; others as strings.
        n_rows : int
            Number of data rows (excluding header).

    # PIVOT: Change encoding="utf-8" to encoding="latin-1" for special characters.
    # PIVOT: Change delimiter="," to delimiter=";" for semicolon-separated files.
    """
    columns = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for header in reader.fieldnames:
            columns[header] = []
        for row in reader:
            for header in reader.fieldnames:
                value = row[header].strip()
                try:
                    columns[header].append(float(value))
                except ValueError:
                    columns[header].append(value)
    n_rows = len(columns[list(columns.keys())[0]])
    return columns, n_rows


# =============================================================================
# SECTION 3: UTILITY FUNCTIONS
# =============================================================================

def normalize_columns(columns):
    """
    Z-score normalize all numeric columns in a column dictionary.

    For each numeric column:
        z = (x - mean) / std_dev

    Parameters
    ----------
    columns : dict
        Column dictionary where values are lists.

    Returns
    -------
    dict
        New column dictionary with normalized numeric columns.
        Non-numeric columns are passed through unchanged.
    """
    normalized = {}
    for col_name in columns:
        values = columns[col_name]

        # Check if the column is numeric
        is_numeric = True
        for v in values:
            if not isinstance(v, float) and not isinstance(v, int):
                is_numeric = False
                break

        if not is_numeric:
            normalized[col_name] = values[:]
            continue

        # Compute mean
        total = 0.0
        for v in values:
            total = total + v
        mean = total / len(values)

        # Compute standard deviation
        sq_diff_sum = 0.0
        for v in values:
            sq_diff_sum = sq_diff_sum + (v - mean) ** 2
        std = math.sqrt(sq_diff_sum / len(values))

        if std == 0.0:
            # All values are the same: normalized to 0
            normalized[col_name] = [0.0] * len(values)
        else:
            norm_values = []
            for v in values:
                norm_values.append((v - mean) / std)
            normalized[col_name] = norm_values

    return normalized


def euclidean_distance_2d(p1, p2):
    """
    Compute Euclidean distance between two 2D points.

    Formula: sqrt((x1-x2)^2 + (y1-y2)^2)

    Parameters
    ----------
    p1 : list or tuple of two floats
        First point [x, y].
    p2 : list or tuple of two floats
        Second point [x, y].

    Returns
    -------
    float
        Euclidean distance.
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def euclidean_distance_nd(p1, p2):
    """
    Compute Euclidean distance between two n-dimensional points.

    Parameters
    ----------
    p1 : list of float
    p2 : list of float

    Returns
    -------
    float
    """
    total = 0.0
    for i in range(len(p1)):
        diff = p1[i] - p2[i]
        total = total + diff * diff
    return math.sqrt(total)


# =============================================================================
# SECTION 4: K-MEANS CORE FUNCTIONS
# =============================================================================

def assign_to_nearest_centroid(points, centroids):
    """
    Assign each point to the nearest centroid.

    For each point, compute the distance to each centroid and assign
    the point to the cluster with the smallest distance.

    Parameters
    ----------
    points : list of list of float
        Data points.
    centroids : list of list of float
        Current centroid positions.

    Returns
    -------
    list of int
        assignments[i] = index of the centroid closest to points[i].
    """
    assignments = []
    for point in points:
        best_cluster = 0
        best_dist = euclidean_distance_nd(point, centroids[0])
        for k in range(1, len(centroids)):
            d = euclidean_distance_nd(point, centroids[k])
            if d < best_dist:
                best_dist = d
                best_cluster = k
        assignments.append(best_cluster)
    return assignments


def compute_centroids(points, assignments, k):
    """
    Compute new centroids as the mean of all points in each cluster.

    Parameters
    ----------
    points : list of list of float
        Data points.
    assignments : list of int
        Cluster assignment for each point.
    k : int
        Number of clusters.

    Returns
    -------
    list of list of float
        New centroid positions. If a cluster has no points, its centroid
        is kept at [0, 0, ...] (degenerate case).
    """
    n_dims = len(points[0])
    new_centroids = []

    for cluster_id in range(k):
        # Collect all points in this cluster
        cluster_points = []
        for i in range(len(points)):
            if assignments[i] == cluster_id:
                cluster_points.append(points[i])

        if len(cluster_points) == 0:
            # Degenerate: no points assigned to this cluster
            new_centroids.append([0.0] * n_dims)
            continue

        # Compute mean for each dimension
        centroid = []
        for d in range(n_dims):
            dim_total = 0.0
            for pt in cluster_points:
                dim_total = dim_total + pt[d]
            centroid.append(dim_total / len(cluster_points))
        new_centroids.append(centroid)

    return new_centroids


def compute_sse(points, assignments, centroids):
    """
    Compute the Sum of Squared Errors (SSE) for a clustering.

    SSE = sum over all clusters C_i:
              sum over all points x in C_i:
                  dist(centroid_i, x)^2

    Parameters
    ----------
    points : list of list of float
    assignments : list of int
    centroids : list of list of float

    Returns
    -------
    float
        Total SSE.
    """
    sse = 0.0
    for i in range(len(points)):
        cluster_id = assignments[i]
        centroid = centroids[cluster_id]
        dist = euclidean_distance_nd(points[i], centroid)
        sse = sse + dist * dist
    return sse


def kmeans(points, k, max_iter=100, seed=42, initial_centroids=None):
    """
    Run K-means clustering.

    Parameters
    ----------
    points : list of list of float
        Data points.
    k : int
        Number of clusters.
    max_iter : int
        Maximum number of iterations. Default 100.
    seed : int
        Random seed for reproducibility. Default 42.
    initial_centroids : list of list of float or None
        If provided, use these as the starting centroids.
        If None, select k random points from the dataset.

    Returns
    -------
    tuple : (assignments, centroids, sse_history)
        assignments : list of int
            Final cluster assignment for each point.
        centroids : list of list of float
            Final centroid positions.
        sse_history : list of float
            SSE value after each iteration.
    """
    random.seed(seed)

    # Choose initial centroids
    if initial_centroids is not None:
        centroids = [c[:] for c in initial_centroids]
    else:
        # Randomly pick k distinct points as initial centroids
        indices = list(range(len(points)))
        random.shuffle(indices)
        centroids = [points[i][:] for i in indices[:k]]

    sse_history = []
    assignments = [0] * len(points)

    for iteration in range(max_iter):
        # Assignment step
        new_assignments = assign_to_nearest_centroid(points, centroids)

        # Compute SSE for this assignment
        sse = compute_sse(points, new_assignments, centroids)
        sse_history.append(sse)

        # Update step
        new_centroids = compute_centroids(points, new_assignments, k)

        # Check convergence: did assignments change?
        changed = False
        for i in range(len(assignments)):
            if assignments[i] != new_assignments[i]:
                changed = True
                break

        assignments = new_assignments
        centroids = new_centroids

        if not changed:
            break

    return assignments, centroids, sse_history


# =============================================================================
# SECTION 5: K-MEANS++ INITIALIZATION
# =============================================================================

def kmeans_plus_plus_init(points, k, seed=42):
    """
    K-means++ initialization: choose initial centroids with smart seeding.

    Algorithm:
      1. Choose first centroid uniformly at random from points.
      2. For each subsequent centroid:
         a. Compute D(x) = min distance^2 from x to any already-chosen centroid.
         b. Choose next centroid with probability proportional to D(x).
      3. Return k centroids.

    Parameters
    ----------
    points : list of list of float
    k : int
    seed : int

    Returns
    -------
    list of list of float
        K initial centroid positions.
    """
    random.seed(seed)
    chosen = []

    # Step 1: choose first centroid uniformly at random
    first_idx = random.randint(0, len(points) - 1)
    chosen.append(points[first_idx][:])

    # Step 2: choose remaining centroids
    for _ in range(k - 1):
        # Compute D(x)^2 for each point: min squared dist to closest chosen centroid
        distances_sq = []
        for point in points:
            min_dist_sq = None
            for centroid in chosen:
                d = euclidean_distance_nd(point, centroid)
                d_sq = d * d
                if min_dist_sq is None or d_sq < min_dist_sq:
                    min_dist_sq = d_sq
            distances_sq.append(min_dist_sq)

        # Choose next centroid with probability proportional to D(x)^2
        total_dist_sq = 0.0
        for d in distances_sq:
            total_dist_sq = total_dist_sq + d

        # Sample a random threshold
        threshold = random.uniform(0, total_dist_sq)
        cumulative = 0.0
        chosen_idx = len(points) - 1
        for i in range(len(points)):
            cumulative = cumulative + distances_sq[i]
            if cumulative >= threshold:
                chosen_idx = i
                break
        chosen.append(points[chosen_idx][:])

    return chosen


# =============================================================================
# SECTION 6: ELBOW METHOD
# =============================================================================

def find_elbow(points, max_k=8, seed=42):
    """
    Run K-means for K = 1 to max_K and record SSE.

    Use the resulting SSE values to identify the elbow point —
    the K where the SSE reduction per additional cluster starts to diminish.

    Parameters
    ----------
    points : list of list of float
    max_k : int
        Maximum K to try. Default 8.
    seed : int

    Returns
    -------
    list of float
        sse_values[i] = SSE for K = i+1 (0-indexed).
    """
    sse_values = []
    for k in range(1, max_k + 1):
        _, _, sse_history = kmeans(points, k, seed=seed)
        sse_values.append(sse_history[-1])
    return sse_values


def print_elbow_chart(sse_values):
    """
    Print an ASCII bar chart of SSE vs K (elbow curve).

    Parameters
    ----------
    sse_values : list of float
        SSE for each K value (index 0 = K=1).
    """
    if len(sse_values) == 0:
        return

    max_sse = max(sse_values)
    bar_width = 40

    print("  K  | SSE       | Chart")
    print("  ---+-----------+" + "-" * bar_width)
    for i in range(len(sse_values)):
        k = i + 1
        sse = sse_values[i]
        if max_sse > 0:
            bar_len = int(bar_width * sse / max_sse)
        else:
            bar_len = 0
        bar = "#" * bar_len
        print("  {:2d} | {:9.1f} | {}".format(k, sse, bar))


# =============================================================================
# SECTION 7: DISPLAY HELPERS
# =============================================================================

def print_section(title):
    """Print a formatted section header."""
    print()
    print("=" * 65)
    print("  " + title)
    print("=" * 65)


def print_clusters(assignments, names, k):
    """
    Print cluster membership for each cluster.

    Parameters
    ----------
    assignments : list of int
    names : list of str
    k : int
    """
    for cluster_id in range(k):
        members = []
        for i in range(len(assignments)):
            if assignments[i] == cluster_id:
                members.append(names[i])
        print("  Cluster {}: {}".format(cluster_id + 1, members))


# =============================================================================
# SECTION 8: MAIN DEMONSTRATION
# =============================================================================

def main():
    """
    Demonstrates K-means clustering with the Friends dataset.

    1. Exercise Q1: 6-person dataset, K=2, manual centroids, step-by-step
    2. Full 10-person dataset, K=4 using K-means
    3. Elbow curve to suggest optimal K
    4. K-means++ initialization example
    """

    # ------------------------------------------------------------------
    # DEMO 1: Exercise Q1 — Step-by-step K=2 on 6-person dataset
    # ------------------------------------------------------------------
    print_section("DEMO 1: Exercise Q1 — K-Means, K=2, 6-Person Dataset")
    print()
    print("  Dataset: Andrew(55,1), Bernhard(43,2), Carolina(37,5),")
    print("           Dennis(82,3), Eve(23,3.2), Fred(46,5)")
    print()
    print("  Initial centroids: Andrew(55,1) and Carolina(37,5)")
    print()

    names_6 = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve", "Fred"]
    points_6 = [
        [55, 1.0],
        [43, 2.0],
        [37, 5.0],
        [82, 3.0],
        [23, 3.2],
        [46, 5.0],
    ]
    initial_c = [[55, 1.0], [37, 5.0]]

    # Show distances to each centroid in iteration 1
    print("  --- Iteration 1: Distances ---")
    print()
    print("  {:10s}  {:>15s}  {:>15s}  {:>12s}".format(
        "Person", "Dist to Andrew", "Dist to Carolina", "Assigned to"))
    print("  " + "-" * 58)
    for i in range(len(points_6)):
        d_andrew = euclidean_distance_2d(points_6[i], initial_c[0])
        d_carolina = euclidean_distance_2d(points_6[i], initial_c[1])
        if d_andrew <= d_carolina:
            assignment = "Cluster 1 (Andrew)"
        else:
            assignment = "Cluster 2 (Carolina)"
        print("  {:10s}  {:>15.4f}  {:>15.4f}  {:>20s}".format(
            names_6[i], d_andrew, d_carolina, assignment))

    # Run K-means with fixed initial centroids
    assignments_6, centroids_6, sse_6 = kmeans(
        points_6, k=2, initial_centroids=initial_c
    )

    print()
    print("  --- After Iteration 1: New Centroids ---")
    # Manually compute iteration 1 centroids for display
    init_assignments = assign_to_nearest_centroid(points_6, initial_c)
    iter1_centroids = compute_centroids(points_6, init_assignments, 2)

    for cluster_id in range(2):
        members = []
        for i in range(len(init_assignments)):
            if init_assignments[i] == cluster_id:
                members.append(names_6[i])
        cx = iter1_centroids[cluster_id]
        print("  Cluster {}: {} -> centroid = ({:.4f}, {:.4f})".format(
            cluster_id + 1, members, cx[0], cx[1]))

    print()
    print("  Expected from exercise:")
    print("    Cluster 1 (Andrew): {Andrew, Dennis} -> centroid = (68.5, 2.0)")
    print("    Cluster 2 (Carolina): {Bernhard, Carolina, Eve, Fred} -> centroid = (37.25, 3.8)")

    print()
    print("  --- Final K-Means Result ---")
    print_clusters(assignments_6, names_6, k=2)
    print()
    print("  Final centroids:")
    for i in range(len(centroids_6)):
        print("    Centroid {}: ({:.4f}, {:.4f})".format(i + 1, centroids_6[i][0], centroids_6[i][1]))
    print()
    print("  Final SSE: {:.4f}".format(sse_6[-1]))
    print("  Converged in {} iteration(s)".format(len(sse_6)))

    # ------------------------------------------------------------------
    # DEMO 2: Full 10-person Friends dataset, K=4
    # ------------------------------------------------------------------
    print_section("DEMO 2: Full 10-Person Friends Dataset, K=4")
    print()

    names_10 = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
                "Fred", "Gwyneth", "Hayden", "Irene", "James"]
    points_10 = [
        [55, 1.0],
        [43, 2.0],
        [37, 5.0],
        [82, 3.0],
        [23, 3.2],
        [46, 5.0],
        [38, 4.2],
        [50, 4.0],
        [29, 4.5],
        [42, 4.1],
    ]

    assignments_10, centroids_10, sse_history_10 = kmeans(
        points_10, k=4, seed=42
    )

    print("  Cluster assignments:")
    print_clusters(assignments_10, names_10, k=4)
    print()
    print("  Final centroids:")
    for i in range(len(centroids_10)):
        print("    Centroid {}: ({:.4f}, {:.4f})".format(
            i + 1, centroids_10[i][0], centroids_10[i][1]))
    print()
    print("  Final SSE: {:.4f}".format(sse_history_10[-1]))
    print("  Converged in {} iteration(s)".format(len(sse_history_10)))

    print()
    print("  Lecture reference clusters (K=4):")
    print("    Cluster 1: {Andrew, Bernhard, Dennis}")
    print("    Cluster 2: {Eve, Irene}")
    print("    Cluster 3: {Gwyneth, Hayden, Fred, James, Carolina}")

    # ------------------------------------------------------------------
    # DEMO 3: Elbow curve
    # ------------------------------------------------------------------
    print_section("DEMO 3: Elbow Curve (SSE vs K)")
    print()
    print("  Running K-means for K=1 to K=8 on the 10-person dataset...")
    print()

    sse_values = find_elbow(points_10, max_k=8, seed=42)

    print_elbow_chart(sse_values)

    print()
    print("  Interpretation: Look for the 'elbow' where SSE stops")
    print("  decreasing sharply. That K is a good candidate.")
    print()

    # Suggest elbow: find the K where the second derivative is largest
    # (biggest change in rate of SSE decrease)
    if len(sse_values) >= 3:
        best_elbow_k = 2
        best_diff = 0.0
        for i in range(1, len(sse_values) - 1):
            drop_before = sse_values[i - 1] - sse_values[i]
            drop_after = sse_values[i] - sse_values[i + 1]
            if drop_before > 0 and drop_after >= 0:
                ratio = drop_before / (drop_after + 1e-9)
                if ratio > best_diff:
                    best_diff = ratio
                    best_elbow_k = i + 1
        print("  Suggested elbow point: K = {}".format(best_elbow_k))

    # ------------------------------------------------------------------
    # DEMO 4: K-means++ initialization
    # ------------------------------------------------------------------
    print_section("DEMO 4: K-Means++ Initialization")
    print()
    print("  Comparing random vs K-means++ initialization on 10-person dataset (K=3)")
    print()

    # Random initialization
    _, _, sse_random = kmeans(points_10, k=3, seed=7)
    print("  Random init SSE (seed=7): {:.4f}".format(sse_random[-1]))

    # K-means++ initialization
    pp_centroids = kmeans_plus_plus_init(points_10, k=3, seed=7)
    _, _, sse_pp = kmeans(points_10, k=3, initial_centroids=pp_centroids)
    print("  K-means++ init SSE:       {:.4f}".format(sse_pp[-1]))

    print()
    print("  K-means++ initial centroid positions:")
    for i in range(len(pp_centroids)):
        print("    Centroid {}: ({:.2f}, {:.2f})".format(
            i + 1, pp_centroids[i][0], pp_centroids[i][1]))

    print()
    print("  K-means++ selects widely-spread initial centroids,")
    print("  which often leads to better final clusters.")

    print()
    print("=" * 65)
    print("  K-Means demonstration complete.")
    print("=" * 65)


if __name__ == "__main__":
    main()
