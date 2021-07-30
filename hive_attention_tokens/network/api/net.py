from hive_attention_tokens.network.peers import Peers


async def get_current_peers(context):
    """Returns the list of current active peers of the node."""
    return Peers.get_current_peers()


async def get_node_info(context):
    """Returns detailed info about the running node, including its list of active peers."""
    details = {
        "node": Peers.get_own_info(),
        "peers": Peers.get_current_peers()
    }
    return details