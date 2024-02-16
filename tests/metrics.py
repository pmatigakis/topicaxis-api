from asyncio import AbstractEventLoop
from unittest.mock import MagicMock, call, patch

import pytest
from fastapi.exceptions import HTTPException
from statsd import StatsClient

from topicaxisapi.metrics import collect_endpoint_metrics


@patch("topicaxisapi.metrics.perf_counter")
def test_collect_endpoint_metrics(
    mock_perf_counter, event_loop: AbstractEventLoop
):
    mock_perf_counter.side_effect = [0.1, 0.5]
    mocked_statsd_client = MagicMock(spec=StatsClient)

    async def endpoint_function(statsd_client):
        pass

    f = collect_endpoint_metrics("my-metric")(endpoint_function)
    event_loop.run_until_complete(f(statsd_client=mocked_statsd_client))

    mocked_statsd_client.incr.assert_called_once_with("my-metric.request")
    mocked_statsd_client.timing.assert_called_once_with(
        "my-metric.duration", 400.0
    )


@patch("topicaxisapi.metrics.perf_counter")
def test_collect_endpoint_metrics_when_endpoint_raised_exception(
    mock_perf_counter, event_loop: AbstractEventLoop
):
    mock_perf_counter.side_effect = [0.1, 0.5]
    mocked_statsd_client = MagicMock(spec=StatsClient)

    async def endpoint_function(statsd_client):
        raise ValueError()

    f = collect_endpoint_metrics("my-metric")(endpoint_function)

    with pytest.raises(ValueError):
        event_loop.run_until_complete(f(statsd_client=mocked_statsd_client))

    mocked_statsd_client.incr.assert_has_calls(
        [call("my-metric.request"), call("my-metric.error")]
    )
    mocked_statsd_client.timing.assert_called_once_with(
        "my-metric.duration", 400.0
    )


@patch("topicaxisapi.metrics.perf_counter")
def test_collect_endpoint_metrics_when_endpoint_raised_4xx_exception(
    mock_perf_counter, event_loop: AbstractEventLoop
):
    mock_perf_counter.side_effect = [0.1, 0.5]
    mocked_statsd_client = MagicMock(spec=StatsClient)

    async def endpoint_function(statsd_client):
        raise HTTPException(status_code=404)

    f = collect_endpoint_metrics("my-metric")(endpoint_function)

    with pytest.raises(HTTPException):
        event_loop.run_until_complete(f(statsd_client=mocked_statsd_client))

    mocked_statsd_client.incr.assert_called_once_with("my-metric.request")
    mocked_statsd_client.timing.assert_called_once_with(
        "my-metric.duration", 400.0
    )


@patch("topicaxisapi.metrics.perf_counter")
def test_collect_endpoint_metrics_when_endpoint_raised_5xx_exception(
    mock_perf_counter, event_loop: AbstractEventLoop
):
    mock_perf_counter.side_effect = [0.1, 0.5]
    mocked_statsd_client = MagicMock(spec=StatsClient)

    async def endpoint_function(statsd_client):
        raise HTTPException(status_code=500)

    f = collect_endpoint_metrics("my-metric")(endpoint_function)

    with pytest.raises(HTTPException):
        event_loop.run_until_complete(f(statsd_client=mocked_statsd_client))

    mocked_statsd_client.incr.assert_has_calls(
        [call("my-metric.request"), call("my-metric.error")]
    )
    mocked_statsd_client.timing.assert_called_once_with(
        "my-metric.duration", 400.0
    )
