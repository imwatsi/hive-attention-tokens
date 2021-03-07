import json
from hashlib import sha256
from datetime import datetime

BLANK_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
UTC_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
NATIVE_TOKEN_ID = "AA0000000000"

def validate_data_rules(data, rules, description):
    for k in rules:
        if k not in data:
            raise Exception(f"Missing key '{k}' from {description}")
        expected_type = rules[k][0]
        max_length = rules[k][1]
        if not isinstance(data[k], expected_type):
            raise Exception(f"Invalid data type for key '{k}'; expected {expected_type}")
        if expected_type == int:
            if max_length and data[k] > max_length:
                raise Exception(f"Data for key '{k}' exceeds max ({max_length})")
        else:
            if max_length and len(data[k]) > (max_length-1):
                raise Exception(f"Data for key '{k}' exceeds max length ({max_length})")

def get_hash_sha256(data):
    block_string = json.dumps(data, sort_keys=True)
    return sha256(block_string.encode()).hexdigest()

def timestamp_to_string(timestamp):
    return datetime.strftime(timestamp, UTC_TIMESTAMP_FORMAT)