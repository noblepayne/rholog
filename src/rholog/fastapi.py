import typing

import fastapi

import rholog.p as p


def request_tracer(trace: p.ITrace):
    async def trace_request(request: fastapi.Request, call_next):
        scope = request.scope

        span_name = f"{scope['method']} {scope['raw_path'].decode()}"
        with trace(
            span_name,
            tags={
                "http.method": request.method,
                "http.url": request.url,
                "http.raw_path": request.scope["raw_path"],
                "http.query_params": dict(request.query_params),
                "http.host": request.client.host if request.client else None,
                "http.port": request.client.port if request.client else None,
            },
        ) as span:
            request.scope["span"] = span
            response = await call_next(request)
            route: fastapi.routing.APIRoute | None = request.scope.get("route")
            tag_updates = {
                "http.status_code": response.status_code,
                "http.path_params": request.path_params,
            }
            if route:
                tag_updates["name"] = route.unique_id
                tag_updates["http.path"] = route.path
            else:
                tag_updates["http.route.missing"] = True
            span.update(tags=tag_updates)
            return response

    return trace_request


def span_from_scope(request: fastapi.Request) -> p.ISpan:
    return request.scope["span"]


SpanFromScope = typing.Annotated[p.ISpan, fastapi.Depends(span_from_scope)]
