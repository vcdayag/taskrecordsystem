import mariadb
from logger import logger
log = logger()


class DATABASE():
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connection = mariadb.connect(
            user="root",
            password="password",
            host="127.0.0.1",
            port=3306,
            database="taskrecordsystem"
        )
        self.cursor = self.connection.cursor()
        log.debug("Connected succesfully")

    def get_rowcount(self):
        return self.cursor.rowcount

    def add_query(self, statement, row):
        """Example of insert query one row at a time

        Args:
            statement (string): sql statement with ? as the place holder of where values should be located
            row (tuple): values that will replace the ? in the statement 
        """

        """
        Example:
        statement = "INSERT INTO test.contacts(first_name, last_name, email) VALUES (?, ?, ?)",
        row = (first_name, last_name, email)
        """
        try:
            self.cursor.execute(statement, row)
            self.connection.commit()
        except mariadb.Error as e:
            log.error(e)

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
            log.error(e)

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
        return self.cursor

    def get_tasks(self):
        return self.get_query("SELECT title, details FROM task")

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    # Examples
    db = DATABASE()
    db.connect()
    # Select Statements
    print([x for x in db.get_query("SELECT * FROM category")])
    # Insert Statements
    db.add_query("INSERT INTO task(title,details,deadline,finished,category_id) VALUES (%s,%s,STR_TO_DATE(%s,'%Y-%m-%d %h:%i:%s'),%d,%d)",
                 ("THIS IS TITLE", "DETAILS", "2013-07-22 12:50:05", True, 1))
