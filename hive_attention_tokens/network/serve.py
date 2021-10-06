from logging import debug
import ssl
from datetime import datetime
from aiohttp import web
from jsonrpcserver import method, async_dispatch
from jsonrpcserver.methods import Methods

from hive_attention_tokens.network.api import net_api, tokens_api


def run_server(config):
    app = web.Application()

    async def status_report(request):
        report = {
            'name': 'Hive Attention Tokens',
            'timestamp': datetime.utcnow().isoformat()
        }
        return web.json_response(status=200, data=report)
    
    
    async def handle(request):
        return web.Response(
            text=await async_dispatch(await request.text()), content_type="application/json"
        )

    app.router.add_post("/", handle)
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