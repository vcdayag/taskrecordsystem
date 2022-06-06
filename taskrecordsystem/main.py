# Libraries used
from turtle import left
from rich.table import Table
from rich.padding import Padding
from rich.prompt import Confirm
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
            returnMessage = "No tasks on that day"
        case "MONTH":
            month = Prompt.ask("Deadline (YYYY-MM)")
            result = db.get_tasks_month(month)
            returnMessage = "No tasks on that month"
        case "CATEGORY":
            if not view_categories():
                return
    
            console.print("\n***Press Enter to view tasks with no category***")
            categoryId = IntPrompt.ask(
                "Category Id", default=0, show_default=False)
            result = db.get_tasks_category(categoryId)
            returnMessage = "No tasks on that category"
        case _:
            result = db.get_tasks()
            returnMessage = "No tasks yet!"

    if db.get_rowcount() == 0:
        log.info("\n[bold orange3]%s\n", returnMessage, extra={"markup": True})
        return False

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
        info.append("\n\n")
        info.append(details)

        console.print("\n",
                      Panel(
                          info,
                          padding=(1, 5),
                          title="{}. {}".format(task_id, title),
                          title_align="left",
                          highlight=True,
                          expand=False
                      )
                      )

    return True


def view_categories():
    result = db.get_categories()
    if db.get_rowcount() == 0:
        log.info("\n[bold orange3]No Categories Yet!\n",
                 extra={"markup": True})
        return False

    table = Table(
        title="\nCategories",
        header_style="bold green",
        leading=1,
        title_justify="center",
        safe_box=True,
        row_styles=["", "dim"],
    )
    table.add_column("Category Id", justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Description", justify="center")

    for category_id, name, description in result:
        table.add_row(str(category_id), name, description)

    console.print(table, "\n")
    return True


def add_task():
    console.print("\n***Create New Task***")
    title = Prompt.ask("Title")
    details = Prompt.ask("Details")
    deadline = Prompt.ask("Deadline (YYYY-MM-DD hh:mm)")
    db.add_task(title, details, deadline)


def delete_task():
    if not view_tasks():
        return

    console.print("\n***Delete a Task***")
    taskid = IntPrompt.ask("Task Id")
    db.delete_task(taskid)


def add_category():
    console.print("\n***Create New Category***")
    title = Prompt.ask("Name")
    details = Prompt.ask("Description")
    db.add_category(title, details)


def delete_category():
    if not view_categories():
        return

    console.print("\n***Delete a Category***")
    Id = IntPrompt.ask("Category Id")
    db.get_category_one(Id)
    if db.get_rowcount() == 1:
        console.print(
            f"\nThis Category Contains {db.get_rowcount()} Task(s). No tasks will be deleted.")
        confirmDelete = Confirm.ask("Confirm to delete Category")
        if confirmDelete == True:
            db.update_task_to_delete(Id)
        else:
            log.info("\n[bold orange3]Delete Category Cancelled!\n",
                     extra={"markup": True})
            return
    db.delete_category(Id)


def mark_task_done():
    if not view_tasks():
        return

    console.print("\n***Mark Task as Done***")
    taskid = IntPrompt.ask("Task Id")
    db.mark_task_done(taskid)


def update_task():
    if not view_tasks():
        return

    console.print("\n***Task to be Edited***")
    taskid = IntPrompt.ask("Task Id")

    result = db.get_tasks_one(taskid)

    if db.get_rowcount() == 0:
        log.info("\n[bold orange3]Task does not exist!\n",
                 extra={"markup": True})
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
    newFinished = Prompt.ask("New Finished", choices=["", "Yes", "No"])
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

        try:
            if newCategory == "":
                newCategory = category_id
            else:
                newCategory = int(newCategory)
        except ValueError as e:
            log.error("\n[bold red]Invalid Category Id\n",
                      extra={"markup": True})
            return

    db.update_task_whole(taskid, newTitle, newDetails,
                         newDeadline, newFinished, newCategory)


CATEGORYCHOICES = [str(x) for x in range(4)]
CATEGORYMESSAGES = """
***Update a Category***
[0] Cancel Update
[1] Name only
[2] Description only
[3] Both"""


def update_category():

    console.print(CATEGORYMESSAGES)
    holder = IntPrompt.ask(
        "Choice", choices=CATEGORYCHOICES, show_choices=False)

    match holder:
        case 0:
            log.info("\n[bold orange3]Update Cancelled!\n",
                     extra={"markup": True})
        case 1:
            category_name_only()
        case 2:
            category_description_only()
        case 3:
            category_both()


def category_name_only():
    if not view_categories():
        return

    console.print("\n***Category to be Edited***")
    categoryid = IntPrompt.ask("Category Id")
    newName = Prompt.ask("New Name")
    db.update_category_name(newName, categoryid)


def category_description_only():
    if not view_categories():
        return

    console.print("\n***Category to be Edited***")
    categoryid = IntPrompt.ask("Category Id")
    newDescription = Prompt.ask("New Description")
    db.update_category_Description(newDescription, categoryid)


def category_both():
    if not view_categories():
        return

    console.print("\n***Category to be Edited***")
    categoryid = IntPrompt.ask("Category Id")
    newTitle = Prompt.ask("New Title")
    newDescription = Prompt.ask("New Description")
    db.update_category_both(newTitle, newDescription, categoryid)


def add_task_to_category():
    if not view_tasks():
        return

    if not view_categories():
        return

    console.print("\n***Add a Task to a Category***")
    taskid = IntPrompt.ask("Task Id")
    categoryid = IntPrompt.ask("Category Id")
    db.add_task_to_category(categoryid, taskid)


CHOICES = [str(x) for x in range(14)]
MAINMENUCOMMANDS = """ [0] Quit
 [1] Add Task
 [2] Edit Task
 [3] Delete Task
 [4] View Tasks (All)
 [5] View Tasks (Day)
 [6] View Tasks (Month)
 [7] View Tasks (Category)
 [8] Mark Task as Done
 [9] Add Category
[10] Edit Category
[11] Delete Category
[12] View Categories
[13] Add Task to Category"""


def menu():
    while True:
        console.print(Panel(Text(MAINMENUCOMMANDS, justify="left"), padding=(1, 1),
                            title="[bold blue]Task Record System", title_align="center", expand=False),)
        choice = IntPrompt.ask("Choice", choices=CHOICES, show_choices=False)
        match choice:
            case 1: add_task()
            case 2: update_task()
            case 3: delete_task()
            case 4: view_tasks()
            case 5: view_tasks("DAY")
            case 6: view_tasks("MONTH")
            case 7: view_tasks("CATEGORY")
            case 8: mark_task_done()
            case 9: add_category()
            case 10: update_category()
            case 11: delete_category()
            case 12: view_categories()
            case 13: add_task_to_category()
            case 0:
                db.close()
                console.print("\nGoodbye!")
                break


if __name__ == '__main__':
    menu()
