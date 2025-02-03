import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DB:
    def __init__(self, name, user, password, host, port, new=True):

        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
            if new:
                sql_create_database = f'create database {self.name}'
                self.cursor.execute(sql_create_database)

        except Exception:
            excp = Exception('Something went wrong')
            raise excp

        self.cursor.close()
        self.connection.close()

    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def connect(self):
        self.connection = psycopg2.connect(dbname=self.name, user=self.user, password=self.password, host=self.host)
        self.cursor = self.connection.cursor()

    def insert(self, columns: list, values: list):
        self.connect()
        self.cursor.executemany(f'INSERT into {self.name} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(values[0]))})', values)
        self.close_connection()

    def create_table(self, ex):
        self.connect()
        self.cursor.execute(ex)
        self.close_connection()

    def command(self, command):
        self.connect()
        self.cursor.execute(command)
        self.close_connection()


if __name__ == '__main__':
    test2 = DB('test4', 'postgres', '2706', 'localhost', '5432', new=False)
