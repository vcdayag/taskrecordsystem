from dotenv import dotenv_values
import mariadb
from logger import logger
import sys

log = logger()
config = dotenv_values()


class DATABASE():
    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user="tsruser",
                password="tsrpassword",
                host="127.0.0.1",
                port=3306,
                database="taskrecordsystem"
            )
            self.cursor = self.connection.cursor()
            log.info("[bold green]Connected successfully",
                     extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})
            sys.exit(0)

    def get_rowcount(self):
        return self.cursor.rowcount

    def query(self, statement, row):
        """Example of insert query with multiple rows at a time

        Args:
            statement (string): SQL statement
            row (tuple): tuple of values for the statement if needed.
        """
        
        try:
            self.cursor.execute(statement, row)
            self.connection.commit()
            log.info("[bold green]Successfully Added!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})

    def add_task(self, title, details, deadline):
        self.query("INSERT INTO task(title, details, deadline) VALUES (%s, %s, TIMESTAMP(%s))",
                           (title, details, deadline))

    def add_category(self, name, description):
        self.query(
            "INSERT INTO category(name, description) VALUES (%s, %s)", (name, description))

    def mark_task_done(self, Id):
        self.query(
            "UPDATE task SET finished=1 WHERE task_id=%s", (Id,))

    def update_task_title(self, title, Id):
        self.query(
            "UPDATE task SET title=%s WHERE task_id=%s", (title, Id))

    def update_task_details(self, details, Id):
        self.query(
            "UPDATE task SET details=%s WHERE task_id=%s", (details, Id))
        log.info("[bold green]Successfully Edited!", extra={"markup": True})

    def update_task_both(self, title, details, Id):
        self.query(
                "UPDATE task SET title=%s, details=%s WHERE task_id=%s", (title, details, Id))

    def update_category_name(self, name, Id):
        self.query(
                "UPDATE category SET name=%s WHERE category_id=%s", (name, Id))

    def update_category_description(self, description, Id):
        self.query(
                "UPDATE category SET description=%s WHERE category_id=%s", (description, Id))

    def update_category_both(self, name, description, Id):
        self.query(
                "UPDATE category SET name=%s, description=%s WHERE category_id=%s", (name, description, Id))

    def add_task_to_category(self, categoryId, taskId):
        self.query(
                "UPDATE task SET category_id=%s WHERE task_id=%s", (categoryId, taskId))
        
    def delete_task(self, Id):
        try:
            self.cursor.execute("DELETE FROM task WHERE task_id=%s", (Id))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                log.info("No task was deleted")
            else:
                log.info("[bold green]Successfully Deleted!",
                         extra={"markup": True})

        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})

    def delete_category(self, Id):
        try:
            self.cursor.execute(
                "DELETE FROM category WHERE category_id=%s", (Id))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                log.info("No task was deleted")
            else:
                log.info("[bold green]Successfully Deleted!",
                         extra={"markup": True})

        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})

    def get_query(self, statement, values=()):
        """_summary_

        Args:
            statement (string): SQL statement
            row (tuple): tuple of values for the statement if needed.

        Returns:
            list: a list of dictionary where the keys of the dictionary is the labels of the selected rows
        """
        
        try:
            self.cursor.execute(statement, values)
            return self.cursor.fetchall()
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})
            return []
        

    def get_tasks(self):
        return self.get_query("SELECT * FROM task")

    def get_tasks_day(self, date):
        return self.get_query("SELECT * FROM task WHERE DATE_FORMAT(deadline, '%Y-%m-%d') = %s", (date,))

    def get_tasks_month(self, month):
        return self.get_query("SELECT * FROM task WHERE DATE_FORMAT(deadline, '%Y-%m') = %s", (month,))

    def get_categories(self):
        return self.get_query("SELECT * FROM category")

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    # Test Examples
    db = DATABASE()
    db.connect()
    # Select Statements
    print([x for x in db.get_query("SELECT * FROM category")])
    # Insert Statements
    db.add_task("INSERT INTO task(title,details,deadline,finished,category_id) VALUES (%s,%s,STR_TO_DATE(%s,'%Y-%m-%d %h:%i:%s'),%d,%d)",
                ("THIS IS TITLE", "DETAILS", "2013-07-22 12:50:05", True, 1))
