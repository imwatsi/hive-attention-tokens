
DB_VERSION = 1

class DbSchema:
    def __init__(self):
        self.tables = {}
        self._populate_tables()

    def _populate_tables(self):

        # Hive Accounts
        hive_accounts = """
            CREATE TABLE IF NOT EXISTS hive_accounts (
                name varchar(16) PRIMARY KEY,
                owner char(53) NOT NULL,
                active char(53) NOT NULL,
                posting char(53) NOT NULL,
                memo char(53) NOT NULL
            );"""
        self.tables['hive_accounts'] = hive_accounts

        # blocks table
        blocks = """
            CREATE TABLE IF NOT EXISTS blocks (
                index integer PRIMARY KEY,
                hash char(64) NOT NULL,
                timestamp timestamp NOT NULL,
                previous_hash char(64) NOT NULL,
                witness varchar(16) NOT NULL REFERENCES hive_accounts (name),
                signature char(88) NOT NULL
            );"""
        self.tables['blocks'] = blocks

        transactions = """
            CREATE TABLE IF NOT EXISTS transactions (
                hash char(64) PRIMARY KEY,
                block_num integer NOT NULL REFERENCES blocks (index),
                index integer NOT NULL,
                data varchar NOT NULL,
                signature char(88),
                account varchar(16) NOT NULL REFERENCES hive_accounts (name)
            );"""
        self.tables['transactions'] = transactions

        virtual_transactions = """
            CREATE TABLE IF NOT EXISTS virtual_transactions (
                block_num integer NOT NULL REFERENCES blocks (index),
                index integer NOT NULL,
                data varchar NOT NULL,
                account varchar(16) NOT NULL REFERENCES hive_accounts (name)
            );"""
        self.tables['virtual_transactions'] = virtual_transactions

        tokens = """
            CREATE TABLE IF NOT EXISTS tokens (
                id char(12) PRIMARY KEY,
                owner varchar(16) NOT NULL REFERENCES hive_accounts (name),
                init_transaction_id char(64) NOT NULL REFERENCES transactions (hash),
                props json NOT NULL
            );"""
        self.tables['tokens'] = tokens

        token_transfers = """
            CREATE TABLE IF NOT EXISTS token_transfers (
                transaction_id char(64) PRIMARY KEY REFERENCES transactions (hash),
                token_id char(12),
                from_acc varchar(16) NOT NULL REFERENCES hive_accounts (name),
                to_acc varchar(16) NOT NULL REFERENCES hive_accounts (name),
                amount numeric(10,3)
            );"""
        self.tables['token_transfers'] = token_transfers

        token_stakes = """
            CREATE TABLE IF NOT EXISTS token_stakes (
                token_id char(12) PRIMARY KEY,
                transaction_id char(64) NOT NULL REFERENCES transactions (hash),
                owner varchar(16) NOT NULL REFERENCES hive_accounts (name),
                amount numeric(10,3)
            );"""
        self.tables['token_stakes'] = token_stakes

        token_emissions = """""" # TODO

        global_props = """
            CREATE TABLE IF NOT EXISTS global_props (
                db_version smallint
            );"""
        self.tables['global_props'] = global_props