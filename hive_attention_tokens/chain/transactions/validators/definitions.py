"""Defines all transaction types, their validation rules and hosts transaction-wide tools"""
from decimal import Decimal
from hive_attention_tokens.utils.tools import Json, SYSTEM_ACCOUNT

""" trans_type, to_account, token, amount """
AIRDROP = [
    [str, 3],
    [str, 16],
    [str, 12],
    [Decimal, None, 3]
]

""" trans_type, from_account, to_account, token, amount """

def get_counter_account(trans):
    if trans[0] == 'gen':
        return SYSTEM_ACCOUNT
    elif trans[0] == 'air':
        return trans[1]
    elif trans[0] == 'trn':
        return trans[2]
    elif trans[0] == 'vot':
        return trans[2]