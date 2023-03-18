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
