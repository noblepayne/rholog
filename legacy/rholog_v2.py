import contextlib
import functools
import inspect
import time
import traceback
import typing
import uuid

from typing_extensions import Self


@typing.runtime_checkable
class ISpan(typing.Protocol):
    def add_context(self, context: dict) -> None:
        ...

    @contextlib.contextmanager
    def trace(
        self,
        name: str,
        context: dict | None = None,
        root_id: str | None = None,
    ) -> typing.Generator[Self, None, None]:
        ...

    def event(
        self,
        name: str,
        context: dict | None = None,
        root_id: str | None = None,
    ) -> None:
        ...


@typing.runtime_checkable
class IPublish(typing.Protocol):
    def publish(self, span: dict) -> None:
        ...


class Span(ISpan):
    __slots__ = ["publisher", "name", "context"]
    publisher: IPublish
    name: str
    context: dict

    def __init__(self, publisher: IPublish, name=None, context=None):
        self.publisher = publisher
        if name is None:
            name = ""
        self.name = name
        if context is None:
            context = {}
        self.context = context

    def add_context(self, context: dict) -> None:
        self.context.update(context)

    @contextlib.contextmanager
    def trace(self, name: str, context: dict | None = None, root_id: str | None = None):
        # Init user context.
        if context is None:
            context = {}
        # Capture filename and lineno of caller.
        filename = context.get("filename")
        lineno = context.get("lineno")
        if not (filename or lineno):
            currentframe = inspect.currentframe()
            if currentframe:
                previous_frame = currentframe.f_back
                while previous_frame and (
                    previous_frame.f_globals.get("__name__") in {"contextlib", __name__}
                ):
                    previous_frame = previous_frame.f_back
                if previous_frame:
                    filename = previous_frame.f_code.co_filename
                    lineno = previous_frame.f_lineno
        # Store name and context.
        existing_name = self.name
        existing_context = self.context
        # Setup IDs.
        trace_id = uuid.uuid4().hex
        parent_id = existing_context.get("trace_id")
        if root_id is None:
            root_id = existing_context.get("root_id", trace_id)
        else:
            # TODO: cleanup, check.
            parent_id = None
        # Setup new context.
        new_context = {"name": name, "root_id": root_id}
        if parent_id is not None:
            new_context["parent_id"] = parent_id
        new_context["trace_id"] = trace_id
        new_context["filename"] = filename
        new_context["lineno"] = lineno
        # Add user context.
        new_context.update(context)
        # Set current cotext.
        new_span = Span(self.publisher, name=name, context=new_context)
        # TODO: issues with this optimization? Async? Multiple routes?
        # self.context = new_context
        # Exec code under trace.
        exc = None
        status = "OK"
        start = time.time()
        try:
            # yield self
            yield new_span
        except Exception as e:
            exc = e
            status = "ERROR"
        end = time.time()
        # Wrap-up.
        duration = end - start
        post_trace = {
            "status": status,
            "start_time": start,
            "end_time": end,
            "duration": duration,
        }
        # Handle exceptions.
        if exc is not None:
            post_trace["exception"] = str(exc)
            post_trace["traceback"] = "".join(traceback.format_exception(exc))
        # Publish.
        new_span.context.update(post_trace)
        new_span.publisher.publish(new_span.context)
        # Restore.
        new_span.name = existing_name
        new_span.context = existing_context
        # Raise.
        if exc is not None:
            raise exc

    def event(
        self, name: str, context: dict | None = None, root_id: str | None = None
    ) -> None:
        with self.trace(name, context, root_id):
            pass


def trace(
    publisher: IPublish,
    name: str,
    context: dict | None = None,
    root_id: str | None = None,
):
    return Span(publisher).trace(name, context, root_id)


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

            with span.trace(
                f"{fn.__module__}.{fn.__qualname__}",
                {
                    "module": fn.__module__,
                    "function": fn.__qualname__,
                    "filename": fn.__code__.co_filename,
                    "lineno": fn.__code__.co_firstlineno,
                },
            ) as newspan:
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
