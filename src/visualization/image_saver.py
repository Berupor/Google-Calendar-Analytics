class ImageSaver:
    def __init__(self, route, dpi):
        self.SAVING_ROUTE = route
        self.DPI = dpi

    def save_plot(self, plot, filename):
        plot.savefig(f"{self.SAVING_ROUTE}/{filename}.png", dpi=self.DPI)
