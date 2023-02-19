class ImageSaver:
    def __init__(self, route):
        self.SAVING_ROUTE = route
        self.RESOLUTION = {"width": 1200, "height": 600, "scale": 4}

    def save_plot(self, plot, filename):
        plot.write_image(f"{self.SAVING_ROUTE}/{filename}.png", **self.RESOLUTION)
