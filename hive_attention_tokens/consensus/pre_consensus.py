# get list of nodes
# get votes and allocate to live nodes
# watch for consesus
# sign consensus message

MAJORITY_CONSENSUS_NODES = 2

class PreConsesus:

    @classmethod
    def watch_votes(cls):
        # periodically refresh view
        # tally up
        # sign consesus message (incl chainID) and pass on till all signatures are there
        # post op to Hive
        # change state to live,  add chain ID
        pass