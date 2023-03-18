You can customize your plot by creating an instance of AnalyzerBuilder with different options,
such as the plot type, transparency, dark theme, and maximum number of events to be analyzed.

```python
from google_calendar_analytics import AnalyzerBuilder

analyzer = (
     AnalyzerBuilder()
    .with_credentials(creds)
    .with_plot_type("Bar")  # Choose a plot type: Bar, Line, MultyLine, or Pie
    .with_transparency(0.5)  # Set the transparency of the chart
    .with_dark_theme(True)  # Enable dark theme for the chart
    .with_max_events(10)  # Set the maximum number of events to be analyzed
    .with_ascending(False)  # Sort the events in descending order of duration
    .build()  # Build the analyzer instance
)
```

## Plot types
You can choose from the following plot types:

### Bar
![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Bar_ploty.png?raw=true) 
### Line
![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Line_ploty.png?raw=true)
### MultyLine
![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Multy.png?raw=true)
### Pie
![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Pie_ploty.png?raw=true)

## Restrictions
Note that not all plot types have the `max_events` variable available. If you want to limit the number
of events to be analyzed, you should use the `Bar`, `Pie` plot type instead of `Line` or `MultyLine`.

Also, you can't use `analyze_many` method with `Line` or `MultyLine` plot types because
these plots are not suitable for multiple events.