# Libraries used
from turtle import left
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


def view_tasks(viewType="ALL"):
    match viewType:
        case "DAY":
            day = Prompt.ask("Deadline (YYYY-MM-DD)")
            result = db.get_tasks_day(day)
        case "MONTH":
            month = Prompt.ask("Deadline (YYYY-MM)")
            result = db.get_tasks_month(month)
        case _:
            result = db.get_tasks()

    if db.get_rowcount() == 0:
        console.print("\nNo Tasks Yet!")
        return

    for task_id, title, details, deadline, finished, name in result:
        info = Text(justify="left")
        info.append("Category: ", style="bold green")
        info.append(str(name))
        info.append(" | ")
        info.append("Deadline: ", style="bold green")
        info.append(str(deadline))
        info.append(" | ")
        info.append("Finished: ", style="bold green")
        info.append(str(bool(finished)))
        info.append("\n")
        info.append(details)

        console.print(
            Panel(
                info,
                padding=(1, 5),
                title="{}. {}".format(task_id, title),
                title_align="left",
                highlight=True,
                expand=False
            )
        )


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
    deadline = Prompt.ask("Deadline (YYYY-MM-DD hh:mm)")
    db.add_task(title, details, deadline)


def delete_task():
    console.print("\n***Delete a Task***")
    taskid = IntPrompt.ask("Task Id")
    db.delete_task(taskid)


def add_category():
    console.print("\n***Create New Category***")
    title = Prompt.ask("Name")
    details = Prompt.ask("Description")
    db.add_category(title, details)


def delete_category():
    console.print("\n***Delete a Category***")
    Id = IntPrompt.ask("Category Id")
    db.delete_category(Id)

def mark_as_done():
    console.print("\n***Mark Task as Done***")
    taskid = Prompt.ask("Task Id")
    db.mark_task_done(taskid)

def update_task():
    TASKCHOICES = [str(x) for x in range(4)]

    while True:
        console.print("""\n***Update a Task***
[0] Cancel Update
[1] Title only
[2] Details only
[3] Both""")
        holder = IntPrompt.ask("Choice", choices=TASKCHOICES, show_choices=False)

        match holder:
            case 0: 
                console.print("Update Cancelled!")
                break
            case 1: 
                task_title_only()
                break
            case 2: 
                task_details_only()
                break
            case 3: 
                task_both()
                break


def task_title_only():
    console.print("\n***Task to be Edited***")
    taskid = Prompt.ask("Task Id")
    newTitle = Prompt.ask("New Title")
    db.update_task_title(newTitle, taskid)

def task_details_only():
    console.print("\n***Task to be Edited***")
    taskid = Prompt.ask("Task Id")
    newDetails = Prompt.ask("New Details")
    db.update_task_details(newDetails, taskid)

def task_both():
    console.print("\n***Task to be Edited***")
    taskid = Prompt.ask("Task Id")
    newTitle = Prompt.ask("New Title")
    newDetails = Prompt.ask("New Details")
    db.update_task_both(newTitle, newDetails, taskid)

def update_category():
    CATEGORYCHOICES = [str(x) for x in range(4)]

    while True:
        console.print("""\n***Update a Category***
[0] Cancel Update
[1] Name only
[2] Description only
[3] Both""")
        holder = IntPrompt.ask("Choice", choices=CATEGORYCHOICES, show_choices=False)

        match holder:
            case 0: 
                console.print("Update Cancelled!")
                break
            case 1: 
                category_name_only()
                break
            case 2: 
                category_description_only()
                break
            case 3: 
                category_both()
                break


def category_name_only():
    console.print("\n***Category to be Edited***")
    categoryid = Prompt.ask("Category Id")
    newName = Prompt.ask("New Name")
    db.update_category_name(newName, categoryid)

def category_description_only():
    console.print("\n***Category to be Edited***")
    categoryid = Prompt.ask("Category Id")
    newDescription = Prompt.ask("New Description")
    db.update_category_Description(newDescription, categoryid)

def category_both():
    console.print("\n***Category to be Edited***")
    categoryid = Prompt.ask("Category Id")
    newTitle = Prompt.ask("New Title")
    newDescription = Prompt.ask("New Description")
    db.update_category_both(newTitle, newDescription, categoryid)

def add_task_to_category():
    console.print("\n***Add a Task to a Category***")
    taskid = Prompt.ask("Task Id")
    categoryid = Prompt.ask("Category Id")
    db.add_task_to_category(categoryid, taskid)


CHOICES = [str(x) for x in range(13)]
MAINMENUCOMMANDS = """[0] Quit
[1] Add Task
[2] View Tasks
[3] Delete Task
[4] Add Category
[5] View Categories
[6] Delete Category
[7] View Tasks (Day)
[8] View Tasks (Month)
[9] Mark Task as Done
[10] Update Task
[11] Update Category
[12] Add Task to Category
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
            case 7: view_tasks("DAY")
            case 8: view_tasks("MONTH")
            case 9: mark_as_done()
            case 10: update_task()
            case 11: update_category()
            case 12: add_task_to_category()
            case 0:
                db.close()
                console.print("Goodbye!")
                break

    # console.print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
    # print(f"ito napili mo loads {choice} {type(choice)}")


if __name__ == '__main__':
    menu()
