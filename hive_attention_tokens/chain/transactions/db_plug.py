from hive_attention_tokens.chain.database.access import DbAccess

db = DbAccess.db

class DbTransactions:
        

    @classmethod
    def new_transaction(cls, data):
        db._insert('transactions', data)

    @classmethod
    def new_token_transfer(cls, data):
        db._insert('token_transfers', data)
    
    @classmethod
    def new_token_genesis(cls, data):
        db._insert('tokens', data)