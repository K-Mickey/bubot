import logging

import conf


def get_logger(
    log_file: str, module_name: str, log_level: str = conf.LOG_LEVEL
) -> logging.Logger:

    handler = logging.FileHandler(conf.LOG_PATH / log_file)
    handler.setLevel(log_level)
    formatter = logging.Formatter(conf.LOG_FORMAT)
    handler.setFormatter(formatter)

    log = logging.getLogger(module_name)
    log.setLevel(log_level)
    log.addHandler(handler)
    return log


def init_logging() -> None:
    logging.basicConfig(
        level=conf.LOG_LEVEL,
        format=conf.LOG_FORMAT,
    )


def _make_log_dir() -> None:
    conf.LOG_PATH.mkdir(parents=True, exist_ok=True)


_make_log_dir()
