import logging
import time
import uuid

import rholog.jsonformatter
import rholog.jsonlog_span_publisher
import rholog.p as p


def step1(span: p.ISpan):
    with span("step1") as span:
        time.sleep(1)


def step2_substep1(span: p.ISpan):
    with span("step2_substep1") as span:
        time.sleep(1)


def step2_substep2(span: p.ISpan):
    with span("step2_substep2") as span:
        span.event("long sleep time")
        time.sleep(4)
        span.event("done sleeping")


def step2(span: p.ISpan):
    with span("step2") as span:
        step2_substep1(span)
        time.sleep(1)
        step2_substep2(span)


def main(trace: p.ITrace, root_id):
    with trace("main", root_id=root_id) as span:
        step1(span)
        step2(span)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    rholog.jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo1")
    publish = rholog.jsonlog_span_publisher.publisher(log)
    trace = p.tracer(publish)
    main(trace, root_id)
