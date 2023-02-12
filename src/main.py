from authentication.auth import CalendarAuth
from data_collecting.collector import CalendarDataCollector
from data_processing.transformer import DataTransformer
from visualization.visualizer import Visualizer

calendar_auth = CalendarAuth(
    "authentication/token.json", "authentication/credentials.json"
)
data_collector = CalendarDataCollector(calendar_auth.get_credentials())
data_transformer = DataTransformer()
data_visualizer = Visualizer()


def main():
    events = data_collector.collect_data(
        range_type="week", calendar_id="zenek.zeka@gmail.com"
    )

    data = data_transformer.get_events_duration(events)

    data_visualizer.plot_pie_chart(data, max_events=5)


if __name__ == "__main__":
    main()
