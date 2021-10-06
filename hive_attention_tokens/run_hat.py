import json
import os
from datetime import datetime
from threading import Thread

from hive_attention_tokens.network.serve import run_server
from hive_attention_tokens.network.peers import Peers
from hive_attention_tokens.config import Config
from hive_attention_tokens.hive.blocks import BlockStream, BlockProcessor
from hive_attention_tokens.engine.witness_voting import WitnessVoteEffect
from hive_attention_tokens.hive.hive_requests import make_request
from hive_attention_tokens.database.handlers import AttentionTokensDb
from hive_attention_tokens.database.setup import DbSetup
from hive_attention_tokens.utils.tools import START_BLOCK, UTC_TIMESTAMP_FORMAT

config = Config.config

def read_block_direct(block_num):
    resp = make_request("block_api.get_block", {"block_num": block_num})
    block = resp['block']
    return block

def do_fork_check():
    db = AttentionTokensDb(config)
    db_head = db.get_db_head()
    if not db_head: return START_BLOCK
    db_block_num = db_head[0]
    db_block_hash = db_head[1]
    next_block = read_block_direct(db_block_num + 1)
    if next_block['previous'] == db_block_hash:
        print("DB fork check passed")
        return db_block_num + 1
    else:
        print(f"DB fork detected. Shutting down")
        os._exit(1) # TODO: safe shut down feature

def _write_db():
    db = AttentionTokensDb(config)
    return db

def _read_db():
    # TODO: implement multithreaded connection pooling
    db = AttentionTokensDb(config)
    return db

def inits():
    # P2P
    Peers.load_own_info()
    Peers.load_seed_peers()
    print(Peers.get_current_peers())
    Thread(target=Peers.peer_list_refresher).start()
    Thread(target=Peers.peer_list_potentials).start()
    # DB
    DbSetup.check_db(config)
    write_db = _write_db()
    read_db = _read_db()
    # Pre-Genesis
    """
    write_db.add_new_hive_account(
        '@sys',
        'STM00000000000000000000000000000000000000000000000000',
        'STM00000000000000000000000000000000000000000000000000',
        'STM00000000000000000000000000000000000000000000000000',
        'STM00000000000000000000000000000000000000000000000000'
    )
    timestamp = datetime.strftime(datetime.utcnow(), UTC_TIMESTAMP_FORMAT)
    write_db.add_new_hat_block(
        0,
        ['0000000000000000000000000000000000000000'],
        '0000000000000000000000000000000000000000',
        timestamp,
        "@@sys",
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    )
    write_db.add_new_transaction(
        '0000000000000000000000000000000000000000',
        0,
        1,
        timestamp,
        json.dumps(
            {
                "id": "AA0000000000",
                "type": "pob",
                "props": {
                    "supply": {
                        "init_amount": "10000000.000",
                        "emission": None,
                        "emission_target_accs": [["@@rewards", "0.009"], ["@imwatsi.test", "0.001"]],
                        "init_reward_pool": "20000.000"
                    },
                    "voting": "stake_weighted",
                    "airdrop_accounts": [["imwatsi.test","1000.000"], ["imwatsi","1000.000"]]
                }
            }
        )
    )
    write_db.add_new_token(
        'AA0000000000',
        '@@sys',
        '0000000000000000000000000000000000000000',
        {
            "type": "pob",
            "props": {
                "supply": {
                    "init_amount": "10000000",
                    "emission": None,
                    "emission_target_accs": [["@@rewards", "0.009"]],
                    "init_reward_pool": "20000.000"
                },
                "voting": "stake_weighted",
                "airdrop_accounts": [["imwatsi.test","1000.000"], ["imwatsi","1000.000"]]
            }
        }
    )
    
    write_db.add_new_token(
        'SK3636363636',
        '@imwatsi.test',
        '0000000000000000000000000000000000000000',
        {
            "type": "pob",
            "props": {
                "supply": {
                    "init_amount": "10000000",
                    "emission": ["tail_constant", "0.01"],
                    "emission_target_accs": [["@@rewards", "0.009"]],
                    "init_reward_pool": "20000.000"
                },
                "voting": "stake_weighted",
                "airdrop_accounts": [["imwatsi.test","1000.000"], ["hichem.test","1000.000"]]
            }
        }
    )
    write_db.db.commit()
    """
    # Transactions
    WitnessVoteEffect.init(write_db)
    # start Hive sync process
    BlockProcessor.init(write_db)
    BlockStream(do_fork_check())

def run():
    inits()
    run_server(config)



if __name__ == "__main__":
    run()
