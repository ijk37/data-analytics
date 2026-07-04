"""
Project 01: Distance Measures
Chapter 5 - Clustering
Data Analytics Course

Demonstrates all distance measures from the lecture:
  - Quantitative, ordinal, nominal (single-attribute)
  - Minkowski family: Manhattan, Euclidean, general r
  - Hamming distance (strings and binary)
  - Edit / Levenshtein distance (dynamic programming)
  - Distance matrix computation
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================

import math


# =============================================================================
# SECTION 2: SINGLE-ATTRIBUTE DISTANCE FUNCTIONS
# =============================================================================

def diff_quantitative(a, b):
    """
    Compute distance between two quantitative (continuous) values.

    Formula: d(a, b) = |a - b|

    Parameters
    ----------
    a : float
        First value.
    b : float
        Second value.

    Returns
    -------
    float
        Absolute difference.

    Example
    -------
    >>> diff_quantitative(55, 37)
    18
    """
    return abs(a - b)


def diff_ordinal(a, b, n_values):
    """
    Compute distance between two ordinal values.

    Ordinal attributes have a meaningful order but intervals may not be equal.
    We normalize by mapping each value to a position in [0, 1].

    Formula: d(a, b) = |pos_a - pos_b| / (n_values - 1)

    Parameters
    ----------
    a : float or int
        Position (rank) of first value. 0-indexed.
    b : float or int
        Position (rank) of second value. 0-indexed.
    n_values : int
        Total number of distinct possible values in the ordinal scale.

    Returns
    -------
    float
        Normalized ordinal distance in [0, 1].

    Example
    -------
    Education: {none=0, primary=1, secondary=2, bachelor=3, master=4, PhD=5}
    >>> diff_ordinal(1, 4, 6)  # primary vs master
    0.6
    """
    return abs(a - b) / (n_values - 1)


def diff_nominal(a, b):
    """
    Compute distance between two nominal (categorical) values.

    Nominal attributes have no inherent order. Values are just labels.

    Formula: d(a, b) = 0 if a == b, else 1

    Parameters
    ----------
    a : any
        First category value.
    b : any
        Second category value.

    Returns
    -------
    int
        0 if equal, 1 if different.

    Example
    -------
    >>> diff_nominal("male", "female")
    1
    >>> diff_nominal("blue", "blue")
    0
    """
    if a == b:
        return 0
    return 1


# =============================================================================
# SECTION 3: MINKOWSKI DISTANCE FUNCTIONS
# =============================================================================

def minkowski_distance(point_x, point_y, r=2):
    """
    Compute the Minkowski distance between two multi-dimensional points.

    Formula: d(x, y) = ( sum_{k=1}^{d} |x_k - y_k|^r )^(1/r)

    Special cases:
      r=1 -> Manhattan / City-block distance
      r=2 -> Euclidean distance
      r -> inf -> Chebyshev distance (max of absolute differences)

    Parameters
    ----------
    point_x : list of float
        Coordinates of the first point.
    point_y : list of float
        Coordinates of the second point. Must have same length as point_x.
    r : float
        The order of the norm. Default is 2 (Euclidean).

    Returns
    -------
    float
        Minkowski distance between point_x and point_y.

    Example
    -------
    >>> minkowski_distance([55, 1], [37, 5], r=2)
    18.22  (approx)
    """
    total = 0.0
    for i in range(len(point_x)):
        diff = abs(point_x[i] - point_y[i])
        total = total + diff ** r
    return total ** (1.0 / r)


def manhattan_distance(x, y):
    """
    Compute the Manhattan (City-block) distance between two points.

    This is Minkowski distance with r=1.

    Formula: d(x, y) = sum_{k=1}^{d} |x_k - y_k|

    Parameters
    ----------
    x : list of float
        Coordinates of the first point.
    y : list of float
        Coordinates of the second point.

    Returns
    -------
    float
        Manhattan distance.
    """
    total = 0.0
    for i in range(len(x)):
        total = total + abs(x[i] - y[i])
    return total


def euclidean_distance(x, y):
    """
    Compute the Euclidean (straight-line) distance between two points.

    This is Minkowski distance with r=2.

    Formula: d(x, y) = sqrt( sum_{k=1}^{d} (x_k - y_k)^2 )

    Parameters
    ----------
    x : list of float
        Coordinates of the first point.
    y : list of float
        Coordinates of the second point.

    Returns
    -------
    float
        Euclidean distance.
    """
    total = 0.0
    for i in range(len(x)):
        diff = x[i] - y[i]
        total = total + diff * diff
    return math.sqrt(total)


# =============================================================================
# SECTION 4: HAMMING DISTANCE FUNCTIONS
# =============================================================================

def hamming_distance_string(s1, s2):
    """
    Compute the Hamming distance between two strings of equal length.

    Counts the number of character positions where the two strings differ.

    Formula: d(s1, s2) = count of positions i where s1[i] != s2[i]

    Parameters
    ----------
    s1 : str
        First string.
    s2 : str
        Second string. Must be same length as s1.

    Returns
    -------
    int
        Number of positions that differ.

    Raises
    ------
    ValueError
        If strings have different lengths.

    Examples
    --------
    d("James", "Jimmy") = 3
    d("Tom", "Tim")     = 1
    """
    if len(s1) != len(s2):
        raise ValueError(
            "Hamming distance requires strings of equal length. "
            "Got lengths " + str(len(s1)) + " and " + str(len(s2))
        )
    count = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count = count + 1
    return count


def hamming_distance_binary(b1, b2):
    """
    Compute the Hamming distance between two binary strings.

    Same as hamming_distance_string but intended for binary sequences.

    Parameters
    ----------
    b1 : str
        First binary string (e.g., "1011101").
    b2 : str
        Second binary string of same length.

    Returns
    -------
    int
        Number of bit positions that differ.

    Example
    -------
    d("1011101", "1001001") = 2
    """
    if len(b1) != len(b2):
        raise ValueError(
            "Hamming distance requires equal-length strings. "
            "Got " + str(len(b1)) + " and " + str(len(b2))
        )
    count = 0
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            count = count + 1
    return count


# =============================================================================
# SECTION 5: EDIT / LEVENSHTEIN DISTANCE
# =============================================================================

def edit_distance(s1, s2):
    """
    Compute the Levenshtein (edit) distance between two strings.

    The edit distance is the minimum number of single-character operations
    needed to transform s1 into s2:
      - Insert a character
      - Delete a character
      - Substitute one character for another

    Uses dynamic programming for efficient computation.

    Parameters
    ----------
    s1 : str
        Source string.
    s2 : str
        Target string.

    Returns
    -------
    int
        Minimum edit distance.

    Example
    -------
    d("Johnny", "Jonston") = 5
    """
    n = len(s1)
    m = len(s2)

    # Build a (n+1) x (m+1) matrix
    # dp[i][j] = edit distance between s1[0..i-1] and s2[0..j-1]
    dp = []
    for i in range(n + 1):
        row = []
        for j in range(m + 1):
            row.append(0)
        dp.append(row)

    # Base cases: transforming empty string
    for i in range(n + 1):
        dp[i][0] = i   # delete i characters from s1
    for j in range(m + 1):
        dp[0][j] = j   # insert j characters into s1

    # Fill in the rest of the matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match: no additional cost
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take the minimum of three operations
                delete_cost = dp[i - 1][j] + 1      # delete from s1
                insert_cost = dp[i][j - 1] + 1      # insert into s1
                subst_cost  = dp[i - 1][j - 1] + 1  # substitute
                dp[i][j] = min(delete_cost, insert_cost, subst_cost)

    return dp[n][m]


# =============================================================================
# SECTION 6: DISTANCE MATRIX
# =============================================================================

def compute_distance_matrix(points, dist_func):
    """
    Compute the full pairwise distance matrix for a set of points.

    Parameters
    ----------
    points : list
        List of points. Each point can be any type supported by dist_func.
    dist_func : function
        A function that takes two points and returns their distance.

    Returns
    -------
    list of list of float
        n x n matrix where matrix[i][j] = dist_func(points[i], points[j]).

    Example
    -------
    >>> pts = [[1, 2], [3, 4], [5, 6]]
    >>> compute_distance_matrix(pts, euclidean_distance)
    """
    n = len(points)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            dist = dist_func(points[i], points[j])
            row.append(dist)
        matrix.append(row)
    return matrix


def print_distance_matrix(matrix, names):
    """
    Print a distance matrix in a formatted grid.

    Parameters
    ----------
    matrix : list of list of float
        The distance matrix.
    names : list of str
        Labels for rows and columns.
    """
    # Determine column width
    col_w = 8

    # Header row
    header = " " * 10
    for name in names:
        header = header + name[:col_w].rjust(col_w)
    print(header)

    # Data rows
    for i in range(len(matrix)):
        row_str = names[i][:10].ljust(10)
        for j in range(len(matrix[i])):
            val = matrix[i][j]
            row_str = row_str + ("{:.2f}".format(val)).rjust(col_w)
        print(row_str)


# =============================================================================
# SECTION 7: DEMONSTRATION HELPERS
# =============================================================================

def print_section(title):
    """Print a formatted section header."""
    print()
    print("=" * 60)
    print("  " + title)
    print("=" * 60)


def print_subsection(title):
    """Print a formatted subsection header."""
    print()
    print("  --- " + title + " ---")


# =============================================================================
# SECTION 8: MAIN DEMONSTRATION
# =============================================================================

def main():
    """
    Run all demonstrations for distance measures.

    Covers:
      1. Single-attribute distances (quantitative, ordinal, nominal)
      2. Minkowski distances (r = 1, 2, 3, inf approximation)
      3. Hamming distance for strings and binary sequences
      4. Edit (Levenshtein) distance
      5. Pairwise distance matrix for the Friends dataset
    """

    # ------------------------------------------------------------------
    # DEMO 1: Single-attribute distances
    # ------------------------------------------------------------------
    print_section("DEMO 1: Single-Attribute Distances (Friends Dataset)")
    print()
    print("Comparing Andrew (Age=55, Education=1) vs Carolina (Age=37, Education=5)")
    print()

    # Quantitative: age
    age_andrew = 55
    age_carolina = 37
    age_diff = diff_quantitative(age_andrew, age_carolina)
    print("  Quantitative distance (Age):")
    print("    d({}, {}) = |{} - {}| = {}".format(
        age_andrew, age_carolina, age_andrew, age_carolina, age_diff))

    # Ordinal: education
    # Education scale: {1, 2, 3, 4, 5} mapped to positions 0..4
    # Andrew=1 -> position 0, Carolina=5 -> position 4, n_values=5
    edu_andrew_pos = 0    # position of education=1 in {1,2,3,4,5}
    edu_carolina_pos = 4  # position of education=5 in {1,2,3,4,5}
    n_edu = 5             # there are 5 distinct education values
    edu_diff = diff_ordinal(edu_andrew_pos, edu_carolina_pos, n_edu)
    print()
    print("  Ordinal distance (Education, scale {1,2,3,4,5}, n=5):")
    print("    Andrew pos=0, Carolina pos=4")
    print("    d(0, 4) = |0 - 4| / (5 - 1) = 4 / 4 = {:.4f}".format(edu_diff))

    # Nominal: names
    name_diff = diff_nominal("Andrew", "Carolina")
    print()
    print("  Nominal distance (Name):")
    print("    d('Andrew', 'Carolina') = {} (different names)".format(name_diff))

    same_name_diff = diff_nominal("Andrew", "Andrew")
    print("    d('Andrew', 'Andrew')   = {} (same name)".format(same_name_diff))

    # ------------------------------------------------------------------
    # DEMO 2: Minkowski distances
    # ------------------------------------------------------------------
    print_section("DEMO 2: Minkowski Distance (Andrew vs Carolina)")
    print()
    print("Andrew = (55, 1),  Carolina = (37, 5)")
    print()

    andrew = [55, 1]
    carolina = [37, 5]

    # r = 1: Manhattan
    d_r1 = manhattan_distance(andrew, carolina)
    print("  r=1 (Manhattan):  |55-37| + |1-5| = 18 + 4 = {:.4f}".format(d_r1))

    # r = 2: Euclidean
    d_r2 = euclidean_distance(andrew, carolina)
    print("  r=2 (Euclidean):  sqrt(18^2 + 4^2) = sqrt(324+16) = {:.4f}".format(d_r2))

    # r = 3: General Minkowski
    d_r3 = minkowski_distance(andrew, carolina, r=3)
    print("  r=3 (Minkowski):  (18^3 + 4^3)^(1/3) = {:.4f}".format(d_r3))

    # r = 10: approximation of Chebyshev (should approach 18)
    d_r10 = minkowski_distance(andrew, carolina, r=10)
    print("  r=10 (approx Chebyshev): {:.4f}  (approaches max(18,4)=18)".format(d_r10))

    print()
    print("  Note: As r increases, the distance approaches the maximum")
    print("  absolute difference in any single dimension (Chebyshev).")

    # ------------------------------------------------------------------
    # DEMO 3: Hamming distance
    # ------------------------------------------------------------------
    print_section("DEMO 3: Hamming Distance")
    print()

    # String example from lecture
    s1 = "James"
    s2 = "Jimmy"
    d_h = hamming_distance_string(s1, s2)
    print("  String Hamming distance:")
    print("    s1 = '{}'".format(s1))
    print("    s2 = '{}'".format(s2))
    print("    Comparing character by character:")
    for i in range(len(s1)):
        match = "same" if s1[i] == s2[i] else "DIFF"
        print("      pos {}: '{}' vs '{}' -> {}".format(i, s1[i], s2[i], match))
    print("    d('{}', '{}') = {}".format(s1, s2, d_h))

    print()
    s3 = "Tom"
    s4 = "Tim"
    d_h2 = hamming_distance_string(s3, s4)
    print("  Another example:")
    print("    d('{}', '{}') = {}".format(s3, s4, d_h2))

    # Binary Hamming distance from lecture
    print()
    b1 = "1011101"
    b2 = "1001001"
    d_bin = hamming_distance_binary(b1, b2)
    print("  Binary Hamming distance:")
    print("    b1 = '{}'".format(b1))
    print("    b2 = '{}'".format(b2))
    print("    Bit comparison:")
    for i in range(len(b1)):
        match = "same" if b1[i] == b2[i] else "DIFF"
        print("      pos {}: {} vs {} -> {}".format(i, b1[i], b2[i], match))
    print("    d('{}', '{}') = {}".format(b1, b2, d_bin))

    # ------------------------------------------------------------------
    # DEMO 4: Edit distance
    # ------------------------------------------------------------------
    print_section("DEMO 4: Edit (Levenshtein) Distance")
    print()

    pairs = [
        ("Johnny", "Jonston"),
        ("kitten", "sitting"),
        ("data", "date"),
        ("", "abc"),
    ]

    for str_a, str_b in pairs:
        d_edit = edit_distance(str_a, str_b)
        print("  d('{}', '{}') = {}".format(str_a, str_b, d_edit))

    print()
    print("  Lecture example verified: d('Johnny', 'Jonston') =", edit_distance("Johnny", "Jonston"))
    print("  (Expected: 5)")

    # ------------------------------------------------------------------
    # DEMO 5: Distance matrix for Friends dataset
    # ------------------------------------------------------------------
    print_section("DEMO 5: Distance Matrix for Friends Dataset (Euclidean)")
    print()
    print("  Using Age and Education as the two dimensions.")
    print()

    # Friends dataset: (Age, Education)
    friends = {
        "Andrew":   [55, 1.0],
        "Bernhard": [43, 2.0],
        "Carolina": [37, 5.0],
        "Dennis":   [82, 3.0],
        "Eve":      [23, 3.2],
        "Fred":     [46, 5.0],
    }

    names = list(friends.keys())
    points = []
    for name in names:
        points.append(friends[name])

    # Compute Euclidean distance matrix
    dist_matrix = compute_distance_matrix(points, euclidean_distance)

    print_distance_matrix(dist_matrix, names)

    # Verify some distances against the exercise answers
    print()
    print("  Verification against Exercise Q1 answers:")
    print("  (Andrew to each person, rounded to 2 decimal places)")
    print()
    andrew_idx = names.index("Andrew")
    for i in range(len(names)):
        d = dist_matrix[andrew_idx][i]
        print("    Andrew -> {:10s} : {:.2f}".format(names[i], d))

    print()
    print("  Exercise Q1 reference distances to Andrew:")
    print("    A=0.00, B=12.04, C=18.44, D=27.02, E=32.58, F=9.85")

    # Show Carolina distances too
    print()
    print("  Distances from Carolina:")
    carolina_idx = names.index("Carolina")
    for i in range(len(names)):
        d = dist_matrix[carolina_idx][i]
        print("    Carolina -> {:10s} : {:.2f}".format(names[i], d))

    print()
    print("  Exercise Q1 reference distances to Carolina:")
    print("    A=17.2, B=6.7, C=0, D=45.2, E=14.0, F=9.0")

    print()
    print("=" * 60)
    print("  All distance measure demonstrations complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
