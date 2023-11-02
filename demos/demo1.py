import logging
import time
import uuid

from rholog import jsonformatter
from rholog import rholog as ρ


def step1(span: ρ.ISpan):
    with span.trace("step1") as span:
        time.sleep(1)


def step2_substep1(span: ρ.ISpan):
    with span.trace("step2_substep1") as span:
        time.sleep(1)


def step2_substep2(span: ρ.ISpan):
    with span.trace("step2_substep2") as span:
        span.event("long sleep time")
        time.sleep(4)
        span.event("done sleeping")


def step2(span: ρ.ISpan):
    with span.trace("step2") as span:
        step2_substep1(span)
        time.sleep(1)
        step2_substep2(span)


def main(publisher, root_id):
    with ρ.trace(publisher, "main", root_id=root_id) as span:
        step1(span)
        step2(span)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo1")
    publisher = jsonformatter.JsonLogSpanPublisher(log)
    main(publisher, root_id)
