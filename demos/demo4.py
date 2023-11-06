import logging
import time
import uuid

import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p


@p.traced(span_param="spam")
def substep_1(spam: p.ISpan):
    time.sleep(1)
    spam.event("inside substep_1")
    time.sleep(1)


@p.traced
def main(span: p.ISpan):
    with span("subcomponent-1", {"param1": 12}) as span:
        span.event("I guess I still want to log?", {"warning": True})
        time.sleep(1)
        substep_1(span)
        time.sleep(1)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    rholog.jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo1")
    publish = rholog.jsonlog_span_publisher.publisher(log)
    trace = p.tracer(publish)
    with trace("__main__", root_id=root_id) as span:
        main(span)
