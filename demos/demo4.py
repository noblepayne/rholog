import logging
import time
import uuid

from rholog import jsonformatter
from rholog import rholog as ρ


@ρ.traced(span_param="spam")
def substep_1(spam: ρ.ISpan):
    time.sleep(1)
    spam.event("inside substep_1")
    time.sleep(1)


@ρ.traced
def main(span: ρ.ISpan):
    with span.trace("subcomponent-1", {"param1": 12}) as span:
        span.event("I guess I still want to log?", {"warning": True})
        time.sleep(1)
        substep_1(span)
        time.sleep(1)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo4")
    publisher = jsonformatter.JsonLogSpanPublisher(log)
    with ρ.trace(publisher, "__main__", root_id=root_id) as span:
        main(span)
