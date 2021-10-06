from logging import debug
import ssl
from datetime import datetime
from aiohttp import web
from jsonrpcserver import method, async_dispatch
from jsonrpcserver.methods import Methods

from hive_attention_tokens.network.api import net


def run_server(config):
    app = web.Application()
    #app['db'] = AttentionTokensDb(config)

    async def status_report(request):
        report = {
            'name': 'Hive Attention Tokens',
            'timestamp': datetime.utcnow().isoformat()
        }
        return web.json_response(status=200, data=report)

    async def handler(request):
        try:
            #response = await async_dispatch(request, methods=all_methods, debug=True, context=app)
            return web.Response(
                text=await async_dispatch(await request.text()),
                content_type="application/json",
                headers = {'Access-Control-Allow-Origin': '*'}
            )
        except Exception as e:
            print(e)

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
        port=3636,
        ssl_context=context
    )