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
    rows = db.get_rowcount();
    if rows == 0:
            print("\nNo Tasks Yet!")
            return

    result = db.get_tasks()

    for task_id, title, details in result:
        console.print(Panel(Text(details, justify="left"), padding=(1, 5),
                            title=str(task_id) + '. ' + title, title_align="left"))

def add_task():
    console.print("\n***Create New Task***")
    title = Prompt.ask("Title")
    details = Prompt.ask("Details")
    db.add_task(title,details)

def delete_task():
    console.print("\n***Delete a Task***")
    taskid = Prompt.ask("Task Id")
    db.delete_task(taskid)

CHOICES = ("0", "1", "2", "3")
def menu():
    while True:
        print("""
            [0] Quit
            [1] Add Task
            [2] View Tasks
            [3] Delete Task
            """
              )
        choice = IntPrompt.ask("Choice", choices=CHOICES, show_choices=False)
        match choice:
            case 1: add_task()
            case 2: view_tasks()
            case 3: delete_task()
            case 0: break

    # console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
    # print(f"ito napili mo loads {choice} {type(choice)}")


def main():
    menu()


if __name__ == '__main__':
    main()
