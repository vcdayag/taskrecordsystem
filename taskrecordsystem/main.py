import database as db

from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console()

def menu():
    print("""
          [1] Add Task
          [2] View Task
          [3] Delete Task
          """
          )
    CHOICES = ("1","2","3")
    choice = IntPrompt.ask("Choice",choices=CHOICES,show_choices=False)
    # console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
    print(f"ito napili mo loads {choice} {type(choice)}")


def main():
    while True:
        menu()
    [console.print(Panel(Text("body text", justify="left"), padding=(1, 5),
                   title=x, title_align="left")) for x in db.test_data()]


if __name__ == '__main__':
    main()
