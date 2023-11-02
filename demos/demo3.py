import logging
import time
import uuid

from rholog import jsonformatter
from rholog import rholog as ρ


# TODO: test kwargs, other names, etc.
@ρ.traced
def substep_1(span: ρ.ISpan):
    span.event("inside substep_1")


def main(publisher, root_id):
    with ρ.trace(publisher, "main", root_id=root_id) as span:
        with span.trace("subcomponent-1", {"param1": 12}) as span:
            span.event("I guess I still want to log?", {"warning": True})
            time.sleep(1)
            substep_1(span)


if __name__ == "__main__":
    root_id = uuid.uuid4().hex
    jsonformatter.log_json_to_stdout(indent=2)
    log = logging.getLogger("demo3")
    publisher = jsonformatter.JsonLogSpanPublisher(log)
    main(publisher, root_id)
