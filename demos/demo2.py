import logging
import time
import uuid

from rholog import jsonformatter
from rholog import rholog as ρ


def step1():
    time.sleep(1)


def step2_substep1():
    time.sleep(1)


def step2_substep2(span: ρ.ISpan):
    span.event("long sleep time")
    time.sleep(4)
    span.event("done sleeping")
    1 / 0


def step2(span: ρ.ISpan):
    step2_substep1()
    time.sleep(1)
    step2_substep2(span)


def main(publisher, root_id):
    with ρ.trace(publisher, "main", root_id=root_id) as span:
        step1()
        step2(span)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo2")
    publisher = jsonformatter.JsonLogSpanPublisher(log)
    main(publisher, root_id)
