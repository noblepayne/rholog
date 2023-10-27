import logging
import time
import uuid

import rholog as ρ


# TODO: test kwargs, other names, etc.
@ρ.traced(span_param="spam")
def substep_1(spam: ρ.Span):
    time.sleep(1)
    spam.event("inside substep_1")
    time.sleep(1)


@ρ.traced
def main(span):
    with span.trace("subcomponent-1", {"param1": 12}) as span:
        span.event("I guess I still want to log?", level=logging.WARNING)
        time.sleep(1)
        substep_1(span)
        time.sleep(1)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    ρ.setup_logging(indent=2)
    log = logging.getLogger("demo3")
    with ρ.trace(log, "__main__", root_id=root_id) as span:
        main(span)
