"""
M3 Animation Video — Matrices & Matrix Operations
==================================================
Manim Community v0.22 scenes (no LaTeX required).

Render one scene (preview):   manim -pql Code/scenes.py WhatIsMatrix
Render the full video:        ./Code/build.sh

Scene order
  1. Title               – opening frame
  2. WhatIsMatrix        – data table -> matrix, rows/cols, m×n, a_ij
  3. MatrixAsTransform   – columns = images of i-hat, j-hat
  4. Addition            – entry-wise, same-size rule
  5. ScalarMultiplication
  6. MatrixVector        – revenue example, row·column, dimension rule
  7. MatrixMatrix        – 2×2 product, AB ≠ BA
  8. Summary             – recap + closing credits frame
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import *  # noqa: E402,F401,F403
from narration import N  # noqa: E402


def span(text, color):
    return f'<span foreground="{color}">{text}</span>'


# ============================================================================
# 1. Title
# ============================================================================
class Title(NarratedScene):
    def construct(self):
        deco = Mat([[1, 0, 2], [3, 1, 4], [0, 5, 1]], color=GREY, font_size=30)
        deco.entries.set_opacity(0.2); deco.brackets.set_stroke(opacity=0.2)
        deco.to_corner(UR, buff=0.35)
        deco2 = Mat([[2, 1], [0, 1]], color=GREY, font_size=30)
        deco2.entries.set_opacity(0.2); deco2.brackets.set_stroke(opacity=0.2)
        deco2.to_corner(DL, buff=0.35)

        title = prose("Matrices & Matrix Operations", size=56, weight=BOLD)
        sub = prose("What a matrix represents  ·  addition  ·  scalar multiplication  ·  "
                    "matrix multiplication", size=26, color=COL_A)
        course = prose("M3 Animation Video Project  —  Linear Algebra", size=28, color=GREY)
        who = prose(f"{STUDENT_NAME}   |   Student ID: {STUDENT_ID}", size=30, color=COL_SCALAR)
        grp = VGroup(title, sub, course, who).arrange(DOWN, buff=0.45)
        grp[3].shift(DOWN * 0.3)

        with self.voice(N["title"], pause=0.6):
            self.play(FadeIn(deco), FadeIn(deco2), Write(title), run_time=2)
            self.play(FadeIn(sub, shift=UP * 0.2))
            self.play(FadeIn(course), FadeIn(who))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 2. What is a matrix?
# ============================================================================
class WhatIsMatrix(NarratedScene):
    def construct(self):
        head = title_bar("What does a matrix represent?")
        self.play(FadeIn(head))

        A = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A, font_size=60,
                col_gap=1.7, row_gap=0.55, bracket_pad=0.25)
        A.move_to(DOWN * 0.1 + RIGHT * 1.0)
        items = ["Pens", "Notebooks", "Erasers"]
        col_lab = VGroup(*[prose(t, 28, GREY).next_to(A.col(j), UP, buff=0.45)
                           for j, t in enumerate(items)])
        row_lab = VGroup(*[prose(f"Shop {i + 1}", 28, GREY).next_to(A.row(i), LEFT, buff=0.9)
                           for i in range(2)])
        caption = prose("January sales (units sold)", 30).next_to(col_lab, UP, buff=0.5)
        grid_lines = VGroup(
            Line(col_lab.get_corner(DL) + DOWN * 0.15 + LEFT * 2.2,
                 col_lab.get_corner(DR) + DOWN * 0.15 + RIGHT * 0.2, color=GREY, stroke_width=1.5),
            Line(row_lab.get_corner(UR) + RIGHT * 0.3 + UP * 0.2,
                 row_lab.get_corner(DR) + RIGHT * 0.3 + DOWN * 0.2, color=GREY, stroke_width=1.5),
        )

        # w1 — a table of data
        with self.voice(N["w1"]):
            self.play(FadeIn(caption), FadeIn(col_lab), FadeIn(row_lab), Create(grid_lines))
            self.play(LaggedStart(*[FadeIn(c, scale=1.3) for c in A.row(0)], lag_ratio=0.5),
                      run_time=2.5)
            self.play(LaggedStart(*[FadeIn(c, scale=1.3) for c in A.row(1)], lag_ratio=0.5),
                      run_time=2.5)

        # w2 — drop the labels -> matrix A
        name = math("<i>A</i>  =", size=60, color=COL_A).next_to(A, LEFT, buff=0.4)
        defn = prose("Matrix: a rectangular array of numbers arranged in rows and columns",
                     28).to_edge(DOWN, buff=0.6)
        with self.voice(N["w2"]):
            self.play(FadeOut(col_lab), FadeOut(row_lab), FadeOut(grid_lines), FadeOut(caption))
            self.play(Create(A.brackets), run_time=1.2)
            self.play(Write(defn), run_time=2)
            self.play(Write(name))

        # w3 — rows and columns
        rboxes = VGroup(*[A.row_box(i) for i in range(2)])
        rlabs = VGroup(*[prose(f"row {i + 1}", 26, COL_ROW).next_to(rboxes[i], RIGHT, buff=0.3)
                         for i in range(2)])
        cboxes = VGroup(*[A.col_box(j) for j in range(3)])
        clabs = VGroup(*[prose(f"column {j + 1}", 24, COL_COL).next_to(cboxes[j], UP, buff=0.2)
                         for j in range(3)])
        with self.voice(N["w3"]):
            self.play(LaggedStart(*[Create(b) for b in rboxes], lag_ratio=0.4),
                      FadeIn(rlabs), run_time=1.5)
            self.wait(1.2)
            self.play(FadeOut(rboxes), FadeOut(rlabs))
            self.play(LaggedStart(*[Create(b) for b in cboxes], lag_ratio=0.3),
                      FadeIn(clabs), run_time=1.5)
            self.wait(0.8)
            self.play(FadeOut(cboxes), FadeOut(clabs))

        # w4 — dimensions
        brace_r = Brace(A, RIGHT, color=COL_ROW)
        brace_c = Brace(A, UP, color=COL_COL)
        lab_r = prose("2 rows", 26, COL_ROW).next_to(brace_r, RIGHT, buff=0.15)
        lab_c = prose("3 columns", 26, COL_COL).next_to(brace_c, UP, buff=0.15)
        dim = math(f"<i>A</i> is {span('2', COL_ROW)} × {span('3', COL_COL)}", size=44)
        gen = math(f"{span('<i>m</i>', COL_ROW)} × {span('<i>n</i>', COL_COL)}  =  "
                   f"{span('rows', COL_ROW)} × {span('columns', COL_COL)}", size=40)
        VGroup(dim, gen).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.6)
        with self.voice(N["w4"]):
            self.play(FadeOut(defn), GrowFromCenter(brace_c), FadeIn(lab_c))
            self.play(GrowFromCenter(brace_r), FadeIn(lab_r))
            self.play(Write(dim))
            self.wait(1)
            self.play(Write(gen))

        # w5 — entry notation a_ij
        self.play(FadeOut(VGroup(brace_r, brace_c, lab_r, lab_c, gen)), dim.animate.to_corner(DL, buff=0.5))
        aij = math(f"<i>a</i><sub>{span('<i>i</i>', COL_ROW)}{span('<i>j</i>', COL_COL)}</sub>"
                   f"  =  entry in {span('row <i>i</i>', COL_ROW)}, {span('column <i>j</i>', COL_COL)}",
                   size=40).next_to(head, DOWN, buff=0.35)
        r2 = A.row_box(1)
        c3 = A.col_box(2)
        e23 = A.entry_box(1, 2, color=WHITE, buff=0.16)
        a23 = math(f"<i>a</i><sub>{span('2', COL_ROW)}{span('3', COL_COL)}</sub> = 6", size=44)
        a23_m = prose("Shop 2 sold 6 erasers", 28, GREY)
        VGroup(a23, a23_m).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.6).shift(RIGHT * 1.5)
        with self.voice(N["w5"]):
            self.play(Write(aij), run_time=2)
            self.wait(1.5)
            self.play(Create(r2))
            self.play(Create(c3))
            self.play(Create(e23), A.entry(1, 2).animate.set_color(WHITE).scale(1.15))
            self.play(FadeIn(a23), FadeIn(a23_m))

        e12 = A.entry_box(0, 1, color=WHITE, buff=0.16)
        a12 = math(f"<i>a</i><sub>{span('1', COL_ROW)}{span('2', COL_COL)}</sub> = 5", size=44)
        a12_m = prose("Shop 1 sold 5 notebooks", 28, GREY)
        VGroup(a12, a12_m).arrange(RIGHT, buff=0.5).move_to(VGroup(a23, a23_m))
        with self.voice(N["w5b"], pause=0.6):
            self.play(FadeOut(VGroup(r2, c3, e23)), A.entry(1, 2).animate.set_color(COL_A).scale(1 / 1.15),
                      FadeOut(VGroup(a23, a23_m)))
            self.play(Create(e12), A.entry(0, 1).animate.set_color(WHITE).scale(1.15))
            self.play(FadeIn(a12), FadeIn(a12_m))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 3. Matrix as a transformation
# ============================================================================
class MatrixAsTransform(NarratedScene):
    def construct(self):
        U = 1.35  # screen units per grid square
        O = np.array([-5.2, -2.6, 0])
        plane = NumberPlane(x_range=[-6, 16, 1], y_range=[-6, 9, 1], x_length=22 * U, y_length=15 * U,
                            background_line_style={"stroke_color": "#2E5C73", "stroke_width": 1.5,
                                                   "stroke_opacity": 0.8},
                            axis_config={"stroke_color": GREY})
        plane.shift(O - plane.c2p(0, 0))
        ghost = plane.copy().set_opacity(0.18)

        def arrow(vec, color):
            return Arrow(O, O + U * np.array([*vec, 0]), buff=0, color=color,
                         stroke_width=6, max_tip_length_to_length_ratio=0.2)

        Tm = [[2, 1], [0, 1]]
        T = Mat(Tm, font_size=48)
        T.cells[0][0].set_color(COL_I); T.cells[1][0].set_color(COL_I)
        T.cells[0][1].set_color(COL_J); T.cells[1][1].set_color(COL_J)
        Tl = labelled(T, "T", WHITE)
        panel_bg = BackgroundRectangle(Tl, color=BG, fill_opacity=0.9, buff=0.3)
        panel = VGroup(panel_bg, Tl).to_corner(UR, buff=0.4)
        head = prose("A matrix as a transformation", 34, weight=BOLD).to_corner(UL, buff=0.4)
        head_bg = BackgroundRectangle(head, color=BG, fill_opacity=0.9, buff=0.2)

        with self.voice(N["w6"]):
            self.play(Create(plane), run_time=1.5)
            self.add(ghost)
            self.play(FadeIn(head_bg), FadeIn(head), FadeIn(panel))
            self.play(Indicate(T.col(0), color=COL_I))
            self.play(Indicate(T.col(1), color=COL_J))

        i_hat = arrow([1, 0], COL_I)
        j_hat = arrow([0, 1], COL_J)
        i_lab = math("î", 40, COL_I).next_to(i_hat, DOWN, buff=0.1)
        j_lab = math("ĵ", 40, COL_J).next_to(j_hat, LEFT, buff=0.1)
        i_new = arrow([2, 0], COL_I)
        j_new = arrow([1, 1], COL_J)
        i_res = math(f"<i>T</i> î = {span('(2, 0)', COL_I)}", 34)
        j_res = math(f"<i>T</i> ĵ = {span('(1, 1)', COL_J)}", 34)
        res = VGroup(i_res, j_res).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        res_bg = BackgroundRectangle(res, color=BG, fill_opacity=0.9, buff=0.2)
        resg = VGroup(res_bg, res).next_to(panel, DOWN, buff=0.3, aligned_edge=RIGHT)

        with self.voice(N["w7"]):
            self.play(GrowArrow(i_hat), FadeIn(i_lab), GrowArrow(j_hat), FadeIn(j_lab))
            self.wait(0.5)
            self.play(ApplyMatrix(Tm, plane, about_point=O),
                      Transform(i_hat, i_new), Transform(j_hat, j_new),
                      i_lab.animate.next_to(i_new, DOWN, buff=0.1),
                      j_lab.animate.next_to(j_new.get_end(), UL, buff=0.1),
                      run_time=3)
            self.add(panel_bg, Tl, head_bg, head)
            self.play(FadeIn(resg))

        # tip-to-tail: 1·(2,0) + 2·(1,1)
        s1 = Arrow(O, O + U * np.array([2, 0, 0]), buff=0, color=COL_I, stroke_width=5,
                   max_tip_length_to_length_ratio=0.15)
        s2 = Arrow(O + U * np.array([2, 0, 0]), O + U * np.array([3, 1, 0]), buff=0, color=COL_J,
                   stroke_width=5, max_tip_length_to_length_ratio=0.25)
        s3 = Arrow(O + U * np.array([3, 1, 0]), O + U * np.array([4, 2, 0]), buff=0, color=COL_J,
                   stroke_width=5, max_tip_length_to_length_ratio=0.25)
        v_new = arrow([4, 2], COL_V)
        v_old = DashedLine(O, O + U * np.array([1, 2, 0]), color=COL_V, stroke_width=3)
        v_old_lab = math("(1, 2) before", 28, COL_V).next_to(v_old.get_end(), LEFT, buff=0.15)
        eq = math(f"<i>T</i>(1, 2) = 1·{span('(2, 0)', COL_I)} + 2·{span('(1, 1)', COL_J)} = "
                  f"{span('(4, 2)', COL_V)}", 34)
        eq_bg = BackgroundRectangle(eq, color=BG, fill_opacity=0.9, buff=0.2)
        eqg = VGroup(eq_bg, eq).to_edge(DOWN, buff=0.35).shift(RIGHT * 2)
        dot = Dot(O + U * np.array([4, 2, 0]), color=COL_V)

        with self.voice(N["w8"], pause=0.6):
            self.play(Create(v_old), FadeIn(v_old_lab))
            self.play(FadeOut(VGroup(i_hat, j_hat, i_lab, j_lab)))
            self.play(GrowArrow(s1))
            self.play(GrowArrow(s2))
            self.play(GrowArrow(s3))
            self.play(GrowArrow(v_new), FadeIn(dot), FadeIn(eqg))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 4. Addition
# ============================================================================
class Addition(NarratedScene):
    def construct(self):
        head = title_bar("Matrix addition")
        self.play(FadeIn(head))

        kw = dict(font_size=50, col_gap=0.6)
        A = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A, **kw)
        B = Mat([[2, 3, 1], [5, 2, 0]], color=COL_B, **kw)
        S = Mat([[5, 8, 3], [9, 3, 6]], color=COL_SUM, **kw)
        plus = math("+", 56)
        eq = math("=", 56)
        row = VGroup(A, plus, B, eq, S).arrange(RIGHT, buff=0.45).shift(UP * 0.4)
        la = prose("A  (January)", 26, COL_A).next_to(A, DOWN, buff=0.35)
        lb = prose("B  (February)", 26, COL_B).next_to(B, DOWN, buff=0.35)
        ls = prose("A + B  (total)", 26).next_to(S, DOWN, buff=0.35)

        with self.voice(N["a1"]):
            self.play(FadeIn(A), FadeIn(la))
            self.play(Write(plus), FadeIn(B, shift=LEFT * 0.3), FadeIn(lb))

        work = math("", 40).to_edge(DOWN, buff=0.8)

        def add_entry(i, j, show_work=True, rt=1.2):
            a, b = A.entry(i, j), B.entry(i, j)
            anims = [Indicate(a, color=WHITE), Indicate(b, color=WHITE)]
            self.play(*anims, run_time=0.6)
            self.play(TransformFromCopy(VGroup(a, b), S.entry(i, j)), run_time=rt)

        with self.voice(N["a2"]):
            self.play(Write(eq), Create(S.brackets), FadeIn(ls))
            w1 = math(f"{span('3', COL_A)} + {span('2', COL_B)} = 5", 40).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(w1))
            add_entry(0, 0)
            w2 = math(f"{span('5', COL_A)} + {span('3', COL_B)} = 8", 40).move_to(w1)
            self.play(FadeTransform(w1, w2))
            add_entry(0, 1)
            self.play(FadeOut(w2))
            rest = [(0, 2), (1, 0), (1, 1), (1, 2)]
            self.play(LaggedStart(*[TransformFromCopy(VGroup(A.entry(i, j), B.entry(i, j)),
                                                      S.entry(i, j)) for i, j in rest],
                                  lag_ratio=0.4), run_time=2.5)

        rule = math(f"(<i>A</i> + <i>B</i>)<sub><i>ij</i></sub>  =  "
                    f"{span('<i>a</i><sub><i>ij</i></sub>', COL_A)} + "
                    f"{span('<i>b</i><sub><i>ij</i></sub>', COL_B)}", 44).to_edge(DOWN, buff=0.8)
        box = SurroundingRectangle(rule, color=GREY, buff=0.2, corner_radius=0.1)
        with self.voice(N["a3"]):
            self.play(Indicate(S, color=WHITE, scale_factor=1.05))
            self.play(Write(rule), Create(box))

        # undefined case
        self.play(FadeOut(VGroup(A, B, S, plus, eq, la, lb, ls, rule, box)))
        A2 = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A, **kw)
        C2 = Mat([[1, 2], [3, 4]], color=COL_B, **kw)
        bad = VGroup(A2, math("+", 56), C2, math("=  ?", 56)).arrange(RIGHT, buff=0.45).shift(UP * 0.4)
        d1 = math("2 × 3", 34, COL_DIM).next_to(A2, DOWN, buff=0.35)
        d2 = math("2 × 2", 34, COL_DIM).next_to(C2, DOWN, buff=0.35)
        orphan = A2.col_box(2, color=RED)
        q = prose("no partner!", 26, RED).next_to(orphan, UP, buff=0.2)
        msg = prose("Undefined — matrices must have the same dimensions", 30, RED).to_edge(DOWN, buff=0.8)
        with self.voice(N["a4"], pause=0.6):
            self.play(FadeIn(bad), FadeIn(d1), FadeIn(d2))
            self.play(Create(orphan), FadeIn(q))
            self.play(Write(msg))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 5. Scalar multiplication
# ============================================================================
class ScalarMultiplication(NarratedScene):
    def construct(self):
        head = title_bar("Scalar multiplication")
        self.play(FadeIn(head))
        kw = dict(font_size=50, col_gap=0.6)
        c = math("2", 60, COL_SCALAR)
        dot = math("·", 56)
        A = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A, **kw)
        eq = math("=", 56)
        R = Mat([[6, 10, 4], [8, 2, 12]], **kw)
        row = VGroup(c, dot, A, eq, R).arrange(RIGHT, buff=0.35).shift(UP * 0.4)
        lab = prose("scalar = a single number", 26, COL_SCALAR).next_to(c, DOWN, buff=0.9)
        arr = Arrow(lab.get_top(), c.get_bottom(), buff=0.1, color=COL_SCALAR, stroke_width=3)

        with self.voice(N["s1"]):
            self.play(FadeIn(A))
            self.play(FadeIn(c, scale=1.5), FadeIn(dot))
            self.play(FadeIn(lab), GrowArrow(arr))

        with self.voice(N["s2"]):
            self.play(FadeOut(lab), FadeOut(arr), Write(eq), Create(R.brackets))
            w1 = math(f"{span('2', COL_SCALAR)} × {span('3', COL_A)} = 6", 40).to_edge(DOWN, buff=0.8)
            self.play(FadeIn(w1), Indicate(A.entry(0, 0), color=WHITE))
            self.play(TransformFromCopy(VGroup(c, A.entry(0, 0)), R.entry(0, 0)))
            w2 = math(f"{span('2', COL_SCALAR)} × {span('5', COL_A)} = 10", 40).move_to(w1)
            self.play(FadeTransform(w1, w2), Indicate(A.entry(0, 1), color=WHITE))
            self.play(TransformFromCopy(VGroup(c, A.entry(0, 1)), R.entry(0, 1)))
            self.play(FadeOut(w2))
            rest = [(0, 2), (1, 0), (1, 1), (1, 2)]
            self.play(LaggedStart(*[TransformFromCopy(VGroup(c, A.entry(i, j)), R.entry(i, j))
                                    for i, j in rest], lag_ratio=0.4), run_time=2.2)
            rule = math(f"({span('<i>c</i>', COL_SCALAR)}<i>A</i>)<sub><i>ij</i></sub>  =  "
                        f"{span('<i>c</i>', COL_SCALAR)} · {span('<i>a</i><sub><i>ij</i></sub>', COL_A)}",
                        44).to_edge(DOWN, buff=0.8)
            box = SurroundingRectangle(rule, color=GREY, buff=0.2, corner_radius=0.1)
            self.play(Write(rule), Create(box))

        # geometric picture
        self.play(FadeOut(VGroup(c, dot, A, eq, R, rule, box)))
        ax = NumberPlane(x_range=[-3, 4, 1], y_range=[-3, 5, 1], x_length=5.6, y_length=6.4,
                         background_line_style={"stroke_color": "#2E5C73", "stroke_width": 1.2},
                         axis_config={"stroke_color": GREY})
        ax.to_edge(DOWN, buff=0.25).to_edge(LEFT, buff=0.8)
        o = ax.c2p(0, 0)
        v = Arrow(o, ax.c2p(1, 2), buff=0, color=COL_V, stroke_width=7,
                  max_tip_length_to_length_ratio=0.25)
        v2 = Arrow(o, ax.c2p(2, 4), buff=0, color=COL_SCALAR, stroke_width=5,
                   max_tip_length_to_length_ratio=0.12)
        vn = Arrow(o, ax.c2p(-1, -2), buff=0, color=RED, stroke_width=5,
                   max_tip_length_to_length_ratio=0.25)
        t1 = math(f"{span('<b>v</b>', COL_V)} = (1, 2)", 36)
        t2 = math(f"{span('2', COL_SCALAR)}{span('<b>v</b>', COL_V)} = (2, 4) :  twice as long, same direction", 32)
        t3 = math(f"{span('−1', RED)}{span('<b>v</b>', COL_V)} = (−1, −2) :  flipped around", 32)
        txt = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.5)
        max_w = config.frame_width / 2 - txt.get_left()[0] - 0.4
        if txt.width > max_w:
            txt.scale_to_fit_width(max_w).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.5)
        with self.voice(N["s3"], pause=0.6):
            self.play(Create(ax), run_time=1.2)
            self.play(GrowArrow(v), FadeIn(t1))
            self.play(GrowArrow(v2), FadeIn(t2), run_time=1.5)
            self.bring_to_front(v)
            self.play(GrowArrow(vn), FadeIn(t3), run_time=1.5)
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 6. Matrix × vector
# ============================================================================
class MatrixVector(NarratedScene):
    def construct(self):
        head = title_bar("Matrix multiplication")
        self.play(FadeIn(head))
        kw = dict(font_size=50, col_gap=0.7, row_gap=0.4)
        A = Mat([[3, 5, 2], [4, 1, 6]], color=COL_A, **kw)
        p = Mat([[10], [20], [5]], color=COL_PRICE, **kw)
        R = Mat([[140], [90]], **kw)
        eq = math("=", 56)
        prod = VGroup(A, p, eq, R).arrange(RIGHT, buff=0.4).shift(UP * 0.55 + LEFT * 0.8)
        la = math(f"{span('<i>A</i>', COL_A)}  (quantities)", 28).next_to(A, DOWN, buff=0.35)
        lp = math(f"{span('<b>p</b>', COL_PRICE)}  (prices, ₹)", 28).next_to(p, DOWN, buff=0.35)
        price_tags = VGroup(*[prose(t, 22, GREY).next_to(p.entry(i, 0), RIGHT, buff=0.45)
                              for i, t in enumerate(["pen", "notebook", "eraser"])])
        price_tags.next_to(p, RIGHT, buff=0.25)

        with self.voice(N["m1"]):
            self.play(FadeIn(A), FadeIn(la))
            self.wait(1)
            self.play(FadeIn(p, shift=LEFT * 0.3), FadeIn(lp), FadeIn(price_tags))

        # Move tags out of the way of "= R"
        self.play(FadeOut(price_tags), Write(eq), Create(R.brackets))

        def dot_row(i, terms, prods, total, voice_key):
            rb = A.row_box(i)
            cb = p.col_box(0)
            line1 = math(" + ".join(f"{span(a, COL_A)}×{span(b, COL_PRICE)}" for a, b in terms), 40)
            line2 = math(" + ".join(prods) + f" = {total}", 40)
            work = VGroup(line1, line2).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.55)
            with self.voice(N[voice_key]):
                self.play(Create(rb), Create(cb))
                for j in range(3):
                    pair = VGroup(A.entry(i, j), p.entry(j, 0))
                    link = Line(A.entry(i, j).get_center(), p.entry(j, 0).get_center(),
                                color=WHITE, stroke_width=2, stroke_opacity=0.6)
                    self.play(Indicate(pair, color=WHITE), Create(link), run_time=0.8)
                    self.play(FadeOut(link), run_time=0.3)
                self.play(FadeIn(line1))
                self.play(FadeIn(line2))
                self.play(TransformFromCopy(line2[-len(str(total)):], R.entry(i, 0)))
            return VGroup(rb, cb, work)

        g1 = dot_row(0, [("3", "10"), ("5", "20"), ("2", "5")], ["30", "100", "10"], 140, "m2")

        dp = prose("row · column  =  dot product", 30, COL_ROW).next_to(head, DOWN, buff=0.3)
        with self.voice(N["m3"]):
            self.play(Indicate(g1[0], color=COL_ROW), Indicate(g1[1], color=COL_COL))
            self.play(Write(dp))
        self.play(FadeOut(g1))

        g2 = dot_row(1, [("4", "10"), ("1", "20"), ("6", "5")], ["40", "20", "30"], 90, "m4")

        rule = math(f"(<i>AB</i>)<sub><i>ij</i></sub> = ({span('row <i>i</i>', COL_ROW)} of <i>A</i>) · "
                    f"({span('column <i>j</i>', COL_COL)} of <i>B</i>)", 40).to_edge(DOWN, buff=0.7)
        box = SurroundingRectangle(rule, color=GREY, buff=0.2, corner_radius=0.1)
        lr = prose("revenue of each shop (₹)", 24, GREY).next_to(R, RIGHT, buff=0.3)
        with self.voice(N["m5"]):
            self.play(FadeOut(g2), FadeIn(lr), Indicate(R, color=WHITE, scale_factor=1.08))
            self.play(Write(rule), Create(box))

        # dimension rule
        dA = math(f"2 × {span('3', COL_DIM)}", 34).next_to(A, DOWN, buff=0.35)
        dP = math(f"{span('3', COL_DIM)} × 1", 34).next_to(p, DOWN, buff=0.35)
        dR = math("2 × 1", 34).next_to(R, DOWN, buff=0.35)
        base_y = p.get_bottom()[1] - 0.4
        for d in (dA, dP, dR):
            d.set_y(base_y)
        inner = CurvedArrow(dA[-1].get_bottom() + DOWN * 0.05, dP[0].get_bottom() + DOWN * 0.05,
                            angle=PI / 1.6, color=COL_DIM, stroke_width=3)
        inner_l = prose("must match", 24, COL_DIM).next_to(inner, DOWN, buff=0.1)
        gen = math(f"(<i>m</i> × {span('<i>n</i>', COL_DIM)}) · ({span('<i>n</i>', COL_DIM)} × <i>k</i>)"
                   f"  →  <i>m</i> × <i>k</i>", 44).to_edge(DOWN, buff=0.7)
        gbox = SurroundingRectangle(gen, color=GREY, buff=0.2, corner_radius=0.1)
        with self.voice(N["m6"], pause=0.6):
            self.play(FadeOut(la), FadeOut(lp), FadeOut(rule), FadeOut(box), FadeOut(dp))
            self.play(FadeIn(dA), FadeIn(dP))
            self.play(Create(inner), FadeIn(inner_l))
            self.wait(2.5)
            self.play(FadeIn(dR))
            self.play(Write(gen), Create(gbox))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 7. Matrix × matrix, non-commutativity
# ============================================================================
class MatrixMatrix(NarratedScene):
    def construct(self):
        head = title_bar("Multiplying two matrices")
        self.play(FadeIn(head))
        kw = dict(font_size=52, col_gap=0.7, row_gap=0.4)
        P = Mat([[2, 0], [1, 3]], color=COL_P, **kw)
        Q = Mat([[1, 4], [2, -1]], color=COL_Q, **kw)
        R = Mat([[2, 8], [7, 1]], **kw)
        lP = math("<i>P</i>", 48, COL_P)
        lQ = math("<i>Q</i>", 48, COL_Q)
        eq = math("=", 56)
        prod = VGroup(P, Q, eq, R).arrange(RIGHT, buff=0.45).shift(UP * 0.4)
        lP.next_to(P, DOWN, buff=0.3)
        lQ.next_to(Q, DOWN, buff=0.3)
        lR = math(f"{span('<i>P</i>', COL_P)}{span('<i>Q</i>', COL_Q)}", 48).next_to(R, DOWN, buff=0.3)

        self.play(FadeIn(P), FadeIn(Q), FadeIn(lP), FadeIn(lQ), Write(eq), Create(R.brackets))

        work = None

        def entry(i, j, text, key):
            nonlocal work
            rb = P.row_box(i)
            cb = Q.col_box(j)
            target = R.entry_box(i, j, color=WHITE)
            w = math(text, 42).to_edge(DOWN, buff=0.8)
            with self.voice(N[key]):
                anims = [Create(rb), Create(cb), Create(target)]
                if work is not None:
                    anims.append(FadeOut(work))
                self.play(*anims)
                self.play(FadeIn(w))
                self.play(TransformFromCopy(w[-1:] if len(R.entry(i, j).text) == 1 else w[-2:],
                                            R.entry(i, j)))
                self.wait(0.3)
                self.play(FadeOut(VGroup(rb, cb, target)))
            work = w

        def t(a, b, c, d, res):
            return (f"{span(a, COL_P)}·{span(b, COL_Q)} + {span(c, COL_P)}·{span(d, COL_Q)} = {res}")

        entry(0, 0, t("2", "1", "0", "2", "2"), "m7")
        entry(0, 1, t("2", "4", "0", "(−1)", "8"), "m8a")
        entry(1, 0, t("1", "1", "3", "2", "7"), "m8b")
        entry(1, 1, t("1", "4", "3", "(−1)", "1"), "m8c")

        # Swap order
        top = VGroup(P, Q, eq, R, lP, lQ)
        Q2 = Mat([[1, 4], [2, -1]], color=COL_Q, font_size=44, col_gap=0.6, row_gap=0.35)
        P2 = Mat([[2, 0], [1, 3]], color=COL_P, font_size=44, col_gap=0.6, row_gap=0.35)
        R2 = Mat([[6, 12], [3, -3]], font_size=44, col_gap=0.6, row_gap=0.35)
        eq2 = math("=", 50)
        bottom = VGroup(Q2, P2, eq2, R2).arrange(RIGHT, buff=0.4)
        lQP = math(f"{span('<i>Q</i>', COL_Q)}{span('<i>P</i>', COL_P)}", 44).next_to(R2, DOWN, buff=0.25)
        neq = math(f"{span('<i>P</i>', COL_P)}{span('<i>Q</i>', COL_Q)}  ≠  "
                   f"{span('<i>Q</i>', COL_Q)}{span('<i>P</i>', COL_P)}", 54, RED)
        res = prose("In general  AB ≠ BA  — matrix multiplication is not commutative",
                    30, RED).to_edge(DOWN, buff=0.45)
        with self.voice(N["m9"]):
            self.play(FadeOut(work), FadeOut(lP), FadeOut(lQ))
            self.play(VGroup(P, Q, eq, R).animate.scale(0.85).move_to(UP * 1.6 + LEFT * 1.3))
            lR.scale(0.9).next_to(R, RIGHT, buff=0.35)
            self.play(FadeIn(lR))
            bottom.move_to(DOWN * 0.9 + LEFT * 1.3)
            lQP.next_to(R2, RIGHT, buff=0.35)
            self.play(FadeIn(bottom), FadeIn(lQP))
            neq.to_edge(RIGHT, buff=0.7).set_y((R.get_center()[1] + R2.get_center()[1]) / 2)
            self.play(FadeIn(neq, scale=1.5))
            self.play(Write(res))

        x_chain = math(f"<b>x</b>  ──{span('<i>Q</i>', COL_Q)}──▶  {span('<i>Q</i>', COL_Q)}<b>x</b>"
                       f"  ──{span('<i>P</i>', COL_P)}──▶  {span('<i>P</i>', COL_P)}({span('<i>Q</i>', COL_Q)}<b>x</b>)"
                       f"  =  ({span('<i>P</i>', COL_P)}{span('<i>Q</i>', COL_Q)})<b>x</b>", 40)
        sub = prose("Q acts first, then P   (socks, then shoes!)", 28, GREY)
        why = VGroup(x_chain, sub).arrange(DOWN, buff=0.4).move_to(DOWN * 0.3)
        with self.voice(N["m10"], pause=0.6):
            self.play(FadeOut(VGroup(P, Q, eq, R, lR, bottom, lQP, neq)))
            self.play(res.animate.next_to(head, DOWN, buff=0.4))
            self.play(Write(x_chain), run_time=2.5)
            self.play(FadeIn(sub))
        self.play(FadeOut(Group(*self.mobjects)))


# ============================================================================
# 8. Summary + closing frame
# ============================================================================
class Summary(NarratedScene):
    def construct(self):
        head = title_bar("Summary")

        def item(markup):
            dot = Dot(color=COL_SCALAR, radius=0.07)
            t = math(markup, 34)
            return VGroup(dot, t).arrange(RIGHT, buff=0.3)

        b1 = item(f"Matrix: rectangular array, size {span('<i>m</i>', COL_ROW)} × "
                  f"{span('<i>n</i>', COL_COL)} (rows × columns); "
                  f"<i>a</i><sub><i>ij</i></sub> = row <i>i</i>, column <i>j</i>")
        b2 = item(f"Addition: {span('(<i>A</i> + <i>B</i>)<sub><i>ij</i></sub> = <i>a</i><sub><i>ij</i></sub> + <i>b</i><sub><i>ij</i></sub>', COL_B)}"
                  "  — same size only")
        b3 = item(f"Scalar multiple: {span('(<i>cA</i>)<sub><i>ij</i></sub> = <i>c</i> · <i>a</i><sub><i>ij</i></sub>', COL_SCALAR)}"
                  "  — every entry scaled")
        b4 = item(f"Product: {span('(<i>AB</i>)<sub><i>ij</i></sub> = row <i>i</i> of <i>A</i> · column <i>j</i> of <i>B</i>', COL_PRICE)}")
        b5 = item(f"({span('<i>m</i>×<i>n</i>', COL_DIM)})({span('<i>n</i>×<i>k</i>', COL_DIM)}) → "
                  f"<i>m</i>×<i>k</i>   and   <i>AB</i> ≠ <i>BA</i> in general")
        bullets = VGroup(b1, b2, b3, b4, b5).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets.next_to(head, DOWN, buff=0.6)
        if bullets.width > config.frame_width - 1:
            bullets.scale_to_fit_width(config.frame_width - 1)
        bullets.set_x(0)

        with self.voice(N["z1"]):
            self.play(FadeIn(head))
        with self.voice(N["z2"]):
            self.play(FadeIn(b1, shift=RIGHT * 0.3))
        with self.voice(N["z3"]):
            self.play(FadeIn(b2, shift=RIGHT * 0.3))
        with self.voice(N["z4"]):
            self.play(FadeIn(b3, shift=RIGHT * 0.3))
        with self.voice(N["z5"]):
            self.play(FadeIn(b4, shift=RIGHT * 0.3))
            self.play(FadeIn(b5, shift=RIGHT * 0.3))
        with self.voice(N["z6"], pause=1.0):
            pass
        self.play(FadeOut(Group(*self.mobjects)))

        # ---- Closing frame: credits & AI disclosure
        ct = prose("Credits", 44, weight=BOLD)
        lines = VGroup(
            prose(f"Created by {STUDENT_NAME}  (ID: {STUDENT_ID})", 28, COL_SCALAR),
            prose("Animation: Manim Community v0.22 (Python) — source code in the Code/ folder", 24),
            prose(f"Narration: voiced by {STUDENT_NAME}" if using_own_voice() else
                  "Narration: synthetic voice, macOS text-to-speech (\"Samantha\")", 24),
            prose("Music: none", 24),
            prose("AI disclosure: script, storyboard and Manim code drafted with Claude (Anthropic);", 24, GREY),
            prose("every calculation verified independently (Code/verify_math.py)", 24, GREY),
        ).arrange(DOWN, buff=0.28)
        credits = VGroup(ct, lines).arrange(DOWN, buff=0.55)
        self.play(FadeIn(credits, shift=UP * 0.2))
        self.wait(5)
        self.play(FadeOut(credits))
