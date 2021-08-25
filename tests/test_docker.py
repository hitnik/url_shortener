import os
from contextlib import contextmanager
from subprocess import Popen

import docker
import pytest
import yaml


def service_count(path):
    with open(path, 'r') as file:
        yml = yaml.load(file.read(), Loader=yaml.BaseLoader)
    return len(yml['services'])


@contextmanager
def compose_manager():
    with Popen(['docker-compose', 'up', '-d']) as p:
        try:
            yield p
        finally:
            os.popen('docker-compose kill -s SIGINT')


def test_docker(skip_docker):
    if skip_docker:
        pytest.skip()
    count = service_count('./docker-compose.yml')
    client = docker.DockerClient()
    client.ping()
    cont_count = client.info()['ContainersRunning']
    with compose_manager() as manager:
        manager.wait(timeout=10)
        assert client.info()['ContainersRunning'] == cont_count + count
    client.close()
