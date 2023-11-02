import contextlib
import functools
import inspect
import logging
import time
import traceback
import typing
import uuid


# TODO: needed?
def _base_logger(logger):
    base = logger
    while isinstance(base, logging.LoggerAdapter):
        base = base.logger
    return base


def _add_context(logger, context, adapter=None):
    if adapter is None:
        adapter = logging.LoggerAdapter
    old_context = getattr(logger, "extra", {})
    new_context = {**old_context, **context}
    base_log = _base_logger(logger)
    return adapter(base_log, new_context)


@contextlib.contextmanager
def context(logger, context, adapter=None):
    base_log = _base_logger(logger)
    existing_extra = getattr(logger, "extra", {})
    newlog = _add_context(logger, context, adapter)
    yield newlog
    newlog.logger = base_log
    newlog.extra = existing_extra


@contextlib.contextmanager
def trace(
    logger: logging.Logger,
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
    base_log = _base_logger(logger)
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

    context_log = _add_context(logger, new_context, Span)

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
