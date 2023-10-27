import contextlib
import datetime
import inspect
import functools
import json
import logging
import sys
import time
import traceback
import typing
import uuid


DEFAULT_FIELDS = {
    "name": "name",
    "levelname": "levelname",
    # TODO: how to handle the... special handling of msg/message?
    "message": "message",
    "timestamp": "asctime",
}


def available_logrecord_fields() -> dict:
    fmt = logging.Formatter()
    rec = logging.LogRecord("name", 10, "pathname", 13, "msg", (), None)
    setattr(fmt, "usesTime", lambda: True)
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


def add_context(logger, context, adapter=None):
    if adapter is None:
        adapter = logging.LoggerAdapter
    old_context = getattr(logger, "extra", {})
    new_context = {**old_context, **context}
    base_log = base_logger(logger)
    return adapter(base_log, new_context)


@contextlib.contextmanager
def context(logger, context, adapter=None):
    base_log = base_logger(logger)
    existing_extra = getattr(logger, "extra", {})
    newlog = add_context(logger, context, adapter)
    yield newlog
    newlog.logger = base_log
    newlog.extra = existing_extra


@contextlib.contextmanager
def trace(
    logger: typing.Union[logging.LoggerAdapter, "Span"],
    name: str,
    context: typing.Mapping | None = None,
    root_id: str | None = None,
    level: int | None = None,
):
    if level is None:
        # TODO: Useful to have a TRACE level?
        level = logging.INFO
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

    context_log = add_context(logger, new_context, Span)

    exc = None
    status = "OK"
    start = time.time()
    try:
        yield context_log
    except Exception as e:
        exc = e
        status = "ERROR"
    end = time.time()

    duration = end - start
    final_trace = {
        "trace": True,
        "message": name,
        "status": status,
        "start_time": start,
        "end_time": end,
        "duration": duration,
    }
    if exc is not None:
        final_trace["exception"] = str(exc)
        final_trace["traceback"] = "".join(traceback.format_exception(exc))
        context_log.error(final_trace)
    else:
        context_log.log(level, final_trace)

    context_log.logger = base_log
    context_log.extra = existing_extra
    if exc is not None:
        raise exc


def event(logger, name, context=None, root_id=None, level=None):
    with trace(logger, name, context, root_id, level=level):
        pass


def traced(fn=None, span_param="span"):
    def _traced(fn):
        argspec = inspect.getfullargspec(fn)

        @functools.wraps(fn)
        def _inner(*args, **kwargs):
            span_type = None
            if span_param in set(argspec.args):
                arg_idx = {arg: idx for idx, arg in enumerate(argspec.args)}
                if span_param in arg_idx:
                    span_idx = arg_idx[span_param]
                    span = args[span_idx]
                    span_type = "args"
                else:
                    raise ValueError(f"Can't find span {span_param} in passed args!")
            elif span_param in kwargs:
                span = kwargs[span_param]
                span_type = "kwargs"
            else:
                raise ValueError(f"Can't find span {span_param} in args or kwargs.")

            with span.trace(fn.__qualname__) as newspan:
                if span_type == "args":
                    args = tuple(
                        newspan if idx == span_idx else arg
                        for idx, arg in enumerate(args)
                    )
                elif span_type == "kwargs":
                    kwargs[span_param] = newspan
                else:
                    raise ValueError(f"Unknown span_type {span_type}.")
                return fn(*args, **kwargs)

        return _inner

    if fn is None:
        return _traced
    return _traced(fn)


class Span(logging.LoggerAdapter):
    # TODO: explore not using LoggerAdapater.
    # TODO: explore reimplemeting/overriding log method.
    def trace(self, name, context=None, root_id=None, level=None):
        return trace(self, name, context, root_id, level)

    def event(self, name, context=None, root_id=None, level=None):
        return event(self, name, context, root_id, level)
