import os
from cdecimal import Decimal

version = "0.0.18.c"
block_reward = 100  # Initial block reward
miner_core_count = -1  # -1 evaluates to number of cores
# Lower limits on what the "time" tag in a block can say.
median_block_time_limit = 100
# Take the median of this many of the blocks.
# How far back in history do we look when we use statistics to guess at
# the current blocktime and difficulty.
history_length = 110
# How far in history we look when we determine next block reward

# This constant is selected such that the 50 most recent blocks count for 1/2 the
# total weight.
inflection = Decimal('0.98')
# How often to generate a block in seconds
blocktime = 60
halve_at = (365 * 24 * 60 * 60 / blocktime)  # Approximately one year
recalculate_target_at = (4*60*60 // blocktime)  # It's every 4 hours

# Precalculate
memoized_weights = [inflection ** i for i in range(history_length)]

assignment_period = 5  # Assign jobs at each T rounds
unassignment_after = 12   # Unassign jobs after T*M rounds
pool_reg_amount = 1000

first_target = '0' * 4 + 'f' * 60

# Coinami root certificate.
# Everyone will accept any certificate that is signed by the root
root_cert_pem = b"""-----BEGIN CERTIFICATE-----
MIICXjCCAgWgAwIBAgIJAMVH45qrPCKOMAoGCCqGSM49BAMCMIGDMQswCQYDVQQG
EwJUUjEPMA0GA1UECAwGVHVya2V5MQ8wDQYDVQQHDAZBbmthcmExEDAOBgNVBAoM
B0JpbGtlbnQxCzAJBgNVBAsMAkNTMRIwEAYDVQQDDAlDYW4gQWxrYW4xHzAdBgkq
hkiG9w0BCQEWEGNhbGthbkBnbWFpbC5jb20wHhcNMTcxMjExMTU0NDM0WhcNMzcx
MjA2MTU0NDM0WjCBgzELMAkGA1UEBhMCVFIxDzANBgNVBAgMBlR1cmtleTEPMA0G
A1UEBwwGQW5rYXJhMRAwDgYDVQQKDAdCaWxrZW50MQswCQYDVQQLDAJDUzESMBAG
A1UEAwwJQ2FuIEFsa2FuMR8wHQYJKoZIhvcNAQkBFhBjYWxrYW5AZ21haWwuY29t
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEScpcjAlHsl9/CivkjIQnHVkq2CEHlzaH
KZlXb10rTTUIpKx4R/i3p9aAOB4LwccO+SqzPs0QMpWbnkL5aTf0CaNjMGEwHQYD
VR0OBBYEFHl6OtJ0v6t0MoNcVXPUeNGE6PkPMB8GA1UdIwQYMBaAFHl6OtJ0v6t0
MoNcVXPUeNGE6PkPMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgGGMAoG
CCqGSM49BAMCA0cAMEQCICRaaCknvnRWLrHBq2KlOzSSA5g0rerDqfEeskOGB9Au
AiAqmCqPhs3ICqNPTDZ0Q2SSk0dTZptbG5cGxDgBoefoPg==
-----END CERTIFICATE-----
"""


def generate_default_config():
    config = dict()
    config['DEBUG'] = False

    config['logging'] = {
        'file': 'log'
    }

    config["port"] = {
        "api": int(os.environ.get('HALOCOIN_API_PORT', '7001')),
        "peers": int(os.environ.get('HALOCOIN_PEERS_PORT', '7002'))
    }

    config["peers"] = {
        "list": [
            {
                'node_id': '52e6eb49-6d59-4bf3-af96-ca3252408a4f',
                'ip': '139.179.21.17',
                'port': 7002,
                'rank': 2,
                'diffLength': '',
                'length': -1
            },
            {
                'node_id': '52e6eb49-6d59-4bf3-af96-ca3252408a4e',
                'ip': '159.89.9.43',
                'port': 7002,
                'rank': 1,
                'diffLength': '',
                'length': -1
            }
        ],
        "download_limit": 250
    }

    config["miner"] = {
        "cores": 8
    }

    config["coinami"] = {
        "threads": 4
    }
    return config


def read_config_file(file_address):
    import yaml
    config = yaml.load(open(file_address, 'rb'))
    if 'DEBUG' in config.keys():
        return config
    else:
        return None


def write_config_file(config, file_address):
    import yaml
    yaml.dump(config, open(file_address, 'w'))
