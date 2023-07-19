from sqlalchemy import text

from database.engine import ConnectionFactory
from database.schemas import Base


class SqlResourceManager:
    def __init__(self, connection_factory: ConnectionFactory) -> None:
        self.connection_factory = connection_factory

    def create_all_tables(self):
        with self.connection_factory() as connection:
            Base.metadata.create_all(connection)

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

            for table_name in Base.metadata.tables:
                connection.execute(text(f'DROP TABLE IF EXISTS {table_name};'))

            # Re-enable foreign key checks
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))

    def make_column_nullable(self, table_name: str):
        pass
