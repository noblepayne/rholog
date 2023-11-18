import logging
import sys

from . import p


def publisher(log: logging.Logger) -> p.Publisher:
    def publish(span: p.SpanData) -> None:
        record = {**span["context"], **span["tags"]}
        # record["span_name"] = record.pop("name", "")
        if record.get("status") == "ERROR":
            level = logging.ERROR
        elif record.get("exception"):
            level = logging.ERROR
        elif record.get("error"):
            level = logging.ERROR
        elif record.get("warning"):
            level = logging.WARNING
        elif record.get("debug"):
            level = logging.DEBUG
        else:
            level = logging.INFO

        record["message"] = "TRACE"

        log.log(level, record)

    return publish


# TODO: Move to tests.
assert isinstance(sys.modules[__name__], p.IPublisher)
