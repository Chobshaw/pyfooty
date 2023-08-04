from sqlalchemy import URL, text

from database.engine import ConnectionFactory, Database
from database.schemas import BaseModel


class SqlResourceManager:
    def __init__(self, connection_factory: ConnectionFactory) -> None:
        self.connection_factory = connection_factory

    def create_all_tables(self):
        with self.connection_factory() as connection:
            BaseModel.metadata.create_all(connection)

    def delete_table(self, table_name: str):
        with self.connection_factory() as connection:
            # Disable foreign key checks to allow deletion of table with circular dependencies
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))

            # Delete table
            connection.execute(text(f'DROP TABLE IF EXISTS {table_name};'))

            # Re-enable foreign key checks
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))

    def delete_all_tables(self):
        with self.connection_factory() as connection:
            # Disable foreign key checks to allow deletion of table with circular dependencies
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))

            for table in connection.execute(text('SHOW TABLES;')):
                connection.execute(text(f'DROP TABLE {table[0]};'))

            # Re-enable foreign key checks
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))

    def make_column_nullable(self, table_name: str):
        pass


if __name__ == '__main__':
    url_object = URL.create(
        drivername='mysql+mysqlconnector',
        username='footymanager',
        password='?Ch0bbyF00ty',
        host='localhost',
        port=3306,
        database='pyfooty',
    )
    database = Database(url_object)
    resource_manager = SqlResourceManager(
        connection_factory=database.connection
    )
    resource_manager.delete_all_tables()
    resource_manager.create_all_tables()
