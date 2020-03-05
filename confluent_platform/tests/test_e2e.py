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

REST_JETTY_METRICS = [
    'kafka.rest.jetty_metrics.connections_active',
    'kafka.rest.jetty_metrics.connections_opened_rate',
]

REST_JETTY_METRICS_OPTIONAL = [
    'kafka.rest.jetty_metrics.connections_closed_rate',
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

SCHEMA_REGISTRY_JETTY_METRICS = [
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

SCHEMA_REGISTRY_METRICS = [
    'kafka.schema.registry.master_slave_role.master_slave_role',
]

BROKER_OPTIONAL_METRICS = [
    'kafka.log.log_flush_stats.log_flush_rate_and_time_ms.avg',
]

REPLICATOR_PRODUCER_METRICS = [
    'kafka.producer.producer_metrics.connection_close_rate',
    'kafka.producer.producer_metrics.connection_close_total',
    'kafka.producer.producer_metrics.connection_count',
    'kafka.producer.producer_metrics.connection_creation_rate',
    'kafka.producer.producer_metrics.connection_creation_total',
    'kafka.producer.producer_metrics.failed_authentication_rate',
    'kafka.producer.producer_metrics.failed_authentication_total',
    'kafka.producer.producer_metrics.failed_reauthentication_rate',
    'kafka.producer.producer_metrics.failed_reauthentication_total',
    'kafka.producer.producer_metrics.incoming_byte_rate',
    'kafka.producer.producer_metrics.incoming_byte_total',
    'kafka.producer.producer_metrics.io_ratio',
    'kafka.producer.producer_metrics.io_time_ns_avg',
    'kafka.producer.producer_metrics.io_wait_ratio',
    'kafka.producer.producer_metrics.io_wait_time_ns_avg',
    'kafka.producer.producer_metrics.io_waittime_total',
    'kafka.producer.producer_metrics.iotime_total',
    'kafka.producer.producer_metrics.network_io_rate',
    'kafka.producer.producer_metrics.network_io_total',
    'kafka.producer.producer_metrics.outgoing_byte_rate',
    'kafka.producer.producer_metrics.outgoing_byte_total',
    'kafka.producer.producer_metrics.request_rate',
    'kafka.producer.producer_metrics.request_size_avg',
    'kafka.producer.producer_metrics.request_size_max',
    'kafka.producer.producer_metrics.request_total',
    'kafka.producer.producer_metrics.response_rate',
    'kafka.producer.producer_metrics.response_total',
    'kafka.producer.producer_metrics.select_rate',
    'kafka.producer.producer_metrics.select_total',
    'kafka.producer.producer_metrics.successful_authentication_no_reauth_total',
    'kafka.producer.producer_metrics.successful_authentication_rate',
    'kafka.producer.producer_metrics.successful_authentication_total',
    'kafka.producer.producer_metrics.successful_reauthentication_rate',
    'kafka.producer.producer_metrics.successful_reauthentication_total',
]

REPLICATOR_PRODUCER_METRICS_OPTIONAL = [
    'kafka.producer.producer_metrics.batch_size_avg',
    'kafka.producer.producer_metrics.batch_size_max',
    'kafka.producer.producer_metrics.bufferpool_wait_time_total',
    'kafka.producer.producer_metrics.produce_throttle_time_avg',
    'kafka.producer.producer_metrics.produce_throttle_time_max',
    'kafka.producer.producer_metrics.record_error_rate',
    'kafka.producer.producer_metrics.record_retry_rate',
    'kafka.producer.producer_metrics.waiting_threads',
]

ALWAYS_PRESENT_METRICS = (BROKER_METRICS
                          + CONNECT_METRICS
                          + REST_JETTY_METRICS
                          + SCHEMA_REGISTRY_JETTY_METRICS
                          + SCHEMA_REGISTRY_METRICS
                          + REPLICATOR_PRODUCER_METRICS
                          )

NOT_ALWAYS_PRESENT_METRICS = (BROKER_OPTIONAL_METRICS
                              + REST_JERSEY_METRICS
                              + SCHEMA_REGISTRY_JERSEY_METRICS
                              + REST_JETTY_METRICS_OPTIONAL
                              + REPLICATOR_PRODUCER_METRICS_OPTIONAL
                              )


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
