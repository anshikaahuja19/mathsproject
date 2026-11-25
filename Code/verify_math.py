"""
Independent check of every worked example shown in the video.
Run:  python Code/verify_math.py      (all asserts must pass)
"""
import numpy as np

# --- What is a matrix? -------------------------------------------------------
A = np.array([[3, 5, 2],    # Shop 1: pens, notebooks, erasers (January)
              [4, 1, 6]])   # Shop 2
assert A.shape == (2, 3)                 # 2 rows x 3 columns
assert A[1, 2] == 6                      # a_23 (maths is 1-indexed)
assert A[0, 1] == 5                      # a_12

# --- Matrix as a transformation ---------------------------------------------
T = np.array([[2, 1],
              [0, 1]])
assert (T @ [1, 0] == [2, 0]).all()      # i-hat -> first column
assert (T @ [0, 1] == [1, 1]).all()      # j-hat -> second column
v = np.array([1, 2])
assert (T @ v == 1 * T[:, 0] + 2 * T[:, 1]).all()
assert (T @ v == [4, 2]).all()

# --- Addition ---------------------------------------------------------------
B = np.array([[2, 3, 1],
              [5, 2, 0]])               # February
assert (A + B == [[5, 8, 3], [9, 3, 6]]).all()

# --- Scalar multiplication --------------------------------------------------
assert (2 * A == [[6, 10, 4], [8, 2, 12]]).all()
assert (2 * v == [2, 4]).all() and (-1 * v == [-1, -2]).all()

# --- Matrix x vector (revenue) ----------------------------------------------
p = np.array([[10], [20], [5]])         # price of pen, notebook, eraser (Rs)
assert 3 * 10 + 5 * 20 + 2 * 5 == 140
assert 4 * 10 + 1 * 20 + 6 * 5 == 90
assert (A @ p == [[140], [90]]).all()
assert (A @ p).shape == (2, 1)

# --- Matrix x matrix ---------------------------------------------------------
P = np.array([[2, 0],
              [1, 3]])
Q = np.array([[1, 4],
              [2, -1]])
assert (P @ Q == [[2, 8], [7, 1]]).all()
assert (Q @ P == [[6, 12], [3, -3]]).all()
assert not (P @ Q == Q @ P).all()        # not commutative
x = np.array([1, 1])
assert (P @ Q @ x == P @ (Q @ x)).all()  # (PQ)x = P(Qx)

print("All worked examples verified.")
print("A + B =\n", A + B, "\n2A =\n", 2 * A, "\nAp =\n", A @ p)
print("PQ =\n", P @ Q, "\nQP =\n", Q @ P)
