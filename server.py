from argparse import ArgumentParser
from aiohttp import web
import re
import subprocess

async def ip_handler(request: web.Request):
    try:
        ipmi_output = subprocess.check_output("ipmitool lan print".split(" "), text=True)
        matches = re.findall(r"IP Address\s*:\s*(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})", ipmi_output)
        return matches[0][0]
    except Exception:
        raise web.HTTPInternalServerError()

async def get_app(args):
    app = web.Application()
    app.add_routes([web.get('/ip', handler=ip_handler)])
    return app

if __name__ == "__main__":
    p = ArgumentParser("ipmi-ip-server")
    p.add_argument("--host", default="0.0.0.0", type=str)
    p.add_argument("--port", default=4788, type=int)
    
    args = p.parse_args()
    app = get_app(args)
    web.run_app(app=app, host=args.host, port=args.port)