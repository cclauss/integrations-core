# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest
from six import iteritems

from datadog_checks.base.stubs.aggregator import AggregatorStub
from .metrics import build_metrics

# https://docs.confluent.io/current/kafka/monitoring.html#broker-metrics

BROKER_METRICS = [
    'kafka.cluster.partition.under_min_isr',
    'kafka.connect.connect_worker_metrics.connector_count',
    'kafka.connect.connect_worker_metrics.connector_startup_attempts_total',
    'kafka.connect.connect_worker_metrics.connector_startup_failure_percentage',
    'kafka.connect.connect_worker_metrics.connector_startup_failure_total',
    'kafka.connect.connect_worker_metrics.connector_startup_success_percentage',
    'kafka.connect.connect_worker_metrics.connector_startup_success_total',
    'kafka.connect.connect_worker_metrics.task_count',
    'kafka.connect.connect_worker_metrics.task_startup_attempts_total',
    'kafka.connect.connect_worker_metrics.task_startup_failure_percentage',
    'kafka.connect.connect_worker_metrics.task_startup_failure_total',
    'kafka.connect.connect_worker_metrics.task_startup_success_percentage',
    'kafka.connect.connect_worker_metrics.task_startup_success_total',
    'kafka.controller.controller_stats.leader_election_rate_and_time_ms.avg',
    'kafka.controller.kafka_controller.active_controller_count',
    'kafka.controller.kafka_controller.offline_partitions_count',
    'kafka.network.request_channel.request_queue_size',
    'kafka.network.request_metrics.local_time_ms.avg',
    'kafka.network.request_metrics.remote_time_ms.avg',
    'kafka.network.request_metrics.request_queue_time_ms.avg',
    'kafka.network.request_metrics.response_queue_time_ms.avg',
    'kafka.network.request_metrics.response_send_time_ms.avg',
    'kafka.network.request_metrics.total_time_ms.avg',
    'kafka.network.socket_server.network_processor_avg_idle_percent',
    'kafka.server.delayed_operation_purgatory.purgatory_size',
    'kafka.server.delayed_operation_purgatory.purgatory_size',
    'kafka.server.replica_fetcher_manager.max_lag',
    'kafka.server.replica_manager.leader_count',
    'kafka.server.replica_manager.partition_count',
    'kafka.server.replica_manager.under_min_isr_partition_count',
    'kafka.server.replica_manager.under_replicated_partitions',
]

BROKER_OPTIONAL_METRICS = [
    'kafka.log.log_flush_stats.log_flush_rate_and_time_ms.avg',
]

METRICS = BROKER_METRICS

# metrics not always present
OPTIONAL_METRICS = BROKER_OPTIONAL_METRICS


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance, rate=True)  # type: AggregatorStub

    # Mark jvm. metrics as asserted
    for metric_name in aggregator._metrics:
        if metric_name.startswith('jvm.'):
            aggregator.assert_metric(metric_name)

    for metric in METRICS:
        aggregator.assert_metric(metric)

    for metric in OPTIONAL_METRICS:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()
