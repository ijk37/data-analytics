"""
Project 03: Hierarchical and Density-Based Clustering
Chapter 5 - Clustering
Data Analytics Course

Implements from scratch:
  - Agglomerative hierarchical clustering with 4 linkage methods
  - ASCII dendrogram visualization
  - DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

Uses Friends dataset for hierarchical clustering.
Uses synthetic 2D data for DBSCAN demonstration.
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================

import math
import csv


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
            Keys are column headers, values are lists.
            Numeric columns stored as floats, others as strings.
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
# SECTION 3: DISTANCE UTILITIES
# =============================================================================

def euclidean_distance(p1, p2):
    """
    Compute Euclidean distance between two points (any dimension).

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


def build_distance_matrix(points):
    """
    Build the full pairwise Euclidean distance matrix.

    Parameters
    ----------
    points : list of list of float

    Returns
    -------
    list of list of float
        n x n symmetric matrix.
    """
    n = len(points)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(euclidean_distance(points[i], points[j]))
        matrix.append(row)
    return matrix


# =============================================================================
# SECTION 4: LINKAGE DISTANCE FUNCTIONS
# =============================================================================

def single_linkage_distance(cluster_a, cluster_b, dist_matrix):
    """
    Compute MIN (single) linkage distance between two clusters.

    d(A, B) = min_{i in A, j in B} dist_matrix[i][j]

    Parameters
    ----------
    cluster_a : list of int
        Indices of points in cluster A.
    cluster_b : list of int
        Indices of points in cluster B.
    dist_matrix : list of list of float
        Precomputed pairwise distance matrix.

    Returns
    -------
    float
        Minimum pairwise distance.
    """
    min_dist = None
    for i in cluster_a:
        for j in cluster_b:
            d = dist_matrix[i][j]
            if min_dist is None or d < min_dist:
                min_dist = d
    return min_dist


def complete_linkage_distance(cluster_a, cluster_b, dist_matrix):
    """
    Compute MAX (complete) linkage distance between two clusters.

    d(A, B) = max_{i in A, j in B} dist_matrix[i][j]

    Parameters
    ----------
    cluster_a : list of int
    cluster_b : list of int
    dist_matrix : list of list of float

    Returns
    -------
    float
        Maximum pairwise distance.
    """
    max_dist = None
    for i in cluster_a:
        for j in cluster_b:
            d = dist_matrix[i][j]
            if max_dist is None or d > max_dist:
                max_dist = d
    return max_dist


def average_linkage_distance(cluster_a, cluster_b, dist_matrix):
    """
    Compute average (group average) linkage distance between two clusters.

    d(A, B) = (1 / (|A| * |B|)) * sum_{i in A} sum_{j in B} dist_matrix[i][j]

    Parameters
    ----------
    cluster_a : list of int
    cluster_b : list of int
    dist_matrix : list of list of float

    Returns
    -------
    float
        Average pairwise distance.
    """
    total = 0.0
    count = 0
    for i in cluster_a:
        for j in cluster_b:
            total = total + dist_matrix[i][j]
            count = count + 1
    if count == 0:
        return 0.0
    return total / count


def ward_distance(cluster_a, cluster_b, dist_matrix, cluster_sizes):
    """
    Compute Ward's linkage distance between two clusters.

    Ward's method minimizes the increase in SSE (total within-cluster variance)
    when merging two clusters. The merge distance is:

    delta_SSE(A, B) = (|A| * |B|) / (|A| + |B|) * dist^2(centroid_A, centroid_B)

    Since we don't have raw points here (only distances), we use the average
    squared distance as an approximation:
    ward_dist = sqrt( (|A|*|B|) / (|A|+|B|) ) * avg_dist(A, B)

    Parameters
    ----------
    cluster_a : list of int
    cluster_b : list of int
    dist_matrix : list of list of float
    cluster_sizes : list of int
        cluster_sizes[i] = number of original points in cluster i.
        (Note: cluster_a and cluster_b are lists of point indices,
         so their sizes are len(cluster_a) and len(cluster_b).)

    Returns
    -------
    float
        Ward's distance (proportional to increase in SSE).
    """
    size_a = len(cluster_a)
    size_b = len(cluster_b)

    # Compute average distance between the two clusters
    avg_dist = average_linkage_distance(cluster_a, cluster_b, dist_matrix)

    # Ward scaling factor
    scale = math.sqrt((size_a * size_b) / (size_a + size_b))
    return scale * avg_dist


