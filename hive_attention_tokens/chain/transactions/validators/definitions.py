"""Defines all transaction types and validation rules."""
from decimal import Decimal

""" trans_type, to_account, token, amount """
AIRDROP = [
    [str, 3],
    [str, 16],
    [str, 12],
    [Decimal, None, 3]
]

""" trans_type, from_account, to_account, token, amount """

TRANSFER = [
    [str, 3],
    [str, 16],
    [str, 16],
    [str, 12],
    [Decimal, None, 3]
]