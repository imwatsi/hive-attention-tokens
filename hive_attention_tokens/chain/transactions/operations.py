"""Structures of operations."""

OPERATION_DATA_RULES = {
    "airdrop": {
        "token": [str, 16],
        "amount": [int, None]
    },
    "transfer": {
        "token": [str, 16], # replace with custom type
        "amount": [int, None],
        "to": [str, 16]
    },
    "witness_vote": {
        "token": [str, 16],
        "account": [str, 16],
        "value": [bool, None]
    }
}