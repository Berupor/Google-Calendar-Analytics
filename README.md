# Google Calendar Analytics

![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/Logo.png?raw=true)
This Python program allows you to perform analytics on your Google Calendar events. With this program, you can visualize
the total duration of your events, compare the length of events across different time periods, and gain insights into
which events take up the most time.

## Features

- Extract events from your Google Calendar
- Compute the total duration of events in a specified time range
- Visualize the duration of events in a pie chart and a bar chart
- Limit the number of events displayed in the charts
- Save the charts as PNG images

## Installation

1. You can install the dependencies for this program by running the following command:

```console
pip install -r requirements.txt
```

2. Configure `.env` file by example

### Setup

You will need to create a Google API key to be able to access your Google Calendar data. The instructions for doing this
can be found in the [Google API documentation](https://developers.google.com/calendar/api/guides/quickstart/python).

Once you have obtained your API key, you will need to save it as a JSON file and place it in the `src/authentication/`
directory of the program. The file should be renamed to `credentials.json`

## Usage

To run the program, simply run the following command:

```console
python main.py
```

The program will prompt you for the start and end dates for the time range you would like to analyze. After entering the
dates, the program will compute the total duration of your events and generate pie charts and bar charts that visualize
the duration of your events.

## Contribution
If you would like to contribute to this project, please feel free to submit a pull request. Some areas where contributions are particularly welcome include:

- Adding new features
- Improving existing features
- Debugging and fixing bugs
- Adding tests to ensure the program is working as expected

## Weekly analytics example:

|           Pie plot            |           Bar plot            |
|:-----------------------------:|:-----------------------------:|
| ![img](examples/pie_plot.png) | ![img](examples/bar_plot.png) |

|           Line plot            |                        
|:------------------------------:|
| ![img](examples/line_plot.png) | 
 
