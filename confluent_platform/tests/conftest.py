# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
import time

import pytest
import requests

from datadog_checks.dev import docker_run
from datadog_checks.dev.utils import load_jmx_config

from .common import BASE_URL, HERE, TEST_AUTH, TEST_MESSAGE, TEST_QUEUES, TEST_TOPICS

INSTANCES = [
    {'host': 'localhost',  # confluentinc/cp-zookeeper
     'port': '31000'},  # OK
    {'host': 'localhost',  # confluentinc/cp-server
     'port': '31001'},  # OK
    {'host': 'localhost',  # cnfldemos/cp-server-connect-datagen
     'port': '31002'},  # OK
    {'host': 'localhost',  # confluentinc/cp-enterprise-control-center
     'port': '31003'},  # DOES NOT WORK
    {'host': 'localhost',  # confluentinc/cp-ksql-server
     'port': '31004'},  # OK
    {'host': 'localhost',  # confluentinc/ksql-examples
     'port': '31015'},  # LOCAL ONLY
    {'host': 'localhost',  # confluentinc/cp-kafka-rest
     'port': '31006'},  # OK
    {'host': 'localhost',  # confluentinc/cp-schema-registry
     'port': '31007'},  # OK
    {'host': 'localhost',  # confluentinc/cp-enterprise-replicator
     'port': '31008'},  # OK
]


def populate_server():
    """
    Add some queues and topics to ensure more metrics are available.
    """
    time.sleep(3)

    for queue in TEST_QUEUES:
        url = '{}/{}?type=queue'.format(BASE_URL, queue)
        requests.post(url, data=TEST_MESSAGE, auth=TEST_AUTH)

    for topic in TEST_TOPICS:
        url = '{}/{}?type=topic'.format(BASE_URL, topic)
        requests.post(url, data=TEST_MESSAGE, auth=TEST_AUTH)


@pytest.fixture(scope="session")
def dd_environment():
    with docker_run(
            os.path.join(HERE, 'compose', 'docker-compose.yaml'),
            log_patterns=['Monitored service is now ready'],
            # conditions=[WaitForPortListening(HOST, TEST_PORT), populate_server],
    ):
        config = load_jmx_config()
        config['instances'] = INSTANCES
        yield config, {'use_jmx': True}
