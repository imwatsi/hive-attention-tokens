from jsonrpcserver import method, Result, Success
from hive_attention_tokens.network.peers import Peers

@method(name="net_api.get_current_peers")
async def get_current_peers() -> Result:
    """Returns the list of current active peers of the node."""
    return Success(Peers.get_current_peers())

@method(name="net_api.get_node_info")
async def get_node_info() -> Result:
    """Returns detailed info about the running node, including its list of active peers."""
    details = {
        "node": Peers.get_own_info(),
        "peers": Peers.get_current_peers()
    }
    return Success(details)