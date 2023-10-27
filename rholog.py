import contextlib
import datetime
import json
import logging
import sys
import time
import typing
import uuid


DEFAULT_FIELDS = {
    "name": "name",
    "levelname": "levelname",
    "message": "message",
    "timestamp": "asctime",
}


def available_logrecord_fields() -> dict:
    fmt = logging.Formatter()
    rec = logging.LogRecord("name", "level", "pathname", "lineno", "msg", (), None)
    fmt.usesTime = lambda: True
    fmt.format(rec)
    return rec.__dict__


class BasicJSONFormatter(logging.Formatter):
    def __init__(self, *args, fields=None, **kwargs):
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
        self.base_fields = available_logrecord_fields().keys()

    def formatTime(self, record, datefmt=None):
        return (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone(datetime.timezone.utc)
            .isoformat()
        )

    def usesTime(self):
        return self.timestamp_key is not None

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
        return json.dumps(final, indent=2)


def setup_logging(level=logging.DEBUG):
    root = logging.getLogger()
    [root.removeHandler(handler) for handler in root.handlers]
    root.setLevel(level)
    stdout = logging.StreamHandler(sys.stdout)
    # TODO: needed? not needed?
    # stdout.setLevel(level)
    formatter = BasicJSONFormatter()
    stdout.setFormatter(formatter)
    root.addHandler(stdout)


def base_logger(logger):
    base = logger
    while isinstance(base, logging.LoggerAdapter):
        base = base.logger
    return base


def add_context(logger, context):
    old_context = getattr(logger, "extra", {})
    new_context = {**old_context, **context}
    base_log = base_logger(logger)
    return logging.LoggerAdapter(base_log, new_context)


@contextlib.contextmanager
def context(logger, context):
    base_log = base_logger(logger)
    existing_extra = getattr(logger, "extra", {})
    newlog = add_context(logger, context)
    yield newlog
    newlog.logger = base_log
    newlog.extra = existing_extra


@contextlib.contextmanager
def trace(logger, name, context=None, root_id=None):
    if context is None:
        context = {}
    base_log = base_logger(logger)
    existing_extra = getattr(logger, "extra", {})

    trace_id = uuid.uuid4().hex
    parent_id = existing_extra.get("trace_id")
    if root_id is None:
        root_id = existing_extra.get("root_id", trace_id)

    new_context = {"root_id": root_id}
    if parent_id is not None:
        new_context["parent_id"] = parent_id
    new_context["trace_id"] = trace_id
    new_context.update(context)

    context_log = add_context(logger, new_context)

    start = time.time()
    yield context_log
    end = time.time()

    duration = end - start
    context_log.info({"message": "TRACE", "trace": name, "duration": duration})

    context_log.logger = base_log
    context_log.extra = existing_extra

def log(logger, name, context=None, root_id=None):
    with trace(logger, name, context, root_id) as tr:
        pass