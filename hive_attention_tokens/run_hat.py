from hive_attention_tokens.chain.base.blockchain import Blockchain, BlockchainState
from hive_attention_tokens.chain.base.witness import BlockSchedule
from hive_attention_tokens.chain.base.auth import HiveAccounts
from hive_attention_tokens.chain.database.setup import DbSetup
from hive_attention_tokens.chain.database.handlers import AttentionTokensDb
from hive_attention_tokens.chain.database.access import DbAccess
from hive_attention_tokens.config import Config
from hive_attention_tokens.server.serve import run_server

from threading import Thread

def run():
    config = Config.load_config()
    HiveAccounts.init(BlockchainState)
    db_head_block = Blockchain.has_db_blocks()
    # TODO: load all accounts
    if db_head_block:
        BlockchainState.state_replaying()
        for i in range(db_head_block[0]+1):
            Blockchain.process_existing_block(i)
        BlockchainState.update_cur_block(
            db_head_block[0],
            db_head_block[1],
            db_head_block[2]
        ) # temp
    else:
        BlockchainState.state_genesis()
        Blockchain.create_genesis_state()
    Thread(target=BlockSchedule.block_schedule).start()
    run_server(config)

if __name__ == "__main__":
    run()