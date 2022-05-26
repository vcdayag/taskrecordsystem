import database as db

from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

console = Console()
lorem = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit, tenetur error, harum nesciunt ipsum debitis quas aliquid."


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
    [console.print(Panel(Text(lorem, justify="left"), padding=(1, 5),
                   title=x, title_align="left")) for x in db.test_data()]


if __name__ == '__main__':
    main()
