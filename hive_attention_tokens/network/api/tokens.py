from random import randint
from jsonrpcserver import method, Result, Success
from hive_attention_tokens.network.peers import Peers

@method(name="tokens_api.get_content_votes")
async def get_content_votes() -> Result:
    """Returns the list of current active peers of the node."""
    return Success(randint(1,100))