# =============================================================================
# SECTION 5: AGGLOMERATIVE CLUSTERING
# =============================================================================

def agglomerative_clustering(points, n_clusters, linkage="ward"):
    """
    Perform agglomerative (bottom-up) hierarchical clustering.

    Algorithm:
      1. Start with n singleton clusters (each point is its own cluster).
      2. Compute pairwise distances between all clusters.
      3. Merge the two closest clusters (by the chosen linkage).
      4. Repeat until the desired number of clusters is reached.

    Parameters
    ----------
    points : list of list of float
        Data points.
    n_clusters : int
        Target number of clusters to return.
    linkage : str
        One of "single", "complete", "average", "ward". Default "ward".

    Returns
    -------
    tuple : (assignments, merge_history)
        assignments : list of int
            Cluster label for each point (0-indexed).
        merge_history : list of dict
            Each entry: {"cluster_a": ..., "cluster_b": ..., "distance": ...,
                         "new_cluster": ..., "merged_size": ...}
    """
    n = len(points)
    dist_matrix = build_distance_matrix(points)

    # Initialize: each point is its own cluster
    # clusters is a list of lists: clusters[i] = list of point indices in cluster i
    clusters = []
    for i in range(n):
        clusters.append([i])

    merge_history = []

    # Merge until we have n_clusters
    while len(clusters) > n_clusters:
        # Find the two closest clusters
        best_i = 0
        best_j = 1
        best_dist = None

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Compute linkage distance between clusters[i] and clusters[j]
                if linkage == "single":
                    d = single_linkage_distance(clusters[i], clusters[j], dist_matrix)
                elif linkage == "complete":
                    d = complete_linkage_distance(clusters[i], clusters[j], dist_matrix)
                elif linkage == "average":
                    d = average_linkage_distance(clusters[i], clusters[j], dist_matrix)
                elif linkage == "ward":
                    d = ward_distance(clusters[i], clusters[j], dist_matrix, None)
                else:
                    raise ValueError("Unknown linkage: " + linkage)

                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_i = i
                    best_j = j

        # Merge clusters[best_i] and clusters[best_j]
        merged = clusters[best_i] + clusters[best_j]
        merge_history.append({
            "cluster_a_indices": clusters[best_i][:],
            "cluster_b_indices": clusters[best_j][:],
            "distance": best_dist,
            "merged_indices": merged[:]
        })

        # Remove the two clusters and add the merged one
        # Remove in reverse order to preserve indices
        if best_i < best_j:
            clusters.pop(best_j)
            clusters.pop(best_i)
        else:
            clusters.pop(best_i)
            clusters.pop(best_j)
        clusters.append(merged)

    # Build assignments array
    assignments = [0] * n
    for cluster_id in range(len(clusters)):
        for point_idx in clusters[cluster_id]:
            assignments[point_idx] = cluster_id

    return assignments, merge_history


# =============================================================================
# SECTION 6: ASCII DENDROGRAM
# =============================================================================

def print_dendrogram_ascii(merge_history, names):
    """
    Print an ASCII text dendrogram showing the merge sequence.

    For each merge step, shows which clusters were combined and at what distance.

    Parameters
    ----------
    merge_history : list of dict
        From agglomerative_clustering().
    names : list of str
        Name for each original point (by index).
    """
    print("  Merge sequence (bottom-up):")
    print()
    print("  Step | Distance | Clusters merged")
    print("  -----+----------+---------------------------------")

    for step_num in range(len(merge_history)):
        step = merge_history[step_num]
        dist = step["distance"]

        a_names = [names[i] for i in step["cluster_a_indices"]]
        b_names = [names[i] for i in step["cluster_b_indices"]]

        a_str = "{" + ", ".join(a_names) + "}"
        b_str = "{" + ", ".join(b_names) + "}"

        print("  {:4d} | {:8.4f} | {} + {}".format(
            step_num + 1, dist, a_str, b_str))

    print()

    # Show the full merge tree as a text diagram
    print("  Merge tree (each level shows newly merged group):")
    print()
    indent_levels = {}
    for i in range(len(names)):
        indent_levels[i] = 0

    for step_num in range(len(merge_history)):
        step = merge_history[step_num]
        dist = step["distance"]
        merged = step["merged_indices"]
        merged_names = [names[i] for i in merged]

        indent = "  " * (step_num + 1)
        print("  Step {:2d} (dist={:.2f}): [{}]".format(
            step_num + 1,
            dist,
            " | ".join(merged_names)))


