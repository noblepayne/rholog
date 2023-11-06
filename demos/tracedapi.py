import logging
import random
import typing

import fastapi

import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p

rholog.jsonformatter.log_json_to_stdout(indent=2)
log = logging.getLogger("fastapi")
publish = rholog.jsonlog_span_publisher.publisher(log)
trace = p.tracer(publish)

app = fastapi.FastAPI()


@app.middleware("http")
async def start_a_trace(request: fastapi.Request, call_next):
    scope = request.scope

    span_name = f"{scope['method']} {scope['raw_path'].decode()}"
    with trace(
        span_name,
        tags={
            "http.method": request.method,
            "http.url": request.url,
            "http.raw_path": request.scope["raw_path"],
            "http.path_params": request.path_params,
            "http.query_params": request.query_params,
            "http.host": request.client.host if request.client else None,
            "http.port": request.client.port if request.client else None,
        },
    ) as span:
        request.scope["span"] = span
        response = await call_next(request)
        route: fastapi.routing.APIRoute | None = request.scope.get("route")
        tag_updates = {"status_code": response.status_code}
        if route:
            tag_updates["name"] = route.unique_id
            tag_updates["http.path"] = route.path
        else:
            tag_updates["http.route.missing"] = True
        span.update(tags=tag_updates)
        return response


def span_from_scope(request: fastapi.Request) -> p.ISpan:
    return request.scope["span"]


SpanFromScope = typing.Annotated[p.ISpan, fastapi.Depends(span_from_scope)]


@p.traced
def get_code(span):
    return random.randint(0, 100)


@app.get("/{a}")
@p.traced
def dumbroute(span: SpanFromScope, a: int, b: str):
    return [{"code": get_code(span), "a": a, "b": b}]
