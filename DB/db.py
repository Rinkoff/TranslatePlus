import mysql.connector as conn
from DB.read_db_config import read_db_config


class DB:
    """
    A class representing a MySQL database connection.

    Attributes:
    connector (MySQLConnection): A connection to the MySQL database.

    Methods:
    create_user_data_table(): Creates a new table called `users` in the database.
    create_table_for_saved_text(): Creates a new table called `user_texts` in the database.
    add_new_user(data): Adds a new user to the `users` table.
    add_text(username, text): Adds a new saved text to the `user_texts` table.
    select_texts(username): Retrieves all saved texts for a given username from the `user_texts` table.
    select_usernames(): Retrieves all usernames from the `users` table.
    take_user_password(username): Retrieves the password for a given username from the `users` table.
    """

    def __init__(self):
        """
        Initializes a new MySQL database connection based on the configuration file.
        """

        db_config = read_db_config("../config.ini", "MySQL")

        try:
            self.connector = conn.connect(
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                host=db_config["host"],
                port=db_config["port"],
            )

        except conn.Error as e:
            print(e)

    def create_user_data_table(self):
        """
        Creates a new table called `users` in the database.

        Returns:
        None
        """

        query = """
               CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(20) NOT NULL,
                email VARCHAR(50) NOT NULL
                );
        """

        try:
            with self.connector.cursor() as cur:
                cur.execute(query)
                self.connector.commit()

        except conn.Error as e:
            print(e)

    def add_new_user(self, data):
        """
        Adds a new user to the `users` table.

        Args:
        data (list): A list containing the username, password, and email of the new user.

        Returns:
        None
        """
        query = """
                INSERT IGNORE INTO users
                (username,password,email)
                VALUES (%s, %s, %s)
            """

        try:
            with self.connector.cursor(prepared=True) as cur:
                cur.execute(query, data)
                self.connector.commit()

        except conn.Error as e:
            print(e)

    def create_table_for_saved_text(self):
        """
        Creates a new table called `user_texts` in the database.

        Returns:
        None
        """
        query = f"""
               CREATE TABLE IF NOT EXISTS user_texts(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(20) NOT NULL,
                saved_text VARCHAR(100) NOT NULL 
                );
        """

        try:
            with self.connector.cursor() as cur:
                cur.execute(query)
                self.connector.commit()

        except conn.Error as e:
            print(e)

    def add_text(self, username, text):
        """
        Inserts a new text into the user_texts table.

        Args:
        username (str): The username of the user who saved the text.
        text (str): The text to be saved.

        Returns:
        None
        """
        query = "INSERT INTO user_texts (username, saved_text) VALUES (%s, %s)"
        values = (username, text)

        try:
            with self.connector.cursor(prepared=True) as cur:
                cur.execute(query, values)
                self.connector.commit()

        except conn.Error as e:
            print(e)

    def select_texts(self, username):
        """
        Selects all saved texts for a given username.

        Args:
        username (str): The username of the user whose texts are to be selected.

        Returns:
        result_list (list): A list of tuples containing all saved texts for the given username.
        """
        query = f"SELECT saved_text FROM user_texts WHERE username = '{username}'"

        with self.connector.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            result_list = list(result)
            return result_list

    def select_usernames(self):
        """
        Selects all usernames in the users table.

        Returns:
        result_list (list): A list of all usernames in the users table.
        """

        query = "SELECT username FROM users"

        with self.connector.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            result_list = [value[0] for value in result]
        return result_list

    def take_user_password(self, username):
        """
        Selects the password for a given username.

        Args:
        username (str): The username of the user whose password is to be selected.

        Returns:
        password (str): The password for the given username.
                         Returns "miss" if the username is not found in the users table.
        """

        query = f"SELECT password FROM users WHERE username = '{username}'"

        with self.connector.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()

            if result:
                password = result[0]
                return password
            else:
                return "miss"


    def remove_saved_text(self,username,text):
        """
        Deletes a given text for a given username from the 'user_texts' table in the database.

        Args:
        username (str): The username of the user whose text is to be deleted.
        text (str): The text to be deleted.

        Returns:
        None
        """

        query = f"DELETE FROM user_texts WHERE username = '{username}' AND saved_text = '{text}'"

        try:
            with self.connector.cursor(prepared=True) as cur:
                cur.execute(query)
                self.connector.commit()

        except conn.Error as e:
            print(e)