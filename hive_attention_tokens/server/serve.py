import ssl
from datetime import datetime
from aiohttp import web
from jsonrpcserver import method, async_dispatch as dispatch
from jsonrpcserver.methods import Methods
from hive_attention_tokens.chain.database.handlers import AttentionTokensDb
from hive_attention_tokens.chain.base.blockchain import BlockchainState
from hive_attention_tokens.server.normalize import normalize_types
from hive_attention_tokens.server.api import chain, accounts

def build_methods():
    methods = Methods()
    methods.add(**{'chain_api.' + method.__name__: method for method in (
        chain.get_info,
        chain.submit_transaction,
        chain.get_block,
        chain.get_transaction
    )})

    methods.add(**{'accounts_api.' + method.__name__: method for method in (
        accounts.get_account,
        accounts.get_account_history
    )})

    return methods


def run_server(config):
    app = web.Application()
    app['db'] = AttentionTokensDb(config)
    all_methods = build_methods()

    async def status_report(request):
        report = {
            'name': 'Hive Attention Tokens',
            'sync': normalize_types(BlockchainState.get_chain_state()),
            'timestamp': datetime.utcnow().isoformat()
        }
        return web.json_response(status=200, data=report)

    async def handler(request):
        request = await request.text()
        try:
            response = await dispatch(request, methods=all_methods, debug=True, context=app)
        except Exception as e:
            pass

        """
            # create and send error response
            error_response = {
                "jsonrpc":"2.0",
                "error" : {
                    "code": -32602,
                    "data": "Invalid JSON in request: " + str(ex),
                    "message": "Invalid parameters"
                },
                "id" : -1
            }
            headers = {
                'Access-Control-Allow-Origin': '*'
            }
            ret = web.json_response(error_response, status=200, headers=headers, dumps=decimal_serialize)
            if req_res_log is not None:
              req_res_log.info("Request: {} processed in {:.4f}s".format(request, perf_counter() - t_start))

            return ret
        """

        if response is not None and response.wanted:
            headers = {
                'Access-Control-Allow-Origin': '*'
            }
            ret = web.json_response(response.deserialized(), status=200, headers=headers)
            return ret
        else:
            return web.Response()

    app.router.add_post("/", handler)
    app.router.add_get("/", status_report)
    if config['ssl_cert'] != '' and config['ssl_key'] != '':
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
        context.load_cert_chain(
                config['ssl_cert'],
                config['ssl_key']
        )
    else:
        context = None
    web.run_app(
        app,
        host=config['server_host'],
        port=config['server_port'],
        ssl_context=context
    )