# Libraries used
from rich.padding import Padding
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.prompt import Prompt, IntPrompt
from rich.console import Console
# Custom modules
import database
from logger import logger

console = Console()
log = logger()
db = database.DATABASE()



def view_tasks():
    result = db.get_tasks()
    if db.get_rowcount() == 0:
        log.debug("walang laman")
        return

    for title, details in result:
        console.print(Panel(Text(details, justify="left"), padding=(1, 5),
                            title=title, title_align="left"))


CHOICES = ("0", "1", "2", "3")


def menu():
    while True:
        print("""
            [0] Quit
            [1] Add Task
            [2] View Task
            [3] Delete Task
            """
              )
        choice = IntPrompt.ask("Choice", choices=CHOICES, show_choices=False)
        match choice:
            case 1: view_tasks()
            case 2: view_tasks()
            case 0: break

    # console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
    # print(f"ito napili mo loads {choice} {type(choice)}")


def main():
    menu()


if __name__ == '__main__':
    main()
