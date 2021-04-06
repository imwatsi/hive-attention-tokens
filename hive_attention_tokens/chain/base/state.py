"""Tied to block processing. A top level representation of the results
    of all transactions in all blocks processsed thus far.
    accounts, acc bals, token bals, markets, token contracts.
    periodic state snapshots, running hash"""

from decimal import Decimal
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID, SYSTEM_ACCOUNT

class StateMachine:

    @classmethod
    def airdrop_action(cls, token_id, to_acc, amount):
        AirdropAction(token_id, to_acc, amount)

    @classmethod
    def transfer_action(cls, token_id, from_acc, to_acc, amount):
        TransferAction(token_id, from_acc, to_acc, amount)

    @classmethod
    def savings_transfer_action(cls):
        pass

    @classmethod
    def savings_withdraw_action(cls):
        pass


class AirdropAction:

    def __init__(self, token_id, to_acc, amount):
        self.token = token_id
        self.to_acc = to_acc
        self.amount = amount
        if to_acc != SYSTEM_ACCOUNT:
            self.verify()
        self.process()
    
    def verify(self):
        TokenBalances.verify_liquid_balance(self.token, SYSTEM_ACCOUNT, self.amount)
    
    def process(self):
        TokenBalances.airdrop_liquid(self.token, self.to_acc, self.amount)

class TransferAction:

    def __init__(self, token_id, from_acc, to_acc, amount):
        self.token = token_id
        self.from_acc = from_acc
        self.to_acc = to_acc
        self.amount = amount
        self.verify()
        self.process()
    
    def verify(self):
        TokenBalances.verify_liquid_balance(self.token, self.from_acc, self.amount)

    def process(self):
        TokenBalances.transfer_liquid(self.token, self.from_acc, self.to_acc, self.amount)



class TokenBalances:
    
    liquid_balances = {
        NATIVE_TOKEN_ID: {
            '@@sys': Decimal("0.000")
        }
    }

    savings_balances = {
        NATIVE_TOKEN_ID: {
            '@@sys': Decimal("0.000")
        }
    }

    staked_balances = {
        NATIVE_TOKEN_ID: {
            '@@sys': Decimal("0.000")
        }
    }

    @classmethod
    def get_liquid_balance(cls, token, acc):
        # TODO: verify account
        if acc not in cls.liquid_balances[token]:
            cls.liquid_balances[token][acc] = Decimal("0.000")
            return Decimal("0.000")
        return cls.liquid_balances[token][acc]
    
    @classmethod
    def get_liquid_balances(cls, acc):
        # TODO: verify account
        result = {}
        liquid_tokens = list(cls.liquid_balances.keys())
        for token in liquid_tokens:
            result[token] = cls.get_liquid_balance(token, acc)
        result['token_map'] = liquid_tokens
        return result
    
    @classmethod
    def airdrop_liquid(cls, token, to_acc, amount):
        cur_bal = cls.get_liquid_balance(token, to_acc)
        if to_acc != SYSTEM_ACCOUNT: # bypass subtraction if init airdrop
            cls.liquid_balances[token][SYSTEM_ACCOUNT] -= amount
        cls.liquid_balances[token][to_acc] = cur_bal + amount
    
    @classmethod
    def transfer_liquid(cls, token, from_acc, to_acc, amount):
        cls.liquid_balances[token][from_acc] -= amount
        cls.liquid_balances[token][to_acc] += amount

    @classmethod
    def verify_liquid_balance(cls, token, acc, amount):
        """Check if an account has enough tokens to perform an action"""
        if cls.liquid_balances[token][acc] >= amount:
            return True
        else:
            raise Exception('Insufficent balance')