class ChainState:
    """"""
    stage = "pre_consensus"
    hive_start_block = None
    
    @classmethod
    def get_chain_stage(cls):
        return cls.stage
    
    @classmethod
    def get_hive_genesis_block_num(cls):
        return cls.hive_start_block
    
    @classmethod
    def set_hive_genesis_block(cls, num):
        # TODO: check if the num is an irreversible block on Hive (LIB)
        cls.hive_start_block = num
    
    class PreConsensus:
        """"""
        def __init__(self) -> None:
            pass