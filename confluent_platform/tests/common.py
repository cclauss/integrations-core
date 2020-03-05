# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from datadog_checks.dev import get_docker_hostname, get_here

CHECK_NAME = 'activemq'

HERE = get_here()
HOST = get_docker_hostname()

TEST_QUEUES = ('FOO_QUEUE', 'TEST_QUEUE')
TEST_TOPICS = ('FOO_TOPIC', 'TEST_TOPIC')
TEST_MESSAGE = {'body': 'test_message'}
TEST_AUTH = ('admin', 'admin')

TEST_PORT = 8161
BASE_URL = 'http://{}:{}/api/message'.format(HOST, TEST_PORT)
