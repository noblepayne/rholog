import collections.abc
import contextlib
import functools
import inspect
import time
import traceback
import types
import typing
import uuid

import typing_extensions

# Base Schema


class SpanContext(typing_extensions.TypedDict, total=False):
    root_id: typing_extensions.Required[str]


class SpanTags(typing_extensions.TypedDict, total=False):
    name: typing_extensions.Required[str]
    span_id: typing_extensions.Required[str]
    parent_id: str


class SpanData(typing_extensions.TypedDict):
    context: SpanContext
    tags: SpanTags


@typing.runtime_checkable
class ISpan(typing.Protocol):
    def __call__(
        self: typing_extensions.Self,
        name: str,
        tags: typing.Mapping | None = None,
        context: typing.Mapping | None = None,
    ) -> contextlib.AbstractContextManager["ISpan"]:
        ...

    @staticmethod
    def update(
        name: str | None = None,
        tags: typing.Mapping | None = None,
        context: typing.Mapping | None = None,
    ) -> None:
        ...

    @staticmethod
    def event(
        name: str,
        tags: typing.Mapping | None = None,
        context: typing.Mapping | None = None,
    ) -> None:
        ...


@typing.runtime_checkable
class ITrace(typing.Protocol):
    @staticmethod
    def __call__(
        name: str,
        tags: typing.Mapping | None = None,
        context: typing.Mapping | None = None,
        root_id: str | None = None,
        parent_id: str | None = None,
    ) -> contextlib.AbstractContextManager[ISpan]:
        ...


# Publishers


Publisher = typing.Callable[[SpanData], None]


@typing.runtime_checkable
class IPublisher(typing.Protocol):
    @staticmethod
    def publisher(*args, **kwargs) -> Publisher:
        ...


# Implementation


def _find_filename_and_lineno(filename, lineno, currentframe: types.FrameType):
    previous_frame = currentframe.f_back
    while previous_frame and (
        previous_frame.f_globals.get("__name__") in {"contextlib", __name__}
    ):
        previous_frame = previous_frame.f_back
    if previous_frame:
        filename = previous_frame.f_code.co_filename
        lineno = previous_frame.f_lineno
        return filename, lineno
    return filename, lineno


def tracer(publish: Publisher):
    @contextlib.contextmanager
    def trace(
        name: str,
        tags: typing.Mapping | None = None,
        context: typing.Mapping | None = None,
        root_id: str | None = None,
        parent_id: str | None = None,
    ) -> collections.abc.Generator[ISpan, None, None]:
        # Init user tags and context.
        if tags is None:
            tags = {}
        if context is None:
            context = {}
        # Capture filename and lineno of caller.
        filename = tags.get("filename")
        lineno = tags.get("lineno")
        if not (filename or lineno) and (currentframe := inspect.currentframe()):
            filename, lineno = _find_filename_and_lineno(filename, lineno, currentframe)
        # Setup ID.
        span_id = uuid.uuid4().hex
        root_id = root_id or span_id
        new_context = {"root_id": root_id, **context}
        new_tags: dict = {
            "name": name,
            "span_id": span_id,
        }
        if parent_id is not None:
            new_tags["parent_id"] = parent_id
        new_tags["filename"] = filename
        new_tags["lineno"] = lineno
        new_tags.update(tags)

        class Trace:
            @contextlib.contextmanager
            def __call__(
                self: typing_extensions.Self,
                name: str,
                tags: typing.Mapping | None = None,
                context: typing.Mapping | None = None,
            ):
                if context is None:
                    context = {}
                if tags is None:
                    tags = {}
                with trace(
                    name=name,
                    tags=tags,
                    context={**new_context, **context},
                    root_id=root_id,
                    parent_id=span_id,
                ) as subtrace:
                    yield subtrace
                    setattr(subtrace, "__call__", self.__call__)
                    setattr(subtrace, "update", self.update)
                    setattr(subtrace, "event", self.event)

            @staticmethod
            def update(
                name: str | None = None,
                tags: typing.Mapping | None = None,
                context: typing.Mapping | None = None,
            ):
                if name is not None:
                    new_tags["name"] = name
                if tags is not None:
                    new_tags.update(tags)
                if context is not None:
                    new_context.update(context)

            @staticmethod
            def event(
                name: str,
                tags: typing.Mapping | None = None,
                context: typing.Mapping | None = None,
            ):
                with trace(
                    name=name,
                    tags={"event": True, **(tags or {})},
                    context={**new_context, **(context or {})},
                    root_id=root_id,
                    parent_id=span_id,
                ):
                    # TODO: OTEL style? Plays less nicely with log output...
                    return None

        # Exec code under trace.
        exc = None
        start = time.time()
        try:
            yield Trace()
        except Exception as e:
            exc = e
        end = time.time()
        # Wrap-up.
        post_trace_tags: dict = {
            "start_time": start,
            "end_time": end,
            "duration": end - start,
        }
        # Handle exceptions.
        if exc is not None:
            post_trace_tags["status"] = "ERROR"
            post_trace_tags["exception"] = str(exc)
            post_trace_tags["traceback"] = "".join(traceback.format_exception(exc))
        # Publish.
        new_tags.update(post_trace_tags)
        new_span: SpanData = {
            "context": typing.cast(SpanContext, new_context),
            "tags": typing.cast(SpanTags, new_tags),
        }
        publish(new_span)
        # Raise.
        if exc is not None:
            # TODO: how to reduce noise in logs?
            raise exc

    return trace


P = typing.ParamSpec("P")
R = typing.TypeVar("R")
FN = typing.Callable[P, R]


@typing.overload
def traced(fn: None = None, *, span_param: str) -> typing.Callable[[FN], FN]:
    pass


@typing.overload
def traced(fn: FN, *, span_param: None = None) -> FN:
    pass


def traced(
    fn: FN | None = None, *, span_param: str | None = None
) -> typing.Union[FN, typing.Callable[[FN], FN]]:
    final_span_param = span_param or "span"

    def _traced(fn: typing.Callable[P, R]) -> typing.Callable[P, R]:
        argspec = inspect.getfullargspec(fn)
        all_args = set(argspec.args).union(set(argspec.kwonlyargs))
        if final_span_param not in all_args:
            raise ValueError(f"Can't find span {final_span_param} in args or kwargs.")
        arg_idx = {arg: idx for idx, arg in enumerate(argspec.args)}

        @functools.wraps(fn)
        def _inner(*args: P.args, **kwargs: P.kwargs) -> R:
            span: ISpan
            if final_span_param in kwargs:
                found_span = kwargs[final_span_param]
                assert isinstance(found_span, ISpan)
                span = found_span
            else:
                span_idx = arg_idx[final_span_param]
                found_span = args[span_idx]
                assert isinstance(found_span, ISpan)
                span = found_span

            with span(
                f"{fn.__module__}.{fn.__qualname__}",
                {
                    "module": fn.__module__,
                    "function": fn.__qualname__,
                    "filename": fn.__code__.co_filename,
                    "lineno": fn.__code__.co_firstlineno,
                },
            ) as newspan:
                old_call = span.__call__
                old_update = span.update
                old_event = span.event
                setattr(span, "__call__", newspan.__call__)
                setattr(span, "update", newspan.update)
                setattr(span, "event", newspan.event)
                result = fn(*args, **kwargs)
                setattr(span, "__call__", old_call)
                setattr(span, "update", old_update)
                setattr(span, "event", old_event)
                return result

        return _inner

    if fn is None:
        return _traced
    return _traced(fn)
