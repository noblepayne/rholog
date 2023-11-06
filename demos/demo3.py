import logging
import time
import uuid

import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p


# TODO: test kwargs, other names, etc.
@p.traced
def substep_1(span: p.ISpan):
    span.event("inside substep_1")


def main(trace: p.ITrace, root_id):
    with trace("main", root_id=root_id) as span:
        with span("subcomponent-1", {"param1": 12}) as span:
            span.event("I guess I still want to log?", {"warning": True})
            time.sleep(1)
            substep_1(span)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    rholog.jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo1")
    publish = rholog.jsonlog_span_publisher.publisher(log)
    trace = p.tracer(publish)
    main(trace, root_id)
