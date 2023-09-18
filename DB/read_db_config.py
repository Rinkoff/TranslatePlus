from configparser import ConfigParser
import os

# Get the directory where this file is located
package_directory = os.path.dirname(os.path.abspath(__file__))


def read_db_config(filename="config.ini", section="MySQL"):
    """
    Reads the MySQL database configuration from a file and returns it as a dictionary.

    Args:
    filename (str): the name of the configuration file (default is "config.ini")
    section (str): the section in the configuration file where the MySQL configuration is located (default is "MySQL")

    Returns:
    db_config (dict): a dictionary containing the MySQL database configuration
    """

    parser = ConfigParser()

    # Read the configuration file
    if parser.read(os.path.join(package_directory, filename)):

        db_config = {}

        if parser.has_section(section):
            items = parser.items(section)

            for item in items:
                db_config[item[0]] = item[1]

            return db_config

        else:
            raise Exception(f"Can't found {section} in {filename}")

    else:
        raise Exception(f"Can't found {filename}")
