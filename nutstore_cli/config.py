# coding: utf-8
import re
from os.path import expanduser, join, exists
from os import getenv

from nutstore_cli.utils.output import debug

CONFIG_KEYS = (
    'username',
    'key',
    'working_dir',
)

DEFAULT_CONFIG_FILENAME = join(expanduser('~'), '.nutstore.config')
DEFAULT_ENV_PREFIX = 'NUTSTORE_'


class ConfigLoader(object):
    PARSE_RE = re.compile('(.+)=(.*)')

    def __init__(self, filename):
        self.config = self.load(filename)

    def load(self, filename):
        config = {}
        if not exists(filename):
            debug('Config file {} not exist'.format(filename))
            return config
        debug('Loading config from {}'.format(filename))
        with open(filename) as f:
            for line in f.xreadlines():
                m = self.PARSE_RE.search(line)
                if m and (m.group(1).strip() in CONFIG_KEYS):
                    k = m.group(1).strip()
                    v = m.group(2).strip()
                    debug('Set "{}" to "{}" in {}'.format(k, v, filename))
                    config[k] = v
            return config


class EnvLoader(object):
    NOT_SET = object()

    def __init__(self, prefix):
        self.config = {}
        for k in CONFIG_KEYS:
            env_key = '{prefix}{key}'.format(prefix=prefix, key=k).upper()
            v = getenv(
                env_key,
                self.NOT_SET
            )
            if v is not self.NOT_SET:
                debug('Set "{}" to "{}" from environment variable {}'.format(k, v, env_key))
                self.config[k] = v


def merge_config(config_filename, env_prefix):
    file_config = ConfigLoader(config_filename)
    env_config = EnvLoader(env_prefix)
    return dict(file_config.config, **env_config.config)  # env config has higher priority


# TODO: set config filename and env prefix in command line
config = merge_config(DEFAULT_CONFIG_FILENAME, DEFAULT_ENV_PREFIX)


def get_config(key):
    return config.get(key, '')
