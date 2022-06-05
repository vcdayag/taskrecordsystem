# Libraries used
from turtle import left
from rich.table import Table
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
        log.info("\n[bold orange3]No Tasks Yet!\n", extra={"markup": True})
        return

    for task_id, title, details, deadline, finished, category_id, name in result:
        info = Text(justify="left")
        info.append("Category Id: ", style="bold green")
        info.append(str(category_id))
        info.append(" | ")
        info.append("Category Name: ", style="bold green")
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
            ),"\n"
        )


def view_categories():
    result = db.get_categories()
    if db.get_rowcount() == 0:
        log.info("\n[bold orange3]No Categories Yet!\n", extra={"markup": True})
        return
    
    table = Table(
                  title="\nCategories",
                  header_style="bold green",
                  leading=1,
                  title_justify="center",
                  safe_box=True,
                  row_styles=["","dim"],
                  )
    table.add_column("Category Id",justify="center")
    table.add_column("Name",justify="center")
    table.add_column("Description",justify="center")
    
    for category_id, name, description in result:
        table.add_row(str(category_id),name,description)
        
    
    console.print(table,"\n")


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

def mark_task_done():
    console.print("\n***Mark Task as Done***")
    taskid = Prompt.ask("Task Id")
    db.mark_task_done(taskid)

TASKCHOICES = [str(x) for x in range(4)]
TASKCHOICESMESSAGE = """
***Update a Task***
[0] Cancel Update
[1] Title only
[2] Details only
[3] Both"""

def update_task():
    console.print("\n***Task to be Edited***")
    taskid = IntPrompt.ask("Task Id")
    
    result = db.get_tasks_one(taskid)

    if db.get_rowcount() == 0:
        log.info("\n[bold orange3]Task does not exist!\n", extra={"markup": True})
        return

    for task_id, title, details, deadline, finished, category_id, name in result:
        print(f"\nTask id: {task_id}")
        print(f"Task Title: {title}")
        print(f"Task Details: {details}")
        print(f"Task Deadline: {deadline}")
        print(f"Task Finished: {finished}")
        print(f"Task Category id: {category_id}")
        print(f"Task Category: {name}")
    
    console.print("\n***Just Press enter if you will not change the value***")
    newTitle = Prompt.ask("New Title")
    newDetails = Prompt.ask("New Details")
    newDeadline = Prompt.ask("New Deadline (YYYY-MM-DD hh:mm)")
    newFinished = Prompt.ask("New Finished",choices=["","Yes","No"])
    newCategory = Prompt.ask("New Category")
    for task_id, title, details, deadline, finished, category_id, name in result:
        if newTitle == "":
            newTitle = title
        if newDetails == "":
            newDetails = details
        if newDeadline == "":
            newDeadline = deadline
        if newFinished == "":
            newFinished = finished
        elif newFinished == "Yes":
            newFinished = 1
        elif newFinished == "No":
            newFinished = 0
        
        if newCategory == "":
            newCategory = category_id
        
        try:
            newCategory = int(newCategory)
        except ValueError as e:
            log.error("\n[bold red] Invalid Category Id%s\n", extra={"markup": True})
            return
        
    
    db.update_task_whole(taskid,newTitle,newDetails,newDeadline,newFinished,newCategory)

CATEGORYCHOICES = [str(x) for x in range(4)]
CATEGORYMESSAGES = """
***Update a Category***
[0] Cancel Update
[1] Name only
[2] Description only
[3] Both"""

def update_category():

    console.print(CATEGORYMESSAGES)
    holder = IntPrompt.ask("Choice", choices=CATEGORYCHOICES, show_choices=False)

    match holder:
        case 0: 
            log.info("\n[bold orange3]Update Cancelled!\n", extra={"markup": True})
        case 1: 
            category_name_only()
        case 2: 
            category_description_only()
        case 3: 
            category_both()


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
                            title="[bold blue]Task Record System", title_align="center", expand=False),)
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
            case 9: mark_task_done()
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
