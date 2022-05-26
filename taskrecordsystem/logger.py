import logging
from rich.logging import RichHandler


def logger(l="DEBUG"):
    logging.basicConfig(
        level=l, format="%(message)s", handlers=[RichHandler()]
    )
    return logging.getLogger("rich")


if __name__ == '__main__':
    log = logger()
    log.debug("this is debug")
    log.info("Hello, World!")
    log.error("this is an error")
