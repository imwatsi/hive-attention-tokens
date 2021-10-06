import json
from os import times
from hive_attention_tokens.database.setup import DbSession
from hive_attention_tokens.consensus.state import ChainState

class AttentionTokensDb:
    """Avails method handlers for common DB operations and also exposes direct
       DB actions through `self.db.select`, `self.db.execute` and `self.db.execute_immediate`"""

    def __init__(self, config):
        self.db = DbSession(config)
        self.config = config
        self.schema = self.db.live_schema

    # TOOLS

    def _populate_by_schema(self, data, fields):
        result = {}
        for i in range(len(fields)):
            result[fields[i]] = data[i]
        return result
    
    def _populate_by_schema_list(self, data, fields):
        result = []
        for d in data:
            entry = self._populate_by_schema(d, fields)
            result.append(entry)
        return result


    # ACCESS METHODS

    def _select(self, table, columns=None, col_filters=None, order_by=None, limit=None):
        if columns:
            _columns = ', '.join(columns)
        else:
            _columns = "*"

        sql = f"SELECT {_columns} FROM {table}"

        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = '{value}'")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        sql += ";"
        return self.db.select(sql)

    def _select_one(self, table, col_filters):
        sql = f"SELECT 1 FROM {table}"
        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = '{value}'")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        return bool(self.db.select(sql))

    def _insert(self, table, data):
        _columns = []
        _values = []
        for col in data:
            _columns.append(col)
            _values.append(f"%({col})s")
        columns = ', '.join(_columns)
        values = ', '.join(_values)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        sql += ";"
        self.db.execute(sql, data)

    def _update(self, table, data, col_filters= {}):
        _values = []
        for col, value in data.items():
            if value is None: continue
            _values.append (f"{col} = %({col})s")
        _final_values = ', '.join(_values)

        sql = f"UPDATE {table} SET {_final_values}"

        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = %(f_{col})s")
                data[f"f_{col}"] = col_filters[col]
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        sql += ";"
        self.db.execute(sql, data)
    
    def _delete(self, table, col_filters):
        sql = f"DELETE FROM {table}"
        if isinstance(col_filters, dict):
            _filters = []
            for col in col_filters:
                _filters.append (f"{col} = %({col}s")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        sql += ";"
        self.db.execute(sql, col_filters)

    def _save(self):
        self.db.commit()

    # GLOBAL PROPS

    def get_db_head(self):
        res = self._select('blocks', ['num', 'hash', 'timestamp'], order_by="num DESC", limit=1)
        if res:
            return res[0]
        else:
            return None

    def get_db_version(self):
        res = self._select('global_props', ['db_version'])
        return res[0]

    def has_global_props(self):
        res = self._select('global_props')
        if res:
            return True
        else:
            return False

    # BLOCKS

    def add_block(self, block_num, block_hash, prev, created_at):
        self._insert('blocks', {
            'num': block_num,
            'hash': block_hash,
            'prev': prev,
            'timestamp': created_at

        })

    def get_block_range(self, start_time, end_time):
        query = f"""
                    SELECT min(num), max(num) FROM blocks
                        WHERE timestamp BETWEEN {start_time} AND {end_time};
                """
        res = self.db.select(query)
        return res
    
    def get_genesis_info(self):
        res = self._select('hat_blocks', ['num', 'timestamp'], col_filters={'num':0})
        if res:
            return self._populate_by_schema(res[0], ['num', 'timestamp'])
        return None

    # HIVE ACCOUNTS

    def add_new_hive_account(self, acc_name, owner, active, posting, memo):
        self._insert('hive_accounts', {
            'name': acc_name,
            'owner': owner,
            'active': active,
            'posting': posting,
            'memo': memo
        })
    
    def account_exists(self, acc_name):
        return bool(self._select('hive_accounts', col_filters={'name': acc_name}))
    
    def get_account(self, acc_name):
        res = self._select('hive_accounts', col_filters={'name': acc_name})
        return self._populate_by_schema(res[0], self.schema['hive_accounts']) if res else None

    # HIVE TRANSACTIONS

    def add_new_transaction(self, trans_id, block, trx_in_block, timestamp, op):
        try:
            _op_json = op.encode('unicode-escape').decode()
            loaded = json.loads(_op_json)
            del loaded
            self._insert('hat_transactions', {
                'id': trans_id,
                'block_num': block,
                'trx_in_block': trx_in_block,
                'timestamp': timestamp,
                'data': _op_json
            })
        except:
            # skip invalid JSON
            print(_op_json)
            return

    def get_latest_block_num(self):
        res = self.db.execute("SELECT MAX(block) FROM hat_transactions")
        return res[0]
    
    # HAT BLOCKS

    def add_new_hat_block(self, num, transactions, hash, timestamp, witness, signature):
        self._insert('hat_blocks', {
            'num': num,
            'transactions': transactions,
            'hash': hash,
            'timestamp': timestamp,
            'witness': witness,
            'signature': signature
        })
    
    # TOKENS

    def add_new_token(self, token_id, owner, init_trans_id, props):
        self._insert('tokens', {
            'id': token_id,
            'owner': '@@sys',
            'init_transaction_id': '0000000000000000000000000000000000000000',
            'props': json.dumps(props)
        })
    
    def is_valid_token(self, token_id):
        return self._select_one('tokens', {'id': token_id})
    
    def add_new_content_vote(self):
        pass

    # WITNESS VOTES

    def add_new_witness_vote(self, voter, witness, vote):
        self._insert('witness_votes',{
            'voter': voter,
            'witness': witness,
            'vote': vote
        })
    
    def update_witness_vote(self, voter, witness, vote):
        self._update(
            'witness_votes',
            {'vote': vote},
            col_filters={'voter': voter, 'witness': witness}
        )
    
    def get_genesis_votes(self):
        """Retrieve witness ranked votes for genesis."""
        # Stake Balances
        genesis_stake_balances = f"""
            SELECT tpu.owner, sum(tpu.amount) FROM (
                SELECT tr.timestamp, tpu.owner, tpu.amount
                        FROM token_powerups tpu
                        JOIN hat_transactions tr ON tpu.transaction_id = tr.id
                            AND (tr.timestamp + 30 days ) > NOW()
                            AND tr.timestamp IS NOT IN (
                                SELECT genesis_timestamp FROM global_props
                            )
            );"""


        if ChainState.get_chain_stage() != 'pre_consensus': return []
        genesis_timestamp = ChainState.get_hive_genesis_block_num()
        sql = f"""
            SELECT sum(amount)
                FROM (
                        SELECT tr.timestamp, tpu.amount
                        FROM token_powerups tpu
                        JOIN hat_transactions tr ON tpu.transaction_id = tr.id
                            AND tr.timestamp < {genesis_timestamp}
                ); 
        """
        # TODO: investigate unique on acc
        res = self.db.select(sql)
        if res:
            return self._populate_by_schema_list(res, ['timestamp', 'amount'])

    
    def get_acc_witness_vote(self, acc, witness):
        res = self._select_one('witness_votes', col_filters={'voter': acc, 'witness': witness})
        return bool(res)
    
    def get_all_acc_witness_votes(self, acc):
        res = self._select('witness_votes', col_filters={'voter': acc})
        return self._populate_by_schema_list(res, self.schema['witness_votes'])
    
    # TOKEN CLAIMDROPS

    def get_acc_token_claimdrop(self, acc, token):
        res = self._select_one('claimdrops', col_filters={'account': acc, 'token_id': token})
        return bool(res)
    
    def add_new_claimdrop(self, transaction_id, acc, token):
        res = self._insert(
            'claimdrops',
            {
                'transaction_id': transaction_id,
                'account': acc,
                'token_id': token
            }
        )
    
    # TOKEN STAKING

    def get_hat_stake_balance(self, acc):
        if ChainState.get_chain_stage() == 'pre_consensus': return []
        genesis_timestamp = ChainState.get_hive_genesis_block_num()
        sql = f"""
            SELECT sum(amount)
                FROM (
                        SELECT tr.timestamp, tpu.amount
                        FROM token_powerups tpu
                        JOIN hat_transactions tr ON tpu.transaction_id = tr.id
                        WHERE tpu.owner = '{acc}'
                            AND (tr.timestamp + 30 days ) > NOW()
                            AND tr.timestamp IS NOT {genesis_timestamp}
                );
        """
        res = self.db.select(sql)
        if res:
            return self._populate_by_schema_list(res, ['timestamp', 'amount'])
