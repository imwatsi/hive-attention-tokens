import json

from os import truncate
from hive_attention_tokens.database.handlers import AttentionTokensDb
from hive_attention_tokens.hive.validation import Validation
from hive_attention_tokens.engine.processor import TransactionsProcessor

class BlockProcessor:

    @classmethod
    def init(cls, db):
        cls.db = db
        cls.head_block = {}
        cls.block_num = 0
        cls.block_time = ''
    
    @classmethod
    def check_op_id(cls, op_id):
        return op_id == 'hat-test'
    
    @classmethod
    def process_block(cls, block_num, block):
        prev = block['previous']
        block_hash = block['block_id']
        timestamp = block['timestamp']

        cls.db.add_block(block_num, block_hash, prev, timestamp)
        transactions = block['transactions']
        for i in range(len(transactions)):
            trans = transactions[i]
            trans_id = block['transaction_ids'][i]
            for op in trans['operations']:
                if op['type'] == 'custom_json_operation':
                    if cls.check_op_id(op['value']['id']):
                        req_auths = op['value']['required_auths']
                        req_posting_auths = op['value']['required_posting_auths']
                        cls.db.add_new_transaction(
                            trans_id,
                            block_num,
                            timestamp,
                            req_auths,
                            req_posting_auths,
                            op['value']['json'])
                        cls.process_transaction(
                            trans_id,
                            block_num,
                            timestamp,
                            req_auths,
                            req_posting_auths,
                            op['value']
                        )
        cls.db._save()
        cls.block_num = block_num
        cls.block_time = timestamp

    @classmethod
    def process_transaction(cls, trans_id, block, timestamp, req_auths, req_posting_auths, transaction):
        _op_json = transaction['json'].encode('unicode-escape').decode()
        _json = json.loads(_op_json)
        header = _json[0]
        trans_type = _json[1]
        payload = _json[2]
        try:
            Validation.validate_transaction(req_auths, req_posting_auths, header, trans_type, payload)
            TransactionsProcessor.process_transaction(trans_id, block, timestamp, req_auths, req_posting_auths, trans_type, payload)
        except Exception as e:
            # TODO: log
            print(e)