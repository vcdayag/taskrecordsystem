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
        console.print("\nNo Tasks Yet!")
        return

    for task_id, title, details in result:
        console.print(Panel(Text(details, justify="left"), padding=(1, 5),
                            title="{}. {}".format(task_id, title), title_align="left"))

def view_tasks_day():
    day = Prompt.ask("Deadline (YYYY-MM-DD)")
    result = db.get_tasks_day(day)
    if db.get_rowcount() == 0:
        console.print("\nNo Tasks Yet!")
        return

    for task_id, title, details in result:
        console.print(Panel(Text(details, justify="left"), padding=(1, 5),
                            title="{}. {}".format(task_id, title), title_align="left"))

def view_tasks_month():
    month = Prompt.ask("Deadline (YYYY-MM-DD)")
    result = db.get_tasks_month(month)
    if db.get_rowcount() == 0:
        console.print("\nNo Tasks Yet!")
        return

    for task_id, title, details in result:
        console.print(Panel(Text(details, justify="left"), padding=(1, 5),
                            title="{}. {}".format(task_id, title), title_align="left"))

def view_categories():
    result = db.get_categories()
    if db.get_rowcount() == 0:
        console.print("\nNo Categories Yet!")
        return

    for category_id, name, description in result:
        console.print(Panel(Text(description, justify="left"), padding=(1, 5),
                            title="{}. {}".format(category_id, name), title_align="left"))


def add_task():
    console.print("\n***Create New Task***")
    title = Prompt.ask("Title")
    details = Prompt.ask("Details")
    deadline = Prompt.ask("Deadline (YYYY-MM-DD)")
    db.add_task(title, details,deadline)


def delete_task():
    console.print("\n***Delete a Task***")
    taskid = Prompt.ask("Task Id")
    db.delete_task(taskid)


def add_category():
    console.print("\n***Create New Category***")
    title = Prompt.ask("Name")
    details = Prompt.ask("Description")
    db.add_category(title, details)


def delete_category():
    console.print("\n***Delete a Category***")
    Id = Prompt.ask("Category Id")
    db.delete_category(Id)


CHOICES = [str(x) for x in range(9)]
MAINMENUCOMMANDS = """[0] Quit
[1] Add Task
[2] View Tasks
[3] Delete Task
[4] Add Category
[5] View Categories
[6] Delete Category
[7] View Tasks (Day)
[8] View Tasks (Month)
"""


def menu():
    while True:
        console.print(Panel(Text(MAINMENUCOMMANDS, justify="left"), padding=(1, 1),
                            title="Main Menu", title_align="center", expand=False),)
        choice = IntPrompt.ask("Choice", choices=CHOICES, show_choices=False)
        match choice:
            case 1: add_task()
            case 2: view_tasks()
            case 3: delete_task()
            case 4: add_category()
            case 5: view_categories()
            case 6: delete_category()
            case 7: view_tasks_day()
            case 8: view_tasks_month()
            case 0:
                console.print("Goodbye!")
                break

    # console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
    # print(f"ito napili mo loads {choice} {type(choice)}")

if __name__ == '__main__':
    menu()