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

CONNECT_METRICS = [
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

    'kafka.connect.connect_worker_rebalance_metrics.completed_rebalances_total',
    'kafka.connect.connect_worker_rebalance_metrics.epoch',
    'kafka.connect.connect_worker_rebalance_metrics.rebalancing',
    'kafka.connect.connect_worker_rebalance_metrics.time_since_last_rebalance_ms',
]

REST_METRICS = [
    'kafka.rest.jetty_metrics.connections_active',
    'kafka.rest.jetty_metrics.connections_closed_rate',
    'kafka.rest.jetty_metrics.connections_opened_rate',
]

REST_JERSEY_METRICS = [
    'kafka.rest.jersey_metrics.brokers.list.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.assign_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.assignment_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.commit.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.commit_offsets_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.committed_offsets_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.create.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.create_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.delete.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.delete_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.records.read_avro_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.records.read_binary_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.records.read_json_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.seek_to_beginning_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.seek_to_end_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.seek_to_offset_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.subscribe_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.subscription_v2.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.topic.read_avro.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.topic.read_binary.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.topic.read_json.request_error_rate',
    'kafka.rest.jersey_metrics.consumer.unsubscribe_v2.request_error_rate',
    'kafka.rest.jersey_metrics.partition.consume_avro.request_error_rate',
    'kafka.rest.jersey_metrics.partition.consume_binary.request_error_rate',
    'kafka.rest.jersey_metrics.partition.consume_json.request_error_rate',
    'kafka.rest.jersey_metrics.partition.get.request_error_rate',
    'kafka.rest.jersey_metrics.partition.get_v2.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_avro.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_avro_v2.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_binary.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_binary_v2.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_json.request_error_rate',
    'kafka.rest.jersey_metrics.partition.produce_json_v2.request_error_rate',
    'kafka.rest.jersey_metrics.partitions.list.request_error_rate',
    'kafka.rest.jersey_metrics.partitions.list_v2.request_error_rate',
    'kafka.rest.jersey_metrics.request_error_rate',
    'kafka.rest.jersey_metrics.root.get.request_error_rate',
    'kafka.rest.jersey_metrics.root.post.request_error_rate',
    'kafka.rest.jersey_metrics.topic.get.request_error_rate',
    'kafka.rest.jersey_metrics.topic.produce_avro.request_error_rate',
    'kafka.rest.jersey_metrics.topic.produce_binary.request_error_rate',
    'kafka.rest.jersey_metrics.topic.produce_json.request_error_rate',
    'kafka.rest.jersey_metrics.topics.list.request_error_rate',
]

SCHEMA_REGISTRY_METRICS = [
    'kafka.schema.registry.jetty_metrics.connections_active',
    'kafka.schema.registry.jetty_metrics.connections_closed_rate',
    'kafka.schema.registry.jetty_metrics.connections_opened_rate',
]

SCHEMA_REGISTRY_JERSEY_METRICS = [
    'kafka.schema.registry.jersey_metrics.brokers.list.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.assign_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.assignment_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.commit.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.commit_offsets_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.committed_offsets_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.create.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.create_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.delete.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.delete_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.records.read_avro_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.records.read_binary_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.records.read_json_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.seek_to_beginning_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.seek_to_end_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.seek_to_offset_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.subscribe_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.subscription_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.topic.read_avro.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.topic.read_binary.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.topic.read_json.request_error_rate',
    'kafka.schema.registry.jersey_metrics.consumer.unsubscribe_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.consume_avro.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.consume_binary.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.consume_json.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.get.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.get_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_avro.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_avro_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_binary.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_binary_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_json.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partition.produce_json_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partitions.list.request_error_rate',
    'kafka.schema.registry.jersey_metrics.partitions.list_v2.request_error_rate',
    'kafka.schema.registry.jersey_metrics.request_error_rate',
    'kafka.schema.registry.jersey_metrics.root.get.request_error_rate',
    'kafka.schema.registry.jersey_metrics.root.post.request_error_rate',
    'kafka.schema.registry.jersey_metrics.topic.get.request_error_rate',
    'kafka.schema.registry.jersey_metrics.topic.produce_avro.request_error_rate',
    'kafka.schema.registry.jersey_metrics.topic.produce_binary.request_error_rate',
    'kafka.schema.registry.jersey_metrics.topic.produce_json.request_error_rate',
    'kafka.schema.registry.jersey_metrics.topics.list.request_error_rate',
]

BROKER_OPTIONAL_METRICS = [
    'kafka.log.log_flush_stats.log_flush_rate_and_time_ms.avg',
]

ALWAYS_PRESENT_METRICS = BROKER_METRICS + CONNECT_METRICS + REST_METRICS + SCHEMA_REGISTRY_METRICS

NOT_ALWAYS_PRESENT_METRICS = BROKER_OPTIONAL_METRICS + REST_JERSEY_METRICS + SCHEMA_REGISTRY_JERSEY_METRICS


@pytest.mark.e2e
def test_e2e(dd_agent_check):
    instance = {}
    aggregator = dd_agent_check(instance, rate=True)  # type: AggregatorStub

    # Mark default jvm. metrics as asserted
    for metric_name in aggregator._metrics:
        if metric_name.startswith('jvm.'):
            aggregator.assert_metric(metric_name)

    for metric in ALWAYS_PRESENT_METRICS:
        aggregator.assert_metric(metric)

    for metric in NOT_ALWAYS_PRESENT_METRICS:
        aggregator.assert_metric(metric, at_least=0)

    aggregator.assert_all_metrics_covered()
