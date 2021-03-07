"""Defines all transaction types and validation rules."""

""" trans_type, to_account, token, amount """
AIRDROP = [
    [str, 3],
    [str, 16],
    [str, 12],
    [float, None, 3]
]

""" trans_type, from_account, to_account, token, amount """

TRANSFER = [
    [str, 3],
    [str, 16],
    [str, 16],
    [str, 12],
    [float, None, 3]
]