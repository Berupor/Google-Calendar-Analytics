from dataclasses import dataclass

pastel_palette = (
    "rgb(102, 197, 204)",
    "rgb(246, 207, 113)",
    "rgb(248, 156, 116)",
    "rgb(220, 176, 242)",
    "rgb(135, 197, 95)",
    "rgb(158, 185, 243)",
    "rgb(254, 136, 177)",
    "rgb(201, 219, 116)",
    "rgb(139, 224, 164)",
    "rgb(180, 151, 231)",
    "rgb(179, 179, 179)",
)


@dataclass
class VisualDesign:
    """
    A class that represents the visual design of the plots.
    """

    grid_color: str = None  # type: ignore
    font_color: str = None  # type: ignore
    rgb_colors: tuple = pastel_palette

    rgb_line_color: str = "rgb(255, 0, 0)"
    line_shape: str = "linear"

    grid_width: float = 0.1
    transparency: float = 1.0
    line_width: float = 2.0

    width: int = 800
    height: int = 400

    dark_theme: bool = False
    show_grid: bool = True
    show_title: bool = True
    show_legend: bool = True
    show_xaxis_title: bool = True
    show_yaxis_title: bool = True

    def __post_init__(self):
        """
        Check if the line_shape parameter is a valid line shape.
        """
        valid_shapes = ("linear", "spline", "hv", "vh", "hvh", "vhv")
        if self.line_shape not in valid_shapes:
            raise ValueError(
                f"Invalid line_shape: {self.line_shape}. Valid options are: {valid_shapes}"
            )


base_plot_design = VisualDesign()
