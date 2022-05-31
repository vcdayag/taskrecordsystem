import mariadb
from logger import logger
log = logger()

from dotenv import dotenv_values

config = dotenv_values()


class DATABASE():
    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user=config["TSRUSER"],
                password=config["TSRPASSWORD"],
                host="127.0.0.1",
                port=3306
            )
            self.cursor = self.connection.cursor()
            log.info("Connected successfully")
        except mariadb.Error as e:
            log.error(e)
        
        #Creating a database
        self.cursor.execute("CREATE database IF NOT EXISTS taskrecordsystem")

        #Use the database
        self.cursor.execute("USE taskrecordsystem")

        #Creating category table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `category`(
            `category_id` INT UNSIGNED AUTO_INCREMENT,
            `name` VARCHAR(16) NOT NULL,
            `description` VARCHAR(128) DEFAULT NULL,
            CONSTRAINT `category_category_id_pk` PRIMARY KEY(`category_id`)
        )''')

        #Creating task table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `task`(
            `task_id` INT UNSIGNED AUTO_INCREMENT,
            `title` VARCHAR(64),
            `details` VARCHAR(1024),
            `deadline` TIMESTAMP,
            `finished` TINYINT DEFAULT 0,
            `category_id` INT UNSIGNED DEFAULT NULL,
            CONSTRAINT `task_task_id_pk` PRIMARY KEY(`task_id`),
            CONSTRAINT `task_category_id_fk` FOREIGN KEY(`category_id`) REFERENCES `category`(`category_id`)
        )''')

    def get_rowcount(self):
        return self.cursor.rowcount 

    def add_task(self,title,details):
        # Example of insert query one row at a time
        
        try:
            self.cursor.execute("INSERT INTO task(title, details, deadline) VALUES (%s, %s, CURTIME())",(title,details))
            self.connection.commit()
            log.info("Successfully Added!")
        except mariadb.Error as e:
            log.error(e)
    
    def add_category(self,name,description):
        # Example of insert query one row at a time
        
        try:
            self.cursor.execute("INSERT INTO category(name, description) VALUES (%s, %s)",(name,description))
            self.connection.commit()
            log.info("Successfully Added!")
        except mariadb.Error as e:
            log.error(e)

    def delete_task(self,Id):
        try:
            self.cursor.execute("DELETE FROM task WHERE task_id=%s",(Id,))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                log.info("No task was deleted")
            else:
                log.info("Successfully Deleted!")
                
        except mariadb.Error as e:
            log.error(e)
    
    def delete_category(self,Id):
        try:
            self.cursor.execute("DELETE FROM category WHERE category_id=%s",(Id,))
            self.connection.commit()
            if self.cursor.rowcount == 0:
                log.info("No task was deleted")
            else:
                log.info("Successfully Deleted!")
                
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
        return self.cursor.fetchall()

    def get_tasks(self):
        return self.get_query("SELECT task_id, title, details FROM task")
    
    def get_categories(self):
        return self.get_query("SELECT category_id, name, description FROM category")

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
