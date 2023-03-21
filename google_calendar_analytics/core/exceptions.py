from dataclasses import dataclass


@dataclass
class NotEnoughDataError(ValueError):
    expected_data_points: int
    available_data_points: int

    def __str__(self):
        return (
            f"\n\nThere is not enough data to perform the analysis.\n"
            f"Expected {self.expected_data_points} data points, but only {self.available_data_points} are available. \n"
            f"This often occurs when the time range is too short to provide sufficient data for the analysis. \n\n"
            f"To resolve the issue, you can try increasing the time range or decreasing the number of periods. \n"
            f"Alternatively, you can consider using a different analysis method that requires less data."
        )


@dataclass
class InvalidPlotTypeError(ValueError):
    plot_type: str
    method: str = None

    def __str__(self):
        options = {
            "analyze_one": ("Line", ),
            "analyze_many": ("Bar", "Pie"),
            "analyze_one_with_periods": ("MultyLine", )
        }

        if self.method is None or self.method not in options:
            options_str = ", ".join([f"'{opt}'" for opt in options.values()])
        else:
            options_str = ", ".join([f"'{opt}'" for opt in options[self.method]])

        return (
            f"\n\nThe plot type '{self.plot_type}' is invalid for '{self.method}'. \n"
            f"Please choose from the following options: {options_str}. \n\n"
        )
