import logging
from rich.logging import RichHandler

def logger(l="INFO"):
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=l, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger("rich")


if __name__ == '__main__':
    log = logger()
    log.info("Hello, World!")
    log.debug("this is debug")