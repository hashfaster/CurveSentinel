import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from curved import CurveDaemon
from curve_config import CurveConfig


def test_curved():
    config_text = CurveConfig.slurp_config_file(config.curve_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000c9048baaa666e4809285190c16b05ee2daa28bc00c3d40c00dce0b104f8'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = CurveConfig.get_rpc_creds(config_text, network)
    curved = CurveDaemon(**creds)
    assert curved.rpc_command is not None

    assert hasattr(curved, 'rpc_connection')

    # Curve testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = curved.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert curved.rpc_command('getblockhash', 0) == genesis_hash
