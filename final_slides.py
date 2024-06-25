from manim import *
from manim_slides import Slide
import numpy as np

class TeachingDemo(Slide):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Font sizes
        self.TITLE_FONT_SIZE = 48
        self.CONTENT_FONT_SIZE = 0.7 * self.TITLE_FONT_SIZE
        self.SUBTITLE_FONT_SIZE = 0.5 * self.TITLE_FONT_SIZE

        Dot.set_default(color=BLACK)
        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Axes.set_default(axis_config={"color": BLACK,
                                        "include_numbers": True})

    def construct(self):
         self.construct_title()
         self.construct_objectives()
         self.construct_intro_to_limits()
         self.construct_conceptualizing_limits()

    def construct_title(self):

        # Empty first Frame
        d = Dot(color=config.background_color).center()
        self.play(Create(d))
        self.next_slide()

        # Main Title Frame
        main_title1 = Text("Intuitive Notion", font_size=self.TITLE_FONT_SIZE)
        main_title2 = Text("of Limits")
        name = Text("by: Cristian B. Jetomo", font_size=self.SUBTITLE_FONT_SIZE)
        self.main_title = VGroup(main_title1, main_title2, name).arrange(DOWN, buff=0.5).center()

        self.play(Write(self.main_title), run_time=2)
        self.next_slide()

    def construct_objectives(self):
        # Learning Objectives
        # (1) header
        header_obj = Text("Learning Objectives", font_size=self.TITLE_FONT_SIZE).to_corner(UL)
        self.wipe(self.main_title, header_obj)
        self.next_slide()

        # (2) objectives
        obj1 = Text("At the end of this module, the students should be able to: ",
                    font_size=self.CONTENT_FONT_SIZE).align_to(header_obj, LEFT).shift(1.5*UP)
        obj2 = paragraph("1. understand limits in relation to Calculus; and",
                        "2. explain the concept of limits graphically and analytically.",
                        font_size=self.CONTENT_FONT_SIZE)
        obj2.next_to(obj1, DOWN).shift(1 * RIGHT)
        objs = VGroup(obj1, obj2)
        self.objectives = VGroup(header_obj, objs)
        self.play(Write(objs), run_time=0.5)
        self.next_slide()

    def construct_intro_to_limits(self):
        # Introduction to Calculus and Limits
        # (1) Title
        title1 = Text("Introduction to Calculus", font_size=self.TITLE_FONT_SIZE)
        title2 = Text("and Limits", font_size=self.TITLE_FONT_SIZE)
        self.subtitle1 = VGroup(title1, title2).arrange(DOWN, buff=0.5).center()
        
        self.wipe(self.objectives, self.subtitle1)
        self.next_slide()

        # --- Visualization
        # (2.1) Calculus
        calc_text = Text("Calculus").scale(0.75).to_edge(LEFT, buff=1)
        calc_box = SurroundingRectangle(calc_text, color=ManimColor("#89b6af"), fill_opacity=0.75, corner_radius=0.1, buff=0.3) 
        self.calculus = VGroup(calc_box, calc_text)

        self.wipe(self.subtitle1, self.calculus)
        self.next_slide()
        
        # (2.2) Differential and Integral
        diff_text = Text("Differential").scale(0.75).center().shift(2.5*UP)
        diff_box = SurroundingRectangle(diff_text, color=ManimColor("#56bbca"), fill_opacity=0.75, corner_radius=0.1, buff=0.3)
        diff_arrow = Arrow(start=calc_box.get_right(), end=diff_box.get_left(), color=ManimColor("#000000"))
        self.differential = VGroup(diff_box, diff_text)

        integ_text = Text("Integral").scale(0.75).center().shift(2.5*DOWN)
        integ_box = SurroundingRectangle(integ_text, color=ManimColor("#56bbca"), fill_opacity=0.75, corner_radius=0.1, buff=0.3)
        integ_arrow = Arrow(start=calc_box.get_right(), end=integ_box.get_left(), color=ManimColor("#000000"))
        self.integral = VGroup(integ_box, integ_text)

        self.arrows = VGroup(diff_arrow, integ_arrow)
        self.play(Create(self.arrows))
        self.play(GrowFromEdge(self.differential, LEFT), GrowFromEdge(self.integral, LEFT))
        self.next_slide()

        # (3) Visualizing Derivatives
        self.visualizing_derivatives()
        
        # (4) Visualizing Integrals
        self.visualizing_integrals()

        # grouping Mobjects for wipe
        self.intro_limits_group = VGroup(self.calculus, self.differential, self.integral, self.arrows, self.deriv_group, self.integ_group)
                      
    def visualizing_derivatives(self):
        box = RoundedRectangle(corner_radius=0, color=BLACK, fill_opacity=0, height=3).move_to(self.differential.get_center() + 4.5 * RIGHT + 0.5*DOWN)
        ax = Axes(color=BLACK, x_length=box.get_right()[0]-box.get_left()[0], y_length=box.get_top()[1]-box.get_bottom()[1], tips=False,
                            axis_config={"color": BLACK}).move_to(box.get_center())

        k = ValueTracker(-3/2*np.pi)
        function = ax.plot(lambda x: np.sin(x), x_range=[-6,6,1], color=BLUE)
        moving_slope = always_redraw(
            lambda: ax.get_secant_slope_group(
                x = k.get_value(),
                graph = function,
                dx = 0.05,
                secant_line_length=1.5,
                secant_line_color=RED
            )
        )
        moving_dot = always_redraw(
            lambda: Dot(color=BLACK).move_to(
                ax.c2p(k.get_value(), function.underlying_function(k.get_value()))
            )
        )
        self.play(Create(box), Create(ax), Create(function))
        self.play(Create(moving_slope), Create(moving_dot))
        self.play(k.animate.set_value(3/2*np.pi), run_time=5, rate_func=linear)
        self.next_slide()

        self.deriv_group = VGroup(box, ax, function, moving_slope, moving_dot)

    def visualizing_integrals(self):
        box = RoundedRectangle(corner_radius=0, color=BLACK, fill_opacity=0, height=3).move_to(self.integral.get_center() + 4.5 * RIGHT + 0.5*UP)
        ax = Axes(color=BLACK, x_range=(-1, 12, 1), y_range=(-1, 3, 1),
                    x_length=box.get_right()[0]-box.get_left()[0], y_length=box.get_top()[1]-box.get_bottom()[1], tips=False,
                    axis_config={"color": BLACK}).move_to(box.get_center())

        function = ax.plot(lambda x: 0.7*np.sqrt(x), x_range=[0,12,0.05], color=BLACK)
        rectangles = VGroup(*[
                    ax.get_riemann_rectangles(
                        function,
                        x_range=[1,11],
                        dx=dx,
                        input_sample_type='left',
                        stroke_width=dx if dx > 0.1 else 0.8
                    ).set_color_by_gradient(BLUE, GREEN).set_stroke(color=BLACK if dx > 0.1 else None)
                    for dx in [1/(i) for i in range(1,10)]
        ])
        r = rectangles[0]

        self.play(Create(box), Create(ax), Create(function), Create(r))
        for rect in rectangles[1:]:
            self.play(Transform(r, rect))
            self.wait(0.3)
        self.next_slide()

        self.integ_group = VGroup(box, ax, function, rectangles)

    def construct_conceptualizing_limits(self):
        # Conceptualizing Limits
        # (1) Title
        self.subtitle2 = Text("Conceptualizing Limits", font_size=self.TITLE_FONT_SIZE).center()
        
        self.wipe(self.intro_limits_group, self.subtitle2)
        self.next_slide()

        # (2.1) Graphical Approach Title
        self.header_graphical = Text("Graphical Approach", font_size=self.CONTENT_FONT_SIZE).to_corner(UL)
        ul = Underline(self.header_graphical, color=BLACK)
        self.header_graphical = VGroup(self.header_graphical, ul)
        self.wipe(self.subtitle2, self.header_graphical)
        self.next_slide()

        t = Text("Consider the function", font_size=self.SUBTITLE_FONT_SIZE)
        eqn1 = MathTex(r"f(x) = \frac{x^3-1}{x-1}, \quad -2 \leq x \leq 2", font_size=1.5*self.SUBTITLE_FONT_SIZE)
        texts = VGroup(t, eqn1).align_to(self.header_graphical, LEFT).arrange(DOWN, buff=0.5).next_to(self.header_graphical, DOWN).shift(DOWN)

        self.play(Write(texts), run_time=0.5)
        self.next_slide()

        # (2.2) Plot
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 6, 1],
                    tips=False).to_edge(RIGHT)
        ax.get_x_axis().numbers.set_color(BLACK)
        ax.get_y_axis().numbers.set_color(BLACK)
        function = ax.plot(lambda x: x**2+x+1, x_range=[-2,2,1], color=WHITE)
        graph1 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[-2, 0.97, 1], color=BLUE)
        graph2 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[1.03, 2, 0.1], color=BLUE)
        break_point = Circle(radius=0.10, color=BLUE).move_to(ax.c2p(1,3))
        func_graph = VGroup(graph1, break_point, graph2)
        self.play(Create(ax), Create(func_graph))
        self.next_slide()

        # (2.3) What happens?
        t2 = Tex(r"What happens to $f(x)$ as \\$x$ approaches 1?",
                    font_size=self.CONTENT_FONT_SIZE).next_to(texts, DOWN).shift(DOWN)
        x_limit = ax.get_x_axis().numbers[3]
        self.play(Write(t2), run_time=0.5)
        self.play(Circumscribe(x_limit, color=RED))
        self.next_slide()

        # (2.4) Moving line and points
        t = ValueTracker(0.1)
        moving_dot = always_redraw(
            lambda: Dot(color=BLACK).move_to(
                ax.c2p(t.get_value(), 0)
            )
        )
        dotted_lines = always_redraw(
            lambda: ax.get_lines_to_point(
                ax.c2p(t.get_value(), function.underlying_function(t.get_value())),
                color=BLACK
            )
        )
        moving_xmark = always_redraw(
            lambda: Cross(color=RED, scale_factor=0.1).move_to(
                ax.c2p(0, function.underlying_function(t.get_value()))
            )
        )
        updating_lines_and_points = VGroup(moving_dot, dotted_lines, moving_xmark)

        self.play(Create(updating_lines_and_points))
        self.next_slide()
        
        # from the left
        self.play(t.animate.set_value(0.5))
        self.wait(0.5)
        self.play(t.animate.set_value(0.95))
        self.next_slide()

        # from the right
        self.play(t.animate.set_value())


def paragraph(*strs, alignment=LEFT, direction=DOWN, **kwargs):
        texts = VGroup(*[Text(s, **kwargs) for s in strs]).arrange(direction)

        if len(strs) > 1:
            for text in texts[1:]:
                text.align_to(texts[0], direction=alignment)

        return texts
