import logging
import random

import fastapi

from rholog import jsonformatter
from rholog import rholog as ρ

app = fastapi.FastAPI()
jsonformatter.log_json_to_stdout(indent=2)
log = logging.getLogger("fastapi")
publisher = jsonformatter.JsonLogSpanPublisher(log)


@app.middleware("http")
async def start_a_trace(request: fastapi.Request, call_next):
    scope = request.scope
    span_name = f"{scope['method']} {scope['raw_path'].decode()}"
    with ρ.trace(publisher, span_name) as span:
        request.scope["span"] = span
        response = await call_next(request)
        span.add_context({"status_cdde": response.status_code})
        return response


@ρ.traced
def get_code(span):
    return random.randint(0, 100)


@app.get("/")
def dumbroute(request: fastapi.Request):
    with request.scope["span"].trace("dumbroute") as span:
        return [{"abc": get_code(span)}]
