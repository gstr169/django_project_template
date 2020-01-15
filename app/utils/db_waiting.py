import os
import psycopg2
from time import sleep


def wait_for_db(host: str, port: int, user: str, password: str, dbname: str, retries: int = 10, period: int = 2):
    # response = None
    for i in range(retries):
        try:
            with psycopg2.connect(host=host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  dbname='postgres') as psql_connection:
                with psql_connection.cursor() as psql_cursor:
                    # Preparing main data for using in sql requests
                    psql_cursor.execute('SELECT COUNT(*) FROM pg_database WHERE datname = %s;', [dbname])
                    # response = psql_cursor.fetchone()
                    # if isinstance(response, tuple):
                    #     response = response[0]
        except psycopg2.OperationalError as err:
            sleep(period)
        else:
            break


if __name__ == '__main__':
    # TODO: set postgres container name
    host = 'project_db'
    port = 5432
    user = 'postgres'
    password = os.getenv('PGPASSWORD')
    dbname = os.getenv('PGDATABASE')
    wait_for_db(host, port, user, password, dbname)