# =============================================================================
# SECTION 7: DBSCAN
# =============================================================================

def dbscan(points, eps, min_pts):
    """
    DBSCAN: Density-Based Spatial Clustering of Applications with Noise.

    Classifies each point as:
      - Core point: has >= min_pts points (including itself) within distance eps
      - Border point: not core, but within eps of a core point
      - Noise point: neither core nor border -> labeled -1

    Parameters
    ----------
    points : list of list of float
        Data points.
    eps : float
        Radius for neighborhood search.
    min_pts : int
        Minimum number of points in Eps-neighborhood to be a core point.

    Returns
    -------
    list of int
        labels[i] = cluster index (0-based) for point i, or -1 for noise.
    """
    n = len(points)

    # Step 1: Classify each point as core, border, or noise
    # First, compute neighborhoods
    neighborhoods = []
    for i in range(n):
        neighbors = []
        for j in range(n):
            if euclidean_distance(points[i], points[j]) <= eps:
                neighbors.append(j)
        neighborhoods.append(neighbors)

    # Classify points
    is_core = []
    for i in range(n):
        if len(neighborhoods[i]) >= min_pts:
            is_core.append(True)
        else:
            is_core.append(False)

    # Step 2: Assign clusters using BFS/DFS from each unvisited core point
    labels = [-1] * n   # -1 = unassigned (will become noise or border)
    cluster_id = 0

    for i in range(n):
        if not is_core[i]:
            continue
        if labels[i] != -1:
            continue  # already assigned

        # Start a new cluster from this core point
        labels[i] = cluster_id

        # Use a queue to expand the cluster (BFS)
        queue = [i]
        while len(queue) > 0:
            current = queue.pop(0)
            for neighbor in neighborhoods[current]:
                if labels[neighbor] == -1:
                    # Unvisited: assign to this cluster
                    labels[neighbor] = cluster_id
                    # If neighbor is also a core point, expand from it too
                    if is_core[neighbor]:
                        queue.append(neighbor)

        cluster_id = cluster_id + 1

    # At this point:
    #   - Core points are labeled with their cluster
    #   - Border points reachable from a core point are labeled with that cluster
    #   - Remaining -1 points are noise

    return labels


def classify_points(points, labels, eps, min_pts):
    """
    Classify each point as Core, Border, or Noise for display purposes.

    Parameters
    ----------
    points : list of list of float
    labels : list of int
        From dbscan().
    eps : float
    min_pts : int

    Returns
    -------
    list of str
        "Core", "Border", or "Noise" for each point.
    """
    n = len(points)

    # Count neighbors within eps for each point
    neighbor_counts = []
    for i in range(n):
        count = 0
        for j in range(n):
            if euclidean_distance(points[i], points[j]) <= eps:
                count = count + 1
        neighbor_counts.append(count)

    classifications = []
    for i in range(n):
        if neighbor_counts[i] >= min_pts:
            classifications.append("Core")
        elif labels[i] != -1:
            classifications.append("Border")
        else:
            classifications.append("Noise")
    return classifications


# =============================================================================
# SECTION 8: MAIN DEMONSTRATION
# =============================================================================

def print_section(title):
    """Print a formatted section header."""
    print()
    print("=" * 65)
    print("  " + title)
    print("=" * 65)


