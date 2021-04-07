"""Defines all transaction types, their validation rules and hosts transaction-wide tools"""
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

def get_counter_account(trans):
    if trans[0] == 'air':
        return trans[1]
    elif trans[0] == 'trn':
        return trans[2]