import logging
from rich.logging import RichHandler


def logger(l="INFO"):
    if l == "INFO":
        logging.basicConfig(
            level=l, format="%(message)s", handlers=[RichHandler(show_time=False, show_level=False, show_path=False)]
        )
    elif l == "DEBUG":
        logging.basicConfig(
            level=l, format="%(message)s", handlers=[RichHandler()]
        )
    return logging.getLogger("rich")


if __name__ == '__main__':
    log = logger()
    log.debug("this is debug")
    log.info("[bold green]Hello, World!", extra={"markup": True})
    log.error("[bold red]this is an error", extra={"markup": True})
    # log.info("Hello, World!")
