import json
import os

CONFIG_FIELDS = [
    'witness_name', 'posting_key', 'active_key', 'public_active_key',
    'ssl_cert', 'ssl_key', 'server_port', 'db_username',
    'db_password', 'server_host'
]
CONFIG_FILE = f"{os.environ.get('HAT_CONFIG')}"

class Config:
    # TODO: split witness_config from server_config
    @classmethod
    def load_config(self):
        values = {}
        if not os.path.exists(CONFIG_FILE):
            new_conf = open(CONFIG_FILE, 'w')
            new_conf.writelines(f"{field}=\n" for field in CONFIG_FIELDS)
            new_conf.close()
            print(
                'No config file detected. A blank one has been created.\n'
                'Populate it with the correct details and restart hive-attention-tokens.'
            )
            os._exit(1)
        f = open(CONFIG_FILE, 'r').readlines()
        for line in f:
            if '=' in line:
                setting = line.split('=')
                _key = setting[0]
                assert _key in CONFIG_FIELDS, f"invalid config key detected {_key}"
                _value = setting[1].strip('\n ')
                if '[' in _value or '{' in _value:
                    values[_key] = json.loads(_value)
                else:
                    values[_key] = _value
        return values