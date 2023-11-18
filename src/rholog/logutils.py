import contextlib
import logging


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


def odd(n: int) -> bool:
    return bool(n % 2)


def banner(text: str, buffer_char="~", length=88) -> str:
    borderless_length = length - 4  # "# "
    text_length = len(text) + 2  # " {text} "

    buffer_length = borderless_length - text_length
    left_buffer_length = right_buffer_length = buffer_length // 2
    if odd(buffer_length):
        if odd(text_length):
            right_buffer_length += 1
        else:
            left_buffer_length += 1

    assert (
        borderless_length == left_buffer_length + text_length + right_buffer_length
    ), f"{borderless_length} != {left_buffer_length} + {text_length} + {right_buffer_length}"
    banner = (
        f"# {left_buffer_length*buffer_char} {text} {right_buffer_length*buffer_char} #"
    )
    assert len(banner) == length, banner
    return banner


def _test():
    for wordl in range(1, 50):
        for length in range(80, 90):
            print(banner(wordl * "X", length=length))
    print()
    for length in range(80, 99):
        print(length)
        for wordl in range(1, 50):
            print(banner(wordl * "X", length=length))
