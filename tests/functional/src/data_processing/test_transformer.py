import pandas as pd
import pytest

from google_calendar_analytics.processing.transformer import (
    AsyncDataTransformer,
    EventDurationPeriodsStrategy,
    ManyEventsDurationStrategy,
    OneEventDurationStrategy,
)


@pytest.fixture()
def many_events_duration_strategy():
    return ManyEventsDurationStrategy()


@pytest.fixture()
def one_event_duration_strategy():
    return OneEventDurationStrategy()


@pytest.fixture()
def event_duration_periods_strategy():
    return EventDurationPeriodsStrategy()


@pytest.fixture()
def async_data_transformer():
    return AsyncDataTransformer()


@pytest.fixture()
def sample_events():
    return [
        {
            "summary": "Event 1",
            "start": {"dateTime": "2022-03-17T09:00:00+00:00"},
            "end": {"dateTime": "2022-03-17T11:00:00+00:00"},
        },
        {
            "summary": "Event 2",
            "start": {"dateTime": "2022-03-18T09:00:00+00:00"},
            "end": {"dateTime": "2022-03-18T12:00:00+00:00"},
        },
        {
            "summary": "Event 3",
            "start": {"dateTime": "2022-03-19T09:00:00+00:00"},
            "end": {"dateTime": "2022-03-19T13:00:00+00:00"},
        },
    ]


@pytest.mark.asyncio
async def test_many_events_duration_strategy_calculate_duration(
    many_events_duration_strategy, sample_events
):
    result = await many_events_duration_strategy.calculate_duration(
        sample_events, max_events=2
    )
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert all(result.columns == ["Event", "Duration"])
    assert all(result["Duration"].values == [4.0, 3.0])


@pytest.mark.asyncio
async def test_one_event_duration_strategy_calculate_duration(
    one_event_duration_strategy, sample_events
):
    result = await one_event_duration_strategy.calculate_duration(
        sample_events, event_name="Event 2"
    )
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert all(result.columns == ["Date", "Duration"])
    assert all(result["Duration"].values == [3.0])


# @pytest.mark.asyncio
# async def test_event_duration_periods_strategy_calculate_duration(
#         event_duration_periods_strategy, sample_events
# ):
#     result = await event_duration_periods_strategy.calculate_duration(
#         sample_events, event_name="Event 1", period_days=1, num_periods=3
#     )
#     assert isinstance(result, pd.DataFrame)
#     assert len(result) == 3
#     assert all(result.columns == ["Date", "Day", "Duration", "Period"])
#     assert all(result["Duration"].values == [2.0, 0.0, 0.0])


@pytest.mark.asyncio
async def test_event_duration_periods_strategy_not_enough_data_error(
    event_duration_periods_strategy, sample_events
):
    with pytest.raises(ValueError):
        await event_duration_periods_strategy.calculate_duration(
            sample_events, event_name="Event 1", period_days=6, num_periods=2
        )


@pytest.mark.asyncio
async def test_async_data_transformer_no_strategy(
    async_data_transformer, sample_events
):
    with pytest.raises(ValueError):
        await async_data_transformer.calculate_duration(sample_events)