def print_clusters(assignments, names, k):
    """Print cluster membership."""
    for cluster_id in range(k):
        members = []
        for i in range(len(assignments)):
            if assignments[i] == cluster_id:
                members.append(names[i])
        print("  Cluster {}: {}".format(cluster_id + 1, members))


def main():
    """
    Demonstrates hierarchical clustering and DBSCAN.

    1. Agglomerative clustering on Friends dataset with all 4 linkage methods
    2. ASCII dendrogram for Ward's linkage
    3. DBSCAN on synthetic 2D data demonstrating core/border/noise
    """

    # Friends dataset
    names = ["Andrew", "Bernhard", "Carolina", "Dennis", "Eve",
             "Fred", "Gwyneth", "Hayden", "Irene", "James"]
    points = [
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

    # ------------------------------------------------------------------
    # DEMO 1: Hierarchical clustering with all 4 linkages
    # ------------------------------------------------------------------
    print_section("DEMO 1: Agglomerative Clustering — Friends Dataset (K=3)")
    print()
    print("  Dataset: 10 persons with Age and Education attributes.")
    print()

    linkage_methods = ["single", "complete", "average", "ward"]
    linkage_display = {
        "single":   "MIN (Single Linkage)",
        "complete": "MAX (Complete Linkage)",
        "average":  "Group Average Linkage",
        "ward":     "Ward's Method",
    }

    for linkage in linkage_methods:
        print()
        print("  --- {} ---".format(linkage_display[linkage]))
        assignments, _ = agglomerative_clustering(points, n_clusters=3, linkage=linkage)
        k_actual = max(assignments) + 1
        print_clusters(assignments, names, k_actual)

    # ------------------------------------------------------------------
    # DEMO 2: Full merge sequence with Ward's linkage
    # ------------------------------------------------------------------
    print_section("DEMO 2: Merge Sequence Dendrogram (Ward's Linkage, K=1)")
    print()
    print("  Running agglomerative clustering until 1 cluster remains.")
    print("  This shows the full dendrogram sequence.")
    print()

    _, merge_history_ward = agglomerative_clustering(points, n_clusters=1, linkage="ward")
    print_dendrogram_ascii(merge_history_ward, names)

    # ------------------------------------------------------------------
    # DEMO 3: Cutting the dendrogram at different K
    # ------------------------------------------------------------------
    print_section("DEMO 3: Dendrogram Cut — Different K Values (Ward's)")
    print()

    for k in [2, 3, 4]:
        assignments_k, _ = agglomerative_clustering(points, n_clusters=k, linkage="ward")
        print("  K={} (Ward's):".format(k))
        print_clusters(assignments_k, names, k)
        print()

    # ------------------------------------------------------------------
    # DEMO 4: Hierarchical clustering — 2-person subset walkthrough
    # ------------------------------------------------------------------
    print_section("DEMO 4: Step-by-Step Walkthrough (6-Person Subset, Single Linkage)")
    print()
    print("  Using Andrew, Bernhard, Carolina, Dennis, Eve, Fred")
    print("  to show each merge step explicitly.")
    print()

    names_6 = names[:6]
    points_6 = points[:6]

    _, merge_history_6 = agglomerative_clustering(points_6, n_clusters=1, linkage="single")

    print("  Distance matrix (Euclidean):")
    dist_matrix_6 = build_distance_matrix(points_6)
    col_w = 9
    header = " " * 10
    for name in names_6:
        header = header + name[:col_w].rjust(col_w)
    print("  " + header)
    for i in range(len(names_6)):
        row_str = names_6[i].ljust(10)
        for j in range(len(names_6)):
            row_str = row_str + ("{:.2f}".format(dist_matrix_6[i][j])).rjust(col_w)
        print("  " + row_str)

    print()
    print_dendrogram_ascii(merge_history_6, names_6)

    # ------------------------------------------------------------------
    # DEMO 5: DBSCAN on synthetic data
    # ------------------------------------------------------------------
    print_section("DEMO 5: DBSCAN — Synthetic 2D Dataset")
    print()

    # Create three clusters plus some noise points
    # Cluster 1: tight group around (2, 2)
    cluster1 = [
        [2.0, 2.0], [2.1, 2.1], [1.9, 2.0], [2.0, 1.9], [2.2, 1.8],
        [1.8, 2.2], [2.1, 1.9],
    ]
    # Cluster 2: tight group around (7, 7)
    cluster2 = [
        [7.0, 7.0], [7.1, 7.2], [6.9, 7.0], [7.0, 6.8], [7.2, 7.1],
        [6.8, 6.9],
    ]
    # Cluster 3: moderate group around (2, 7)
    cluster3 = [
        [2.0, 7.0], [2.3, 7.1], [1.8, 6.9], [2.1, 7.3],
    ]
    # Noise points: isolated
    noise = [
        [5.0, 1.0], [9.0, 2.0], [0.5, 9.5],
    ]

    all_points = cluster1 + cluster2 + cluster3 + noise
    n_total = len(all_points)

    # True group labels for display
    true_groups = (
        ["C1"] * len(cluster1) +
        ["C2"] * len(cluster2) +
        ["C3"] * len(cluster3) +
        ["Noise"] * len(noise)
    )

    eps = 1.0
    min_pts = 3

    print("  Parameters: Eps={}, MinPts={}".format(eps, min_pts))
    print("  Dataset: {} points (3 dense clusters + {} noise points)".format(
        n_total, len(noise)))
    print()

    labels = dbscan(all_points, eps=eps, min_pts=min_pts)
    classifications = classify_points(all_points, labels, eps, min_pts)

    # Summary
    n_clusters = 0
    if labels:
        n_clusters = max(labels) + 1

    print("  DBSCAN found {} cluster(s)".format(n_clusters))
    noise_count = sum(1 for l in labels if l == -1)
    print("  Noise points: {}".format(noise_count))
    print()

    # Detailed results
    print("  {:5s}  {:10s}  {:12s}  {:8s}  {:10s}".format(
        "Point", "True Group", "DBSCAN Class", "Cluster", "Coords"))
    print("  " + "-" * 55)
    for i in range(n_total):
        cluster_label = "Noise" if labels[i] == -1 else str(labels[i] + 1)
        print("  {:5d}  {:10s}  {:12s}  {:8s}  ({:.1f}, {:.1f})".format(
            i, true_groups[i], classifications[i], cluster_label,
            all_points[i][0], all_points[i][1]))

    print()
    print("  Cluster membership:")
    for cid in range(n_clusters):
        members = [i for i in range(n_total) if labels[i] == cid]
        print("  Cluster {}: points {}".format(cid + 1, members))
    noise_pts = [i for i in range(n_total) if labels[i] == -1]
    print("  Noise: points {} (coordinates: {})".format(
        noise_pts,
        [all_points[i] for i in noise_pts]))

    # ------------------------------------------------------------------
    # DEMO 6: DBSCAN parameter sensitivity
    # ------------------------------------------------------------------
    print_section("DEMO 6: DBSCAN Parameter Sensitivity")
    print()
    print("  Same dataset, different Eps and MinPts combinations:")
    print()

    param_combos = [
        (0.5, 2),
        (1.0, 2),
        (1.0, 3),
        (1.5, 3),
        (2.0, 3),
    ]

    print("  {:6s}  {:7s}  {:10s}  {:12s}".format(
        "Eps", "MinPts", "Clusters", "Noise pts"))
    print("  " + "-" * 40)
    for eps_val, min_pts_val in param_combos:
        lbls = dbscan(all_points, eps=eps_val, min_pts=min_pts_val)
        n_c = max(lbls) + 1 if max(lbls) >= 0 else 0
        n_n = sum(1 for l in lbls if l == -1)
        print("  {:6.1f}  {:7d}  {:10d}  {:12d}".format(
            eps_val, min_pts_val, n_c, n_n))

    print()
    print("  Observations:")
    print("  - Small Eps or large MinPts -> more noise, fewer clusters")
    print("  - Large Eps or small MinPts -> fewer, larger clusters")
    print("  - Balance needed to capture true cluster structure")

    print()
    print("=" * 65)
    print("  Hierarchical and DBSCAN demonstration complete.")
    print("=" * 65)


if __name__ == "__main__":
    main()
