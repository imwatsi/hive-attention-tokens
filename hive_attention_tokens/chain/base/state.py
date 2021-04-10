"""Tied to block processing. A top level representation of the results
    of all transactions in all blocks processsed thus far.
    accounts, acc bals, token bals, markets, token contracts.
    periodic state snapshots, running hash"""

from decimal import Decimal
from hive_attention_tokens.utils.tools import NATIVE_TOKEN_ID, SYSTEM_ACCOUNT

class StateMachine:

    @classmethod
    def token_genesis_action(cls,token_id, props):
        GenesisAction(token_id, props)

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


class GenesisAction:
    def __init__(self, token_id, props):
        self.token = token_id
        self.props = props
        self.verify()
        self.process()
    
    def verify(self):
        exists = Tokens.check_token_existence(self.token)
        if exists: raise Exception(f"Token '{self.token}' already exists")
    
    def process(self):
        Tokens.add_new_token(self.token, self.props)
        TokenBalances.genesis(self.token, self.props['initial_supply'])

class AirdropAction:

    def __init__(self, token_id, to_acc, amount):
        self.token = token_id
        self.to_acc = to_acc
        self.amount = amount
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


class Tokens:
    """Keeps track of token types and their props"""
    tokens = {}

    @classmethod
    def add_new_token(cls, token, props):
        cls.tokens[token] = props

    @classmethod
    def check_token_existence(cls, token):
        # TODO: check in Tokens registry
        if token in TokenBalances.liquid_balances or token in TokenBalances.savings_balances or token in TokenBalances.staked_balances:
            return True
        return False


class TokenBalances:
    
    liquid_balances = {}
    liquid_totals = {}

    savings_balances = {}
    savings_totals = {}

    staked_balances = {}
    staked_totals = {}
    
    # TOTALS

    @classmethod
    def get_liquid_total(cls, token):
        if token in cls.liquid_totals:
            return cls.liquid_totals[token]
        else:
            return Decimal("{:.3f}".format(0))

    @classmethod
    def get_savings_total(cls, token):
        if token in cls.savings_totals:
            return cls.savings_totals[token]
        else:
            return Decimal("{:.3f}".format(0))
    
    @classmethod
    def get_staked_total(cls, token):
        if token in cls.staked_totals:
            return cls.staked_totals[token]
        else:
            return Decimal("{:.3f}".format(0))

    # BALANCES

    @classmethod
    def get_balance(cls, form, token, acc):
        if form == 'liquid':
            ref = cls.liquid_balances
        elif form == 'savings':
            ref = cls.savings_balances
        elif form == 'staked':
            ref = cls.staked_balances
        if acc not in ref[token]:
            ref[token][acc] = Decimal("0.000")
            return Decimal("0.000")
        return ref[token][acc]
    
    @classmethod
    def get_balances(cls, acc):
        # TODO: verify account
        final = {}
        for form in ['liquid', 'savings', 'staked']:
            if form == 'liquid':
                ref = cls.liquid_balances
            elif form == 'savings':
                ref = cls.savings_balances
            elif form == 'staked':
                ref = cls.staked_balances
            result = {}
            tokens = list(ref.keys())
            for token in tokens:
                result[token] = cls.get_balance(form, token, acc)
            result['token_map'] = tokens
            final[form] = dict(result)
            del result
        return final

    @classmethod
    def genesis(cls, token, amount):
        cls.liquid_balances[token] = {
            SYSTEM_ACCOUNT: Decimal("{:.3f}".format(amount))
        }
        cls.liquid_totals[token] = Decimal("{:.3f}".format(amount))

        cls.savings_balances[token] = {
            SYSTEM_ACCOUNT: Decimal("{:.3f}".format(0))
        }
        cls.savings_totals[token] = Decimal("{:.3f}".format(0))

        cls.staked_balances[token] = {
            SYSTEM_ACCOUNT: Decimal("{:.3f}".format(0))
        }
        cls.staked_totals[token] = Decimal("{:.3f}".format(0))

    @classmethod
    def airdrop_liquid(cls, token, to_acc, amount):
        cur_bal = cls.get_balance('liquid', token, to_acc)
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