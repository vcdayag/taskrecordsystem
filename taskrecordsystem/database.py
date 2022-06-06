import mariadb
from logger import logger
import sys

log = logger()


class DATABASE():
    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user="trsuser",
                password="trspassword",
                host="127.0.0.1",
                port=3306,
                database="taskrecordsystem"
            )
            self.cursor = self.connection.cursor()
            log.debug("[bold green]Connected successfully",
                      extra={"markup": True})
        except mariadb.Error as e:
            log.error("\n[bold red]%s\n", e, extra={"markup": True})
            sys.exit(0)

    def get_rowcount(self):
        return self.cursor.rowcount

    def query(self, statement, row, successful, unsuccessful):
        """Example of insert query with multiple rows at a time

        Args:
            statement (string): SQL statement
            row (tuple): tuple of values for the statement if needed.
        """

        try:
            self.cursor.execute(statement, row)
            self.connection.commit()
            if self.cursor.rowcount == 0:
                log.info("\n[bold orange3]%s\n", unsuccessful,
                         extra={"markup": True})
            else:
                log.info("\n[bold green]%s\n", successful,
                         extra={"markup": True})
        except mariadb.Error as e:
            if e.errno == 1451:
                log.error("\n[bold red]Tasks exists in this Category therefore it can not be deleted!\n", extra={
                          "markup": True})
            if e.errno == 1452:
                log.error("\n[bold red]Category Id does not exist!\n", extra={
                          "markup": True})
            else:
                log.error("\n[bold red]%s\n", e, extra={"markup": True})

    def delete_query(self, statement, row):
        self.query(statement, row, "Successfully Deleted!",
                   "Nothing was deleted")

    def update_query(self, statement, row):
        self.query(statement, row, "Successfully Edited!",
                   "Nothing was edited")

    def add_query(self, statement, row):
        self.query(statement, row, "Successfully Added!",
                   "Nothing was added")

    def add_task(self, title, details, deadline):
        self.add_query("INSERT INTO task(title, details, deadline) VALUES (%s, %s, TIMESTAMP(%s))",
                       (title, details, deadline))

    def add_category(self, name, description):
        self.add_query(
            "INSERT INTO category(name, description) VALUES (%s, %s)", (name, description))

    def add_task_to_category(self, categoryId, taskId):
        self.add_query(
            "UPDATE task SET category_id=%d WHERE task_id=%d", (categoryId, taskId))

    def mark_task_done(self, Id):
        self.update_query(
            "UPDATE task SET finished=1 WHERE task_id=%d", (Id,))

    def update_task_whole(self, Id, title, details, deadline, finished, categoryId):
        self.update_query(
            "UPDATE task SET title=%s, details=%s, deadline=TIMESTAMP(%s), finished=%d, category_id=%d WHERE task_id=%d", (title, details, deadline, finished, categoryId, Id))

    def update_task_to_delete(self, categoryId):
        self.update_query(
            "UPDATE task SET category_id = NULL WHERE category_id=%d", (categoryId,))

    def update_category_name(self, name, Id):
        self.update_query(
            "UPDATE category SET name=%s WHERE category_id=%d", (name, Id))

    def update_category_description(self, description, Id):
        self.update_query(
            "UPDATE category SET description=%s WHERE category_id=%d", (description, Id))

    def update_category_both(self, name, description, Id):
        self.update_query(
            "UPDATE category SET name=%s, description=%s WHERE category_id=%d", (name, description, Id))

    def delete_task(self, Id):
        self.delete_query("DELETE FROM task WHERE task_id=%d", (Id,))

    def delete_category(self, Id):
        self.delete_query("DELETE FROM category WHERE category_id=%d", (Id,))

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
        return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              """)

    def get_tasks_one(self, Id):
        return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              WHERE task_id=%d""", (Id,))

    def get_tasks_day(self, date):
        return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              WHERE DATE_FORMAT(deadline, '%Y-%m-%d') = %s""", (date,))

    def get_tasks_month(self, month):
        return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              WHERE DATE_FORMAT(deadline, '%Y-%m') = %s""", (month,))

    def get_tasks_category(self, Id):
        if Id == 0:
            return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              WHERE t.category_id is NULL""")

        return self.get_query("""
                              SELECT task_id, title, details, deadline, finished, t.category_id, name
                              FROM task AS t
                              LEFT JOIN category AS c
                              ON t.category_id=c.category_id
                              WHERE t.category_id=%d""", (Id,))

    def get_categories(self):
        return self.get_query("SELECT * FROM category")

    def get_category_one(self, Id):
        return self.get_query("SELECT * FROM category WHERE category_id=%d", (Id,))

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
