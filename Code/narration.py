"""
Narration script for every scene, keyed by scene and step.
Text is written for the speech engine (e.g. "2 by 3" rather than "2×3").
`python Code/narration.py` prints the full script as Markdown.
"""

N = {
    # ---------------------------------------------------------------- Title
    "title": (
        "Hi! In this video we'll answer a simple question: what actually is a matrix? "
        "Then we'll learn how to add matrices, scale them by a number, and multiply them, "
        "and see why multiplication works the way it does."
    ),
    # ---------------------------------------------------------------- What is a matrix
    "w1": (
        "Let's start with something familiar. Two stationery shops record how many pens, "
        "notebooks and erasers they sold in January. Shop 1 sold 3 pens, 5 notebooks and 2 erasers. "
        "Shop 2 sold 4 pens, 1 notebook and 6 erasers."
    ),
    "w2": (
        "If we keep the numbers and drop the labels, we get a matrix: a rectangular array of numbers, "
        "arranged in rows and columns. We name a matrix with a capital letter. Let's call this one A."
    ),
    "w3": (
        "Each horizontal line of numbers is a row. Here, every row is one shop. "
        "Each vertical line is a column, and every column is one item."
    ),
    "w4": (
        "A has 2 rows and 3 columns, so we say A is a 2 by 3 matrix. We always write rows first, "
        "then columns. In general, a matrix with m rows and n columns is called m by n."
    ),
    "w5": (
        "To point at a single entry, we use a small letter with two subscripts: a, sub i j, "
        "is the entry in row i and column j. For example, a sub 2 3 sits in row 2, column 3. "
        "It's 6, so shop 2 sold 6 erasers."
    ),
    "w5b": (
        "And a sub 1 2 is 5: the notebooks sold by shop 1. "
        "So the position of a number carries meaning: it tells us which shop, and which item."
    ),
    # ---------------------------------------------------------------- Transformation view
    "w6": (
        "A matrix can also describe a transformation of space. "
        "Take this 2 by 2 matrix T, whose columns are 2 0, and 1 1."
    ),
    "w7": (
        "The first column tells us where the unit vector i hat lands, and the second column "
        "tells us where j hat lands. Watch the whole grid move along with them."
    ),
    "w8": (
        "So where does the vector 1 2 go? It was 1 step of i hat plus 2 steps of j hat, "
        "and grid lines stay parallel and evenly spaced. So it lands on 1 times 2 0, plus 2 times 1 1, "
        "which is 4 2. Combining columns like this is the heart of matrix multiplication."
    ),
    # ---------------------------------------------------------------- Addition
    "a1": (
        "Now February's sales arrive as a second matrix, B. Same shops in the same rows, "
        "and the same items in the same columns."
    ),
    "a2": (
        "To find the total sales, we add matching entries. 3 plus 2 is 5 pens for shop 1. "
        "5 plus 3 is 8 notebooks. And we do the same for every position."
    ),
    "a3": (
        "So A plus B is the 2 by 3 matrix: 5 8 3, 9 3 6. In symbols, the i j entry of A plus B "
        "is a i j plus b i j."
    ),
    "a4": (
        "This only works when both matrices have the same dimensions. If we try to add a 2 by 3 matrix "
        "to a 2 by 2 matrix, the third column has no partner, so the sum is undefined."
    ),
    # ---------------------------------------------------------------- Scalar multiplication
    "s1": (
        "Suppose the shops expect sales to double. We multiply the whole matrix by the number 2. "
        "A single number like this is called a scalar."
    ),
    "s2": (
        "Scalar multiplication multiplies every entry by the scalar. 2 times 3 is 6, 2 times 5 is 10, "
        "and so on. The rule is: entry i j of c A equals c times a i j."
    ),
    "s3": (
        "Geometrically, multiplying a vector by a positive scalar stretches it without changing its "
        "direction. Times 2 doubles its length. A negative scalar, like minus 1, flips it around."
    ),
    # ---------------------------------------------------------------- Matrix × vector
    "m1": (
        "Now the most interesting operation: matrix multiplication. A pen costs 10 rupees, "
        "a notebook 20, and an eraser 5. We store these prices as a 3 by 1 column vector, p."
    ),
    "m2": (
        "What was shop 1's revenue? We pair each quantity with its price: 3 times 10, "
        "plus 5 times 20, plus 2 times 5. That's 30 plus 100 plus 10, which is 140 rupees."
    ),
    "m3": (
        "Notice what we did. We took row 1 of A and the column p, multiplied matching entries, "
        "and added them up. This is called the dot product of a row with a column."
    ),
    "m4": (
        "For shop 2, we use row 2: 4 times 10, plus 1 times 20, plus 6 times 5. "
        "That's 40 plus 20 plus 30, which gives 90."
    ),
    "m5": (
        "So A times p is the column 140, 90: one revenue for each shop. That's the rule: "
        "the i j entry of a product is row i of the first matrix, dotted with column j of the second."
    ),
    "m6": (
        "Look at the dimensions. A is 2 by 3, and p is 3 by 1. The inner numbers must match, "
        "because each row of A needs exactly one partner for each of its 3 entries. "
        "The outer numbers, 2 by 1, give the size of the answer. In general, an m by n matrix "
        "times an n by k matrix gives an m by k matrix."
    ),
    # ---------------------------------------------------------------- Matrix × matrix
    "m7": (
        "Let's multiply two 2 by 2 matrices, P and Q. Top left entry: row 1 of P dotted with "
        "column 1 of Q. 2 times 1, plus 0 times 2, is 2."
    ),
    "m8a": "Top right: row 1 with column 2. 2 times 4, plus 0 times minus 1, is 8.",
    "m8b": "Bottom left: row 2 with column 1. 1 times 1, plus 3 times 2, is 7.",
    "m8c": "Bottom right: row 2 with column 2. 1 times 4, plus 3 times minus 1, is 1.",
    "m9": (
        "So P Q is 2 8, 7 1. But if we swap the order, Q P works out to 6 12, 3 minus 3. "
        "A different answer! Matrix multiplication is not commutative: in general, "
        "A B is not equal to B A."
    ),
    "m10": (
        "Why? Think of matrices as transformations. P Q times x means P applied to Q x: "
        "first Q acts, then P. Like putting on socks and then shoes, the order matters."
    ),
    # ---------------------------------------------------------------- Summary
    "z1": "Let's summarise.",
    "z2": (
        "A matrix is a rectangular array of numbers. Its size is rows by columns, "
        "and a i j is the entry in row i, column j."
    ),
    "z3": "Addition works entry by entry, and needs matrices of the same size.",
    "z4": "Scalar multiplication multiplies every entry by the same number.",
    "z5": (
        "And matrix multiplication combines rows with columns. The inner dimensions must match, "
        "and the order matters."
    ),
    "z6": "Thanks for watching!",
}

if __name__ == "__main__":
    print("# Narration script\n")
    for k, v in N.items():
        print(f"**{k}** — {v}\n")
