from settings.loader import config

from database import queries
import psycopg2
from psycopg2.extras import RealDictCursor


class BaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(config.db.url)

    def manage(self,
               sql: str, *args,
               fetchone: bool = False,
               fetchall: bool = False,
               commit: bool = False
               ):
        # returning *
        with self.connection as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, args)

                if fetchone and commit:
                    connection.commit()
                    return cursor.fetchone()
                if fetchone:
                    return cursor.fetchone()
                if fetchall:
                    return cursor.fetchall()

                connection.commit()
                return


class TableManager(BaseManager):
    def is_table_exists(self, table_name: str):
        return self.manage(queries.TABLE_EXISTS_SQL, table_name, fetchone=True)

    def create_tables(self):
        for table_name, table_sql in queries.TABLES_DATA.items():
            if not self.is_table_exists(table_name).get('exists'):
                self.manage(table_sql, commit=True)
                print(f'{table_name} table created')


table_manager = TableManager()
