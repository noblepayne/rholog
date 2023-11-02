import datetime
import json
import logging
import sys
import typing

from . import rholog

DEFAULT_FIELDS = {
    "name": "name",
    "levelname": "levelname",
    # TODO: how to handle the... special handling of msg/message?
    # TODO: can't rename/alias message.
    "message": "message",
    "timestamp": "asctime",
}


def available_logrecord_fields() -> dict:
    fmt = logging.Formatter()
    rec = logging.LogRecord("name", 10, "pathname", 13, "msg", (), None)
    setattr(fmt, "usesTime", lambda: True)
    fmt.format(rec)
    return rec.__dict__


class JSONFormatter(logging.Formatter):
    def __init__(self, *args, fields=None, indent=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fields is None:
            fields = DEFAULT_FIELDS
        timestamp_keys = {k for k in fields if fields[k] == "asctime"}
        if len(timestamp_keys) == 1:
            timestamp_key = timestamp_keys.pop()
            fields.pop(timestamp_key, None)
            self.timestamp_key = timestamp_key
        else:
            self.timestamp_key = None
        self.fields = fields
        self.indent = indent
        self.base_fields = available_logrecord_fields().keys()

    def formatTime(self, record, datefmt=None):
        # TODO: support datefmt?
        return (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone(datetime.timezone.utc)
            .isoformat()
        )

    def usesTime(self):
        return self.timestamp_key is not None

    # TODO: support additional encodings?
    # TODO: paramaterize json
    def format(self, record):
        super().format(record)
        extra = {
            k: record.__dict__.get(k)
            for k in record.__dict__
            if k not in self.base_fields
        }
        nested = record.msg if isinstance(record.msg, typing.Mapping) else {}
        chosen_fields = {k: record.__dict__.get(v) for k, v in self.fields.items()}
        if nested:
            chosen_fields.pop("message", None)
        final = {**chosen_fields, **nested, **extra}
        if self.timestamp_key is not None:
            final[self.timestamp_key] = record.asctime
        return json.dumps(final, indent=self.indent)


def log_json_to_stdout(level=logging.DEBUG, fields=None, indent=None, clear=True):
    root = logging.getLogger()
    if clear:
        for handler in root.handlers:
            root.removeHandler(handler)
    root.setLevel(level)
    stdout = logging.StreamHandler(sys.stdout)
    formatter = JSONFormatter(fields=fields, indent=indent)
    stdout.setFormatter(formatter)
    root.addHandler(stdout)


class JsonLogSpanPublisher(rholog.IPublish):
    log: logging.Logger

    def __init__(self, log: logging.Logger) -> None:
        self.log = log

    def publish(self, span: dict) -> None:
        if span.get("status") == "ERROR":
            level = logging.ERROR
        elif span.get("exception"):
            level = logging.ERROR
        elif span.get("error"):
            level = logging.ERROR
        elif span.get("warning"):
            level = logging.WARNING
        elif span.get("debug"):
            level = logging.DEBUG
        else:
            level = logging.INFO

        span["message"] = "TRACE"

        self.log.log(level, span)
