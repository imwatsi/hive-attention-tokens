
DB_VERSION = 1

class DbSchema:
    def __init__(self):
        self.tables = []
        self.indexes = {}
        self.views = {}
        self._populate_tables()
        self._populate_views()
        self._populate_indexes()

    def _populate_tables(self):

        # Accounts
        hive_accounts = """
            CREATE TABLE IF NOT EXISTS hive_accounts (
                name varchar(16) PRIMARY KEY,
                owner char(53) NOT NULL,
                active char(53) NOT NULL,
                posting char(53) NOT NULL,
                memo char(53) NOT NULL
            );"""
        self.tables.append(['hive_accounts', hive_accounts])

        # Blocks
        blocks = """
            CREATE TABLE IF NOT EXISTS blocks (
                num integer PRIMARY KEY,
                hash char(40) NOT NULL,
                prev char(40),
                timestamp timestamp NOT NULL
            );"""
        self.tables.append(['blocks', blocks])

        # blocks table
        blocks = """
            CREATE TABLE IF NOT EXISTS hat_blocks (
                num integer PRIMARY KEY,
                transactions char(64) ARRAY NOT NULL,
                hash char(64) NOT NULL,
                timestamp timestamp NOT NULL,
                witness varchar(16) NOT NULL,
                signature char(88) NOT NULL
            );"""
        self.tables.append(['blocks', blocks])

        # Hive HAT transactions/ops
        hat_transactions = """
            CREATE TABLE hat_transactions (
                id char(40) PRIMARY KEY,
                block_num integer NOT NULL,
                trx_in_block smallint NOT NULL,
                timestamp timestamp NOT NULL,
                data json NOT NULL
            );"""
        self.tables.append(['hat_transactions', hat_transactions])

        virtual_transactions = """
            CREATE TABLE IF NOT EXISTS virtual_transactions (
                block_num integer NOT NULL REFERENCES hat_blocks (num),
                index integer NOT NULL,
                data json NOT NULL,
                account varchar(16) NOT NULL
            );"""
        self.tables.append(['virtual_transactions', virtual_transactions])

        witness_votes = """
            CREATE TABLE IF NOT EXISTS witness_votes (
                voter varchar(16) NOT NULL,
                witness varchar(16) NOT NULL,
                vote boolean NOT NULL,
                UNIQUE (voter, witness)
            );"""
        self.tables.append(['witness_votes', witness_votes])


        tokens = """
            CREATE TABLE IF NOT EXISTS tokens (
                id char(12) PRIMARY KEY,
                owner varchar(16) NOT NULL,
                init_transaction_id char(40) NOT NULL REFERENCES hat_transactions (id),
                props json NOT NULL
            );"""
        self.tables.append(['tokens', tokens])

        token_transfers = """
            CREATE TABLE IF NOT EXISTS token_transfers (
                transaction_id char(64) PRIMARY KEY REFERENCES hat_transactions (id),
                token_id char(12),
                from_acc varchar(16) NOT NULL,
                to_acc varchar(16) NOT NULL,
                amount numeric(10,3)
            );"""
        self.tables.append(['token_transfers', token_transfers])

        token_powerups = """
            CREATE TABLE IF NOT EXISTS token_powerups (
                token_id char(12) PRIMARY KEY,
                transaction_id char(64) NOT NULL REFERENCES hat_transactions (id),
                owner varchar(16) NOT NULL,
                amount numeric(10,3)
            );"""
        self.tables.append(['token_powerups', token_powerups])

        token_powerdowns = """
            CREATE TABLE IF NOT EXISTS token_powerdowns (
                token_id char(12) PRIMARY KEY,
                transaction_id char(64) NOT NULL REFERENCES hat_transactions (id),
                owner varchar(16) NOT NULL,
                amount numeric(10,3)
            );"""
        self.tables.append(['token_powerdowns', token_powerdowns])

        claimdrops = """
            CREATE TABLE IF NOT EXISTS claimdrops (
                transaction_id char(64) NOT NULL REFERENCES hat_transactions (id),
                account varchar(16) NOT NULL,
                token_id char(12)
            );"""

        self.tables.append(['claimdrops', claimdrops])

        token_emissions = """""" # TODO: maybe not, make it emergent property

        global_props = """
            CREATE TABLE IF NOT EXISTS global_props (
                db_version smallint,
                genesis_block integer,
                genesis_timestamp timestamp
            );"""
        self.tables.append(['global_props', global_props])
    
    def _populate_indexes(self):
        trans_blocks_ix = """
            CREATE INDEX trans_blocks_ix
            ON hat_transactions(block_num)
        ;"""
        self.indexes['trans_blocks_ix'] = trans_blocks_ix

        trans_id_ix = """
            CREATE INDEX trans_id_ix
            ON hat_transactions(id)
        ;"""
        self.indexes['trans_id_ix'] = trans_id_ix

        trans_timestamp_ix = """
            CREATE INDEX trans_timestamp_ix
            ON hat_transactions(timestamp)
        ;"""
        self.indexes['trans_timestamp_ix'] = trans_timestamp_ix
    
    def _populate_views(self):
        pass
