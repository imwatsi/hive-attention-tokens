import json
from hashlib import sha256
from datetime import datetime
from decimal import Decimal

BLANK_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
UTC_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
NATIVE_TOKEN_ID = "AA0000000000"
SYSTEM_ACCOUNT = "@@sys"
MAX_TOKEN_LEN = 12
MAX_TOKEN_AMOUNT = None
TOKEN_DECIMAL_PLACES = 3

class Json:
    """Custom JSON object type"""
    def __new__(self, payload):
        self.json_object = json.loads(payload)
        self.len = len(payload)
        return self
    
    def __str__(self):
        return json.dumps(self.json_object)

def _clean_values_dict(data):
    new = {}
    for k in data:
        if isinstance(data[k], Decimal):
            new[k] = str(data[k])
    return new

def normalize_json(data):
    if isinstance(data, dict):
        for k in data:
            if isinstance(data[k], dict):
                data[k] = _clean_values_dict(data[k])
        data = _clean_values_dict(data)
    return json.dumps(data)

def parse_transaction_payload(payload):
    elements = []
    buffer = ""
    in_line = False
    for ch in payload:
        if ch == '"': in_line = not in_line
        if ch == "," and not in_line:
            elements.append(buffer)
            buffer = ""
            continue
        buffer += ch
    elements.append(buffer)
    return elements

def get_counter_account(trans):
    if trans[0] == 'gen':
        return SYSTEM_ACCOUNT
    elif trans[0] == 'air':
        return trans[1]
    elif trans[0] == 'trn':
        return trans[2]

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

def validate_sha256_hash(data):
    valid_chars = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2' , '3', '4', '5', '6', '7', '8', '9']
    if not isinstance(data, str): return False
    for x in data.lower():
        if x not in valid_chars: return False
    return True