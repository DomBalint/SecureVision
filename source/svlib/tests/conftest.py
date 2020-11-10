import os

import pytest


files = ['test1.yaml', 'test2.yaml', 'test3.yaml']


@pytest.fixture(scope='module')
def desired_config_files():
    return [os.path.join(os.getcwd(), 'data_test', file) for file in files]


params_configs = [
    {
        'mail_server': {
            'host': 'example11.securevison.intra.net',
            'port': '28031'
        }
    },
    {
        'kafka': {
            'bootstrap_servers': 'example22.securevision.intra.net'
        }
    },
    {
        'sql_alchemy': {
            'host': 'example33.securevision.intra.net',
            'port': '27017',
            'user': 'test',
            'password': 'test'
        }
    }
]
params_files_configs = list(tuple(zip(files, params_configs)))


@pytest.fixture(scope='module', params=params_files_configs)
def desired_configs(request):
    return request.param


@pytest.fixture(scope='module')
def whole_config():
    wc = {}
    for conf in params_configs:
        wc.update(conf)
    return wc
