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
