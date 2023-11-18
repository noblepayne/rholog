import logging
import random
import time

import fastapi

import rholog.fastapi as pf
import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p

# Setup logging.
rholog.jsonformatter.log_json_to_stdout(indent=2)
log = logging.getLogger(__name__)
# Setup tracing.
publish = rholog.jsonlog_span_publisher.publisher(log)
trace = p.tracer(publish)
trace_request = pf.request_tracer(trace)

# Init FastAPI.
app = fastapi.FastAPI()

# Add request tracing middleware.
app.middleware("http")(trace_request)


@p.traced(span_param="_")
def get_code(limit, _):
    time.sleep(random.randint(0, 300) / 100)
    return random.randint(0, limit)


@app.get("/inventory/{id}")
@p.traced
def dumbroute(span: pf.SpanFromScope, id: int, limit: int | None = 100):
    time.sleep(1)
    return [{"code": get_code(limit, _=span), "id": id, "b": limit}]
