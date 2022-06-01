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
            log.error("\n[bold red]%s\n",e, extra={"markup": True})
            sys.exit(0)

    def get_rowcount(self):
        return self.cursor.rowcount

    def add_task(self, title, details, deadline):
        # Example of insert query one row at a time

        try:
            self.cursor.execute(
                "INSERT INTO task(title, details, deadline) VALUES (%s, %s, TIMESTAMP(%s))", (title, details, deadline))
            self.connection.commit()
            log.info("[bold green]Successfully Added!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def add_category(self, name, description):
        # Example of insert query one row at a time

        try:
            self.cursor.execute(
                "INSERT INTO category(name, description) VALUES (%s, %s)", (name, description))
            self.connection.commit()
            log.info("[bold green]Successfully Added!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def mark_as_done(self, Id):
        try:
            self.cursor.execute(
                "UPDATE task SET finished=1 WHERE task_id=%s", (Id))
            self.connection.commit()
            log.info("[bold green]Task Finished!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_task_title(self, title, Id):
        try:
            self.cursor.execute(
                "UPDATE task SET title=%s WHERE task_id=%s", (title, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_task_details(self, details, Id):
        try:
            self.cursor.execute(
                "UPDATE task SET details=%s WHERE task_id=%s", (details, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_task_both(self, title, details, Id):
        try:
            self.cursor.execute(
                "UPDATE task SET title=%s, details=%s WHERE task_id=%s", (title, details, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_category_name(self, name, Id):
        try:
            self.cursor.execute(
                "UPDATE category SET name=%s WHERE category_id=%s", (name, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_category_description(self, description, Id):
        try:
            self.cursor.execute(
                "UPDATE category SET description=%s WHERE category_id=%s", (description, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def update_category_both(self, name, description, Id):
        try:
            self.cursor.execute(
                "UPDATE category SET name=%s, description=%s WHERE category_id=%s", (name, description, Id))
            self.connection.commit()
            log.info("[bold green]Successfully Edited!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def add_task_to_category(self, categoryId, taskId):
        try:
            self.cursor.execute(
                "UPDATE task SET category_id=%s WHERE task_id=%s", (categoryId, taskId))
            self.connection.commit()
            log.info("[bold green]Successfully Added!", extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

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
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

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
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def add_multiple_query(self, statement, rows):
        """Example of insert query with multiple rows at a time

        Args:
            statement (string): sql statement with ? as the place holder of where values should be located
            rows (list): this is a list of tuple with values that will replace the ? in the statement
        """

        """
        Example:
        statement = "INSERT INTO test.contacts(first_name, last_name, email) VALUES (?, ?, ?)",
        rows = [(first_name, last_name, email)]
        """
        try:
            self.cursor.executemany(statement, rows)
            self.connection.commit()
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n",e, extra={"markup": True})

    def get_query(self, statement, values=()):
        """_summary_

        Args:
            statement (string): sql statement with ? as the place holder of where values should be located
            row (tuple): values that will replace the ? in the statement

        Returns:
            list: a list of dictionary where the keys of the dictionary is the labels of the selected rows
        """

        """
        Example:
        statement = "SELECT first_name, last_name, email FROM test.contacts WHERE email=?"
        row = (email)
        """

        self.cursor.execute(statement, values)
        return self.cursor.fetchall()

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
    # Examples
    db = DATABASE()
    db.connect()
    # Select Statements
    print([x for x in db.get_query("SELECT * FROM category")])
    # Insert Statements
    db.add_task("INSERT INTO task(title,details,deadline,finished,category_id) VALUES (%s,%s,STR_TO_DATE(%s,'%Y-%m-%d %h:%i:%s'),%d,%d)",
                ("THIS IS TITLE", "DETAILS", "2013-07-22 12:50:05", True, 1))
